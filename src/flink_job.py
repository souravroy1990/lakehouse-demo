from pyflink.table import EnvironmentSettings, StreamTableEnvironment

# ----------------------------------------------------------------------------- 
# Create Flink environment
# ----------------------------------------------------------------------------- 
env_settings = EnvironmentSettings.in_streaming_mode()
t_env = StreamTableEnvironment.create(environment_settings=env_settings)

# ----------------------------------------------------------------------------- 
# Basic Flink configs
# ----------------------------------------------------------------------------- 
conf = t_env.get_config().get_configuration()

# Checkpointing
conf.set_string("execution.checkpointing.interval", "30s")
conf.set_string("execution.checkpointing.mode", "EXACTLY_ONCE")
conf.set_string("execution.checkpointing.timeout", "10min")

# MiniBatch tuning
conf.set_string("table.exec.mini-batch.enabled", "true")
conf.set_string("table.exec.mini-batch.allow-latency", "5 s")
conf.set_string("table.exec.mini-batch.size", "5000")

# Iceberg Streaming Commit
conf.set_string("table.exec.iceberg.streaming.commit.enabled", "true")
conf.set_string("table.exec.iceberg.streaming.commit.interval", "1 min")

# S3 / MinIO settings (these will be used by both Iceberg and Paimon)
conf.set_string("fs.s3a.access.key", "admin")
conf.set_string("fs.s3a.secret.key", "password")
conf.set_string("fs.s3a.endpoint", "http://minio:9000")
conf.set_string("fs.s3a.path.style.access", "true")
conf.set_string("fs.s3a.connection.ssl.enabled", "false")

# ----------------------------------------------------------------------------- 
# Register Hive-backed Iceberg Catalog
# ----------------------------------------------------------------------------- 
t_env.execute_sql("""
CREATE CATALOG hive_catalog WITH (
  'type' = 'iceberg',
  'catalog-type' = 'hive',
  'uri' = 'thrift://hive-metastore:9083',
  'warehouse' = 's3a://lakehouse/warehouse',
  'property-version' = '1',
  'hive-version' = '3.1.3'
)
""")

# ----------------------------------------------------------------------------- 
# Register Paimon Catalog (NEW) pointing to dedicated paimon warehouse
# ----------------------------------------------------------------------------- 
t_env.execute_sql("""
CREATE CATALOG paimon_catalog WITH (
  'type' = 'paimon',
  'warehouse' = 's3a://lakehouse/paimon/warehouse',
  'metastore' = 'hive',
  'uri' = 'thrift://hive-metastore:9083'
)
""")

# ----------------------------------------------------------------------------- 
# Use Default Catalog for Kafka (so it's NOT inside Iceberg or Paimon)
# ----------------------------------------------------------------------------- 
t_env.use_catalog("default_catalog")
t_env.use_database("default_database")

# ----------------------------------------------------------------------------- 
# Kafka Source Table
# ----------------------------------------------------------------------------- 
t_env.execute_sql("""
CREATE TABLE IF NOT EXISTS trade_source (
  trade_id STRING,
  symbol STRING,
  price DOUBLE,
  volume INT,
  trade_time TIMESTAMP(3),
  WATERMARK FOR trade_time AS trade_time - INTERVAL '5' SECOND
) WITH (
  'connector' = 'kafka',
  'topic' = 'fake-data-topic',
  'properties.bootstrap.servers' = 'kafka:9092',
  'properties.group.id' = 'flink-consumer-group',
  'format' = 'json',
  'json.ignore-parse-errors' = 'true',
  'json.timestamp-format.standard' = 'ISO-8601',
  'scan.startup.mode' = 'earliest-offset'
)
""")

# ----------------------------------------------------------------------------- 
# Iceberg Sink Table (created in Hive Catalog)
# ----------------------------------------------------------------------------- 
t_env.use_catalog("hive_catalog")

# Create DB
t_env.execute_sql("CREATE DATABASE IF NOT EXISTS trades_db")

# Create Iceberg table
t_env.execute_sql("""
CREATE TABLE IF NOT EXISTS trades_db.iceberg_trades (
  trade_id STRING,
  symbol STRING,
  price DOUBLE,
  volume INT,
  trade_time TIMESTAMP(3)
)
PARTITIONED BY (symbol)
WITH (
  'format-version'='2',
  'write.distribution-mode'='hash',
  'write.metadata.delete-after-commit.enabled'='true',
  'write.metadata.previous-versions-max'='50'
)
""")


# ----------------------------------------------------------------------------- 
# Paimon Sink Table (created in Paimon Catalog)
# - primary key + bucketing to enable changelog/upsert if you later want it
# ----------------------------------------------------------------------------- 
t_env.use_catalog("paimon_catalog")

# Create DB in paimon catalog (same logical DB name as Iceberg for parity)
t_env.execute_sql("CREATE DATABASE IF NOT EXISTS trades_db")

# Create the dedicated Paimon target table (v2) that will store streaming data
try:
    t_env.execute_sql("""
    CREATE TABLE IF NOT EXISTS trades_db.paimon_trades (
      trade_id STRING,
      symbol STRING,
      price DOUBLE,
      volume INT,
      trade_time TIMESTAMP(3),
      PRIMARY KEY (trade_id) NOT ENFORCED
    ) WITH (
      'bucket' = '8',
      'bucket-key' = 'trade_id',
      'changelog-producer' = 'full-compaction',
      'snapshot.time-retained' = '1 h',
      'snapshot.num-retained.min' = '5',
      'snapshot.num-retained.max' = '20'
    )
    """)

except Exception as e:
    # tolerate the scenario where Paimon finds existing schema/files on the filesystem
    msg = str(e)
    if "Schema in filesystem exists" in msg or "creation is not allowed" in msg or "Schema in filesystem" in msg:
        print("Note: Paimon schema already exists on filesystem — skipping create (non-fatal).")
    else:
        raise

# ----------------------------------------------------------------------------- 
# Ensure Paimon table is registered in catalog (if schema existed on filesystem but metastore entry is missing)
# This checks for the table and, if missing, attempts to register it by pointing to the existing path.
# ----------------------------------------------------------------------------- 
def ensure_registered():
    try:
        # If SHOW TABLES works and lists paimon_trades, nothing to do.
        res = t_env.execute_sql("SHOW TABLES IN paimon.trades_db")
        rows = list(res.collect())
        names = [r[1] for r in rows] if rows else []
        if "paimon_trades" in names:
            return
    except Exception:
        # SHOW TABLES may fail if DB doesn't exist in catalog — proceed to registration attempt
        pass

    # Attempt to register catalog metadata for the existing filesystem table.
    # Use the same catalog name you defined earlier: paimon_catalog
    fs_path = "s3a://lakehouse/paimon/warehouse/trades_db.db/paimon_trades"
    try:
        # switch to the paimon_catalog so CREATE TABLE registers there
        t_env.use_catalog("paimon_catalog")

        # Create a table entry in paimon_catalog pointing at the existing filesystem path
        t_env.execute_sql(f"""
        CREATE TABLE IF NOT EXISTS trades_db.paimon_trades (
          trade_id STRING,
          symbol STRING,
          price DOUBLE,
          volume INT,
          trade_time TIMESTAMP(3)
        ) WITH (
          'path' = '{fs_path}'
        )
        """)
        print("Registered existing Paimon filesystem table into catalog using path:", fs_path)

        # switch back to default catalog for the rest of the job (keeps original behavior)
        t_env.use_catalog("default_catalog")
    except Exception as e:
        # If registration fails, show clear error and re-raise so it's visible in logs
        print("Failed to register existing filesystem table into catalog. Error:", e)
        raise

# call the ensure step before doing the insert
ensure_registered()

# ----------------------------------------------------------------------------- 
# INSERT Kafka → Iceberg
# ----------------------------------------------------------------------------- 
# point back to the fully-qualified Kafka source
t_env.execute_sql("""
INSERT INTO hive_catalog.trades_db.iceberg_trades
SELECT trade_id, symbol, price, volume, trade_time
FROM default_catalog.default_database.trade_source
""")

# ----------------------------------------------------------------------------- 
# INSERT Kafka → Paimon (new dedicated paimon_trades)
# ----------------------------------------------------------------------------- 
t_env.execute_sql("""
INSERT INTO paimon_catalog.trades_db.paimon_trades
SELECT trade_id, symbol, price, volume, trade_time
FROM default_catalog.default_database.trade_source
""")

print("✅ Flink job successfully submitted — Kafka → Iceberg + Paimon (paimon_trades)")
