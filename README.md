# 🧠 Modern Open Lakehouse Demo — Python + Apache Iceberg + Paimon + Flink + Spark + Kafka + Hive + Superset

Welcome to the **Zero-to-Lakehouse** project — a fully open-source, production-style real-time data lakehouse, built entirely with:

- 🐍 **Python**
- 🔥 **Apache Kafka** (stream ingestion)
- ⚡ **Apache Flink** (stream processing)
- ❄️ **Apache Iceberg** (ACID tables)
- 🪶 **Apache Paimon** (streaming-first lakehouse tables)
- 🗂 **Hive Metastore** (catalog layer)
- 🚀 **Apache Spark & Trino** (interactive SQL engines)
- 🦆 **Duckdb** (In memory analytics)
- 📊 **Apache Superset** (dashboards + BI)
- 🪣 **MinIO** (S3-compatible data lake)
- 🐳 **Docker Compose** (unified orchestration)

This repository provides a fully functional **local lakehouse** that mirrors real-world architectures — perfect for **workshops, demos, learning, or rapid prototyping**.

## 📐 Architecture Overview

                          ┌──────────────────────┐
                          │   Fake Data Producer │
                          │   (Python Generator) │
                          └─────────┬────────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │     Kafka        │
                           │  (Stream Bus)    │
                           └────────┬─────────┘
                                    │
                                    ▼
                          ┌────────────────────┐
                          │      Flink         │
                          │ (PyFlink Streaming │
                          │   Transform + ETL) │
                          └───────┬────┬───────┘
                                  │    │
                    Writes ACID   │    │ Writes Streaming
                   batch/stream   │    │ upserts/append
                                  ▼    ▼
                    ┌──────────────┐   ┌────────────────┐
                    │   Iceberg    │   │    Paimon      │
                    │  (ACID OLAP  │   │ (Real-time OLAP│
                    │   Tables)    │   │ Tables)        │
                    └───────┬──────┘   └───────┬────────┘
                            │                  │
                            │ Metadata via Hive│
                            ▼                  ▼
                    ┌───────────────────────────────────┐
                    │          Hive Metastore           │
                    │   (Unified Catalog for both)      │
                    └───────────────┬───────────────────┘
                                    │
                                    ▼
                     ┌───────────────────────────────┐
                     │   Query Layer (SQL Engines)   │
                     │   ┌───────────┐  ┌──────────┐ │
                     │   │   Spark   │  │  Trino   │ │
                     │   └───────────┘  └──────────┘ │
                     └──────────────┬────────────────┘
                                    │
                                    ▼
                          ┌─────────────────────┐
                          │     Superset        │
                          │  Dashboards + BI    │
                          └─────────────────────┘

## 🗂 Folder Layout

```bash
/docker
    /duckdb                 → Duckdb volume
    /flink                  → Flink JobManager, TaskManager, configs, jobs
    /spark                  → Spark master/worker, SQL client, custom JARs
    /trino                  → Trino coordinator + catalog configs
    /hive                   → Hive Metastore + required dependencies
    /superset               → Superset initialization
    /minio                  → MinIO S3 bucket
/src                        → Source code
    /utils/kafka_utils.py   → PyFlink job writing to Iceberg + Paimon
    /data_generator.py      → Stream Data generator
    /flink_job.py           → Flink job
    /iceberg_rewrite.sc     → Scala script to rewrite/compact Iceberg data files
    /query_iceberg.py       → List Iceberg catalog objects + sample data
    /query_paimon.py        → List Paimon catalog objects + sample data
    /requirements.txt       → Python dependecies for generator and helpers
README.md                   → Includes details about the repository and steps to run the docker locally
```

### 🐧 For Rancher Desktop (WSL) Users

If you are using **Rancher Desktop** with **WSL** on **Windows**, Docker runs **inside the WSL
environment**, not directly on Windows.  
To access your project files, you must navigate to the mounted Windows filesystem.

👉 **Install WSL (if not already installed):**  
<https://learn.microsoft.com/en-us/windows/wsl/install>

After opening your WSL terminal, change directory to the repository location where the
`docker/` folder resides:

```bash
cd /mnt/c/Users/<username>/path/to/repository
```

### Download Dependency JARs

Download the required JAR from Maven Central using `wget`:

```bash
mkdir -p jars # from project root(lakehouse-demo in this case)
cd jars

# AWS SDK v1 bundle – required by Hadoop S3A to talk to S3 / MinIO
wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar

# Apache Commons Lang v2 – legacy utility classes used by Hadoop & Hive
wget https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar

# Guava internal dependency – required by newer Guava versions
wget https://repo1.maven.org/maven2/com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.jar

# Google Guava – core utilities used heavily by Hadoop, Hive, Iceberg, Flink
wget https://repo1.maven.org/maven2/com/google/guava/guava/28.2-jre/guava-28.2-jre.jar

# Hadoop AWS module – provides the S3A filesystem implementation
wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.10.1/hadoop-aws-2.10.1.jar

# Hive execution & metadata classes – required for Hive Metastore integration
wget https://repo1.maven.org/maven2/org/apache/hive/hive-exec/3.1.3/hive-exec-3.1.3.jar

# Iceberg runtime for Flink 1.18 – enables Flink read/write support for Iceberg tables
wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.18/1.6.0/iceberg-flink-runtime-1.18-1.6.0.jar

# Iceberg Hive runtime – allows Iceberg to use Hive Metastore as its catalog
wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-hive-runtime/1.6.0/iceberg-hive-runtime-1.6.0.jar

# Iceberg Spark runtime for Spark 3.5 (Scala 2.12) – required for spark
wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.6.0/iceberg-spark-runtime-3.5_2.12-1.6.0.jar

# Thrift utility library – required by Hive Metastore for RPC & metrics
wget https://repo1.maven.org/maven2/org/apache/thrift/libfb303/0.9.3/libfb303-0.9.3.jar
```

### Download Apache Spark

```bash
wget --no-check-certificate https://archive.apache.org/dist/spark/spark-3.5.1/spark-3.5.1-bin-hadoop3.tgz
```

## 🚀 How to Run the Entire Lakehouse

```bash
cd docker
docker compose up -d
```

Wait ~60 seconds for all services to initialize.

## 📡 1. Data Generator

### Check fake trades streaming into Kafka

```bash
docker logs -f docker-fake-data-producer-1
```

## 🔥 2. Kafka

### Enter the Kafka container and verify topics and messages

```bash
docker exec -it docker-kafka-1 /bin/bash

kafka-topics --bootstrap-server localhost:9092 --list

kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic fake-data-topic \
  --from-beginning \
  --max-messages 10
```

### Describe kafka topic setup

```bash
docker exec -it docker-kafka-1 kafka-topics \
  --bootstrap-server kafka:9092 \
  --describe \
  --topic fake-data-topic
```

### Earliest offset

```bash
docker exec -it docker-kafka-1 kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list kafka:9092 \
  --topic fake-data-topic \
  --time -2
```

### Latest offset

```bash
docker exec -it docker-kafka-1 kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list kafka:9092 \
  --topic fake-data-topic \
  --time -1
```

### Latest offset partition wise

```bash
docker exec -it docker-kafka-1 kafka-run-class kafka.tools.GetOffsetShell \
  --broker-list kafka:9092 \
  --topic fake-data-topic
```

## 🗂 3. Hive Metastore & Lake Storage Verification

### Enter the Hive Metastore container and verify that the Hadoop S3 (MinIO) filesystem is accessible

```bash
docker exec -it hive-metastore /bin/bash

hadoop fs -ls s3a://lakehouse/
```

If everything is configured correctly, you should see output similar to:

```bash
Found 2 items
drwxrwxrwx   - hive hive          0 2026-02-14 11:05 s3a://lakehouse/paimon
drwxrwxrwx   - hive hive          0 2026-02-14 11:05 s3a://lakehouse/warehouse
```

## ⚡ 4. Enter Flink JobManager Container

```bash
docker exec -it flink-jobmanager bash
```

Once inside flink jobmanager container run the flink job using

```bash
flink run -py /opt/flink/jobs/flink_job.py
```

### ⚡ Flink SQL — Iceberg (hive_catalog) & Paimon (paimon_catalog) Setup + Verification

Start Flink SQL clint using:

```bash
sql-client.sh
```

Below are the **sequential Flink SQL statements** to:

- Create Iceberg catalog (Hive-backed)
- Create Paimon catalog (Hive-backed)
- Verify databases
- Verify tables
- Query data

---

### Create Iceberg Catalog (Hive-backed)

```sql
CREATE CATALOG hive_catalog WITH (
  'type' = 'iceberg',
  'catalog-type' = 'hive',
  'uri' = 'thrift://hive-metastore:9083',
  'warehouse' = 's3a://lakehouse/warehouse',
  'property-version' = '1'
);
```

### Create Paimon Catalog(Hive-backed)

```sql
CREATE CATALOG paimon_catalog WITH (
  'type' = 'paimon',
  'warehouse' = 's3a://lakehouse/paimon/warehouse',
  'metastore' = 'hive',
  'uri' = 'thrift://hive-metastore:9083'
);
```

### Verify Catalogs

```sql
SHOW CATALOGS;
```

### Iceberg (hive_catalog) Verification

```sql
USE CATALOG hive_catalog;
SHOW DATABASES;
USE trades_db;
SHOW TABLES;
```

### Check Iceberg Snapshots

```sql
SELECT * FROM `hive_catalog`.`trades_db`.`iceberg_trades$snapshots`;
SELECT * FROM `hive_catalog`.`trades_db`.`iceberg_trades$history`;
```

### Query Iceberg Data

```sql
DESCRIBE iceberg_trades;
SELECT * FROM iceberg_trades LIMIT 10;
```

### Query Planning

```sql
EXPLAIN FORMATTED
SELECT *
FROM hive_catalog.trades_db.iceberg_trades
WHERE symbol = 'INFY';

EXPLAIN
SELECT *
FROM hive_catalog.trades_db.iceberg_trades
WHERE symbol = 'INFY';
```

### File Pruning

```sql
SELECT *
FROM hive_catalog.trades_db.iceberg_trades
WHERE symbol = 'INFY';
```

Check in spark jobs UI -> Sql/Dataframe for no. of files scanned

### Enable Runtime & Adaptive Plan Visibility

```sql
SET spark.sql.adaptive.enabled = true;
SET spark.sql.adaptive.logLevel = DEBUG;
SET spark.sql.optimizer.excludedRules = '';
SET spark.sql.iceberg.planning.enabled=true;
```

### Explain With Cost & Statistics

```sql
EXPLAIN COST
SELECT *
FROM hive_catalog.trades_db.iceberg_trades
WHERE symbol = 'INFY';
```

### Confirm Partition Pruning Explicitly

```sql
SELECT *
FROM hive_catalog.trades_db.iceberg_trades
WHERE price > 1000;
```

Scans all partition

```sql
SELECT *
FROM hive_catalog.trades_db.iceberg_trades
WHERE symbol = 'INFY'
AND price > 1000;
```

Scans only 1 partition

**Note: Iceberg + Spark reads data in columnar format (Arrow / vectorized Parquet), Require row-based processing So Spark inserts: Columnar → Row conversion, Batchscan means Iceberg optimizations are happening**

### Groupby

```sql
SELECT symbol, COUNT(*) FROM  hive_catalog.trades_db.iceberg_trades GROUP BY symbol;

EXPLAIN FORMATTED
SELECT symbol, COUNT(*)
FROM hive_catalog.trades_db.iceberg_trades
GROUP BY symbol;
```

### Iceberg Schema Evolution

### ADD Column

```sql
ALTER TABLE hive_catalog.trades_db.iceberg_trades
ADD COLUMNS (
  exchange STRING
);

SELECT * FROM hive_catalog.trades_db.iceberg_trades LIMIT 5;
```

### RENAME COLUMN

```sql
ALTER TABLE hive_catalog.trades_db.iceberg_trades
RENAME exchange TO exchange_system;
```

### DROP COLUMN

```sql
ALTER TABLE hive_catalog.trades_db.iceberg_trades
DROP COLUMN trade_time;

DESCRIBE hive_catalog.trades_db.iceberg_trades;
```

**Note: Schema evolution, Partition evolution doesn't create new snapshot, only metadata.json is created**

### Partition Evolution

#### Add new partition

```sql
ALTER TABLE hive_catalog.trades_db.iceberg_trades
ADD PARTITION FIELD trade_id;
```

#### Drop old partition

```sql
ALTER TABLE hive_catalog.trades_db.iceberg_trades
DROP PARTITION FIELD symbol;

DESCRIBE hive_catalog.trades_db.iceberg_trades;
DESCRIBE TABLE EXTENDED trades_db.iceberg_trades;
```

#### Check partiiton pruning still works with symbol

```sql
SELECT * FROM hive_catalog.trades_db.iceberg_trades WHERE symbol = 'INFY';
```

#### Expire old snapshots

```sql
CALL hive_catalog.system.expire_snapshots(
'trades_db.iceberg_trades',
TIMESTAMP '2026-02-25 00:00:00'
);
```

#### Remove orphan files

```sql
CALL hive_catalog.system.remove_orphan_files(
'trades_db.iceberg_trades'
);
```

#### Repartition(CTAS migration)

```sql
CREATE TABLE trades_db.iceberg_trades_v2
USING iceberg
PARTITIONED BY (trade_id)
AS
SELECT * FROM trades_db.iceberg_trades;
```

After a CTAS migration old and new table can be swapped and old table can be deleted. This is the cleanest way.

### Iceberg prevents auto reuse of old column

Do this in same order

```sql
ALTER TABLE hive_catalog.trades_db.iceberg_trades DROP COLUMN trade_time;
ALTER TABLE hive_catalog.trades_db.iceberg_trades DROP COLUMN exchange;
ALTER TABLE hive_catalog.trades_db.iceberg_trades ADD COLUMN trade_time timestamp;
SELECT * FROM trades_db.iceberg_trades limit 5;
```

It should show the trade_time as NULL as iceberg don't use same column identity internally to prevent PII, GDPR regulations. To get back the old data simply DROP the table and re-register with the first metadata with which it was working.

### Partition + Bucket together

```sql
ALTER TABLE iceberg_trades
SET PARTITION SPEC (
  symbol,
  bucket(16, trade_id)
);
```

This creates a partition based on symbol and then buckets based on hash of trade-id. Help with query example- WHERE symbol='INFY'	Partition pruning, WHERE trade_id='uuid' Bucket pruning, WHERE symbol='INFY' AND trade_id='uuid' Excellent pruning.

### Rollback

1. Rollback is only applicable to snapshot and not to schema/partition i.e. metadata. So if only one snapshot exists then the best way to restore table to old format is to use CTAS and recreate another table using the data from the old table

2. Other option is manual restore.

```sql
SELECT snapshot_id,parent_id,operation,committed_at
FROM hive_catalog.trades_db.iceberg_trades.snapshots
ORDER BY committed_at;

INSERT INTO hive_catalog.trades_db.iceberg_trades
VALUES
('rollback-test-1', 'INFY', 999.99, 10, TIMESTAMP '2026-02-28 10:00:00'),
('rollback-test-2', 'TCS',  888.88, 20, TIMESTAMP '2026-02-28 10:05:00');

SELECT symbol, COUNT(*) FROM  hive_catalog.trades_db.iceberg_trades GROUP BY symbol;

INSERT INTO hive_catalog.trades_db.iceberg_trades
VALUES
('rollback-test-3', 'TCS', 998.99, 10, TIMESTAMP '2026-02-28 10:00:00');

SELECT snapshot_id,parent_id,operation,committed_at
FROM hive_catalog.trades_db.iceberg_trades.snapshots
ORDER BY committed_at;

SELECT * FROM hive_catalog.trades_db.iceberg_trades WHERE trade_id LIKE 'rollback-test%';

CALL hive_catalog.system.rollback_to_snapshot('trades_db.iceberg_trades', 4291488040064066143);

SELECT symbol, COUNT(*) FROM  hive_catalog.trades_db.iceberg_trades GROUP BY symbol;
SELECT * FROM hive_catalog.trades_db.iceberg_trades WHERE trade_id LIKE 'rollback-test%';
```

Rollback based on timestamp is also allowed using

```sql
CALL hive_catalog.system.rollback_to_timestamp('trades_db.iceberg_trades', TIMESTAMP '2026-02-19 16:05:29');
```

### Check ancestor lineage

```sql
SELECT * FROM hive_catalog.trades_db.iceberg_trades.history;
```

### Paimon (hive_catalog) Verification

```sql
USE CATALOG paimon_catalog;
SHOW DATABASES;
USE trades_db;
SHOW TABLES;
```

### Check Paimon Snapshots

```sql
SELECT * FROM `paimon_catalog`.`trades_db`.`paimon_trades$snapshots`;
SELECT * FROM `paimon_catalog`.`trades_db`.`paimon_trades$history`;
SELECT * FROM `paimon_trades$partitions`;
SELECT * FROM `paimon_trades$files`;
SELECT * FROM `paimon_trades$manifests`;
SELECT * FROM `paimon_trades$partitions`;
SELECT * FROM `paimon_trades$buckets`;
SELECT * FROM `paimon_trades$schemas`;
```

## Query Paimon Data

```sql
DESCRIBE paimon_trades;
SELECT * FROM paimon_trades LIMIT 10;
SELECT COUNT(*) FROM paimon_trades;
```

## Upsert functionality in Paimon

```bash
INSERT INTO paimon_trades VALUES ('pk-demo-1','INFY',1500,10,TIMESTAMP '2026-01-20 10:00:00');
SELECT * FROM paimon_trades WHERE trade_id = 'pk-demo-1';
INSERT INTO paimon_trades VALUES ('pk-demo-1','INFY',1550,25,TIMESTAMP '2026-01-20 10:05:00');
```

## 🔥 5. Apache Spark SQL – Iceberg Table Querying & Maintenance

This section describes how to query and manage **Apache Iceberg tables** using **Apache Spark** via:

- Spark SQL (CLI)
- Scala (Spark Shell)
- Python (Spark Submit)

It also includes **recovery steps required after restarting only the Spark container**.

### Access Spark Container

```bash
docker exec -it spark bash
```

### Query Iceberg Tables Using Python (Spark Submit)

```bash
spark-submit /opt/spark-apps/query_iceberg.py
```

### Query Iceberg Tables Using Spark SQL (SQL / Scala)

```bash
/opt/spark/bin/spark-sql   --master spark://spark:7077   --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions   --conf spark.sql.defaultCatalog=hive_catalog   --conf spark.sql.catalog.hive_catalog=org.apache.iceberg.spark.SparkCatalog   --conf spark.sql.catalog.hive_catalog.type=hive   --conf spark.sql.catalog.hive_catalog.uri=thrift://hive-metastore:9083   --conf spark.sql.catalog.hive_catalog.warehouse=s3a://lakehouse/warehouse   --conf spark.driver.extraClassPath=/opt/spark/custom-jars/*   --conf spark.executor.extraClassPath=/opt/spark/custom-jars/*
```

### Database & Table Recovery (Optional-After Spark Restart Only)

```bash
CREATE DATABASE hive_catalog.trades_db;
SHOW DATABASES IN hive_catalog;
DROP TABLE IF EXISTS hive_catalog.trades_db.iceberg_trades; # Check if the table exists first
```

### DROP TABLE IF EXISTS hive_catalog.trades_db.iceberg_trades

Use the latest metadata JSON file from MinIO:

```bash
CALL hive_catalog.system.register_table(
  table => 'trades_db.iceberg_trades',
  metadata_file => 's3a://lakehouse/warehouse/trades_db.db/iceberg_trades/metadata/00006-793232ee-64be-4eb0-b7b9-5feeaba1a067.metadata.json'
);
```

### Explore Iceberg Metadata Tables

```bash
USE hive_catalog.trades_db;

SHOW DATABASES;
SHOW TABLES;

SHOW TBLPROPERTIES iceberg_trades;
```

#### Snapshots

```bash
SELECT * FROM hive_catalog.trades_db.iceberg_trades.snapshots;

SELECT snapshot_id, parent_id, operation, committed_at, manifest_list
FROM hive_catalog.trades_db.iceberg_trades.snapshots
ORDER BY committed_at DESC;
```

#### History

```bash
SELECT * FROM hive_catalog.trades_db.iceberg_trades.history;
```

#### Manifests

```bash
SELECT * FROM hive_catalog.trades_db.iceberg_trades.manifests;
```

#### Time Travel Query

```bash
SELECT * FROM hive_catalog.trades_db.iceberg_trades VERSION AS OF 2886444592202014212;
```

#### Partitions & Files

```bash
SELECT * FROM hive_catalog.trades_db.iceberg_trades.partitions;
SELECT * FROM hive_catalog.trades_db.iceberg_trades.files;
SELECT * FROM hive_catalog.trades_db.iceberg_trades.data_files;
```

#### Describe

```bash
DESCRIBE hive_catalog.trades_db.iceberg_trades;
```

### Refresh Iceberg Metadata in Spark/Cache Invalidation

```bash
REFRESH hive_catalog.trades_db.iceberg_trades;
```

### Iceberg Compaction (COMPACTION/Rewrite Data Files) – Scala

```bash
/opt/spark/bin/spark-shell \
   --master spark://spark:7077 \
   --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
   --conf spark.sql.defaultCatalog=hive_catalog \
   --conf spark.sql.catalog.hive_catalog=org.apache.iceberg.spark.SparkCatalog \
   --conf spark.sql.catalog.hive_catalog.type=hive \
   --conf spark.sql.catalog.hive_catalog.uri=thrift://hive-metastore:9083 \
   --conf spark.sql.catalog.hive_catalog.warehouse=s3a://lakehouse/warehouse \
   --jars /opt/spark/custom-jars/iceberg-spark-runtime-3.5_2.12-1.6.0.jar
```

#### Inspect Existing Data Files

```bash
spark.sql("""SELECT file_path, record_count, file_size_in_bytes FROM hive_catalog.trades_db.iceberg_trades.files""").show(false)
```

#### Run Scala Compaction Logic

Copy and run **iceberg_rewrite.sc** on terminal

### Verify New Snapshot After Compaction

```bash
SELECT snapshot_id, operation, committed_at FROM hive_catalog.trades_db.iceberg_trades.snapshots ORDER BY committed_at DESC;
```

This should show replace as the action/operation and a new snapshot generated

### Query Paimon Tables Using Python (Spark Submit)

```bash
spark-submit /opt/spark-apps/query_paimon.py
```

### Query Paimon Tables Using Spark SQL (SQL)

```bash
/opt/spark/bin/spark-sql \
  --master spark://spark:7077 \
  --conf spark.driver.extraClassPath=/opt/spark/custom-jars/* \
  --conf spark.executor.extraClassPath=/opt/spark/custom-jars/* \
  --conf "spark.sql.extensions=org.apache.paimon.spark.extensions.PaimonSparkSessionExtensions" \
  --conf "spark.sql.catalog.paimon=org.apache.paimon.spark.SparkCatalog" \
  --conf "spark.sql.catalog.paimon.warehouse=s3a://lakehouse/paimon/warehouse" \
  --conf "spark.sql.catalog.paimon.metastore=hive" \
  --conf "spark.sql.catalog.paimon.uri=thrift://hive-metastore:9083" \
  --conf "spark.sql.catalog.hive_catalog=org.apache.iceberg.spark.SparkCatalog" \
  --conf "spark.sql.catalog.hive_catalog.type=hive" \
  --conf "spark.sql.catalog.hive_catalog.uri=thrift://hive-metastore:9083" \
  --conf "spark.sql.catalog.hive_catalog.warehouse=s3a://lakehouse/warehouse"
```

#### Explore Paimon Tables

```bash
SHOW CATALOGS;
SHOW DATABASES IN paimon;
SHOW TABLES IN paimon.trades_db;
DESCRIBE EXTENDED paimon.trades_db.paimon_trades;
```

#### Show Consistency in Paimon

```bash
SELECT * FROM paimon.trades_db.paimon_trades LIMIT 20;
SELECT * FROM  paimon.trades_db.paimon_trades WHERE trade_id = 'pk-demo-1';
```

### Query Paimon + Iceberg Tables Using Spark SQL (SQL)

```bash
/opt/spark/bin/spark-sql \
  --master spark://spark:7077 \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --conf spark.sql.defaultCatalog=hive_catalog \
  --jars /opt/spark/custom-jars/iceberg-spark-runtime-3.5_2.12-1.6.0.jar \
  --conf spark.driver.extraClassPath=/opt/spark/custom-jars/* \
  --conf spark.executor.extraClassPath=/opt/spark/custom-jars/* \
  --conf "spark.sql.extensions=org.apache.paimon.spark.extensions.PaimonSparkSessionExtensions" \
  --conf "spark.sql.catalog.paimon=org.apache.paimon.spark.SparkCatalog" \
  --conf "spark.sql.catalog.paimon.warehouse=s3a://lakehouse/paimon/warehouse" \
  --conf "spark.sql.catalog.paimon.metastore=hive" \
  --conf "spark.sql.catalog.paimon.uri=thrift://hive-metastore:9083" \
  --conf spark.sql.catalog.hive_catalog=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.hive_catalog.type=hive \
  --conf spark.sql.catalog.hive_catalog.uri=thrift://hive-metastore:9083 \
  --conf spark.sql.catalog.hive_catalog.warehouse=s3a://lakehouse/warehouse
```

## 🔥 6. Trino Iceberg Query Reference

This section documents commonly used Trino SQL queries for exploring and querying
Iceberg tables using the Trino CLI.

---

### Connect to Trino CLI

```bash
docker exec -it trino trino
```

### SQL Queries insode trino

```sql
SHOW CATALOGS;
SHOW SCHEMAS FROM iceberg;
SHOW TABLES FROM iceberg.trades_db;
```

### Basic table queries

```sql
SELECT count(*) FROM iceberg.trades_db.iceberg_trades
SELECT * FROM iceberg.trades_db.iceberg_trades LIMIT 10;
```

### Metadata Tables

```
SELECT * FROM iceberg.trades_db."iceberg_trades$snapshots";
SELECT * FROM iceberg.trades_db."iceberg_trades$files";
SELECT * FROM iceberg.trades_db."iceberg_trades$manifests";
SELECT * FROM iceberg.trades_db."iceberg_trades$partitions";
SELECT snapshot_id, parent_id, summary FROM iceberg.trades_db."iceberg_trades$snapshots" ORDER BY committed_at DESC;
```

### Timetravel Query

```sql
SELECT COUNT(*) FROM iceberg.trades_db.iceberg_trades FOR VERSION AS OF <snapshot_id>;
```

## 🦆 7. DuckDB + Iceberg - In Memory Analytics

This section demonstrates how **DuckDB** can directly query **Apache Iceberg tables stored in MinIO (S3-compatible storage)** without using Hive Metastore or any external catalog.

DuckDB acts as a **lightweight analytical query engine**, reading Iceberg metadata and Parquet files directly from object storage.

---

### 🎯 What we are checking

- DuckDB can query **Iceberg tables directly from MinIO**
- No Hive Metastore or catalog service is required
- Queries are **ACID-consistent** via Iceberg snapshots
- DuckDB always reads the **latest committed snapshot**
- No in-progress or partial files are ever read

#### Make a data directory

```bash
mkdir duckdb/data
```

#### Attach to the running DuckDB process

```bash
docker attach duckdb
```

#### Check db list

```bash
PRAGMA database_list;
```

#### Row count (latest snapshot)

```bash
SELECT count(*) FROM iceberg_scan('s3://lakehouse/warehouse/trades_db.db/iceberg_trades');
```

#### Inspect schema

```bash
DESCRIBE SELECT * FROM iceberg_scan('s3://lakehouse/warehouse/trades_db.db/iceberg_trades');
```

#### Preview data

```bash
SELECT * FROM iceberg_scan('s3://lakehouse/warehouse/trades_db.db/iceberg_trades') LIMIT 10;
```

#### Check latest snapshot

```bash
SELECT * FROM iceberg_snapshots('s3://lakehouse/warehouse/trades_db.db/iceberg_trades');
```

#### Check metadata

```bash
SELECT * FROM iceberg_metadata('s3://lakehouse/warehouse/trades_db.db/iceberg_trades');
```

#### Perform in memory analytics

```bash
SELECT
    symbol,
    COUNT(*) AS trades,
    SUM(price) AS total_value
  FROM iceberg_scan(
    's3://lakehouse/warehouse/trades_db.db/iceberg_trades'
  )
  GROUP BY symbol
  ORDER BY trades DESC;
```

#### Query a specific snapshot (snapshot ID known)

```bash
SELECT count(*)
    FROM iceberg_scan(
      's3://lakehouse/warehouse/trades_db.db/iceberg_trades',
       snapshot_from_id => 5267319272613887200
);
```

#### Read metadata files(Json)

```bash
SELECT *
  FROM read_json(
    's3://lakehouse/warehouse/trades_db.db/iceberg_trades/metadata/*.json'
);
```

#### To see all the fields

```bash
.mode line
```

To go back to default mode

```bash
.mode duckbox
```

#### Read metadata files(Avro)

```bash
SELECT *
    FROM read_avro(
      's3://lakehouse/warehouse/trades_db.db/iceberg_trades/metadata/7dee4c5e-2918-4acf-aa38-858d228c81ab-m0.avro'
);

SELECT *
    FROM read_avro(
      's3://lakehouse/warehouse/trades_db.db/iceberg_trades/metadata/snap-5267319272613887200-1-7dee4c5e-2918-4acf-aa38-858d228c81ab.avro'
);
```

#### Read data files(Parquet)

```bash
 SELECT *
    FROM read_parquet(
      's3://lakehouse/warehouse/trades_db.db/iceberg_trades/data/symbol=HDFCBANK/*'
);

SELECT *
    FROM read_parquet(
      's3://lakehouse/warehouse/trades_db.db/paimon_trades/bucket-0/*'
);
```

#### Detach safely(To Avoid Lock)

```bash
Ctrl + P, Ctrl + Q
```

## 🔥 8. Apache Superset – Trino Iceberg Integration

This section explains how to connect **Apache Superset** to **Trino** and visualize
Iceberg tables stored in the lakehouse.

---

### Overview

In this setup:

- **Trino** is used as the SQL query engine
- **Iceberg** tables are queried via Trino
- **Apache Superset** is used for analytics and visualization

Superset connects to Trino using a SQLAlchemy connection string and allows
users to build charts directly on Iceberg tables.

---

### Trino Connection Details

Superset connects to Trino using the following connection string:

```bash
trino://trino@trino:8080/iceberg/trades_db
```

#### Connection Breakdown

| Component | Value |
|--------|------|
| Engine | Trino |
| User | `trino` |
| Host | `trino` |
| Port | `8080` |
| Catalog | `iceberg` |
| Schema | `trades_db` |

---

### Create Database Connection in Superset

1. Log in to **Apache Superset UI**
2. Navigate to:  
   **Settings → Database Connections**
3. Click **+ Database**
4. Select **Trino** as the database type
5. Enter the SQLAlchemy URI: trino://trino@trino:8080/iceberg/trades_db
6. Click **Test Connection**
7. If successful, click **Connect**

### Add Iceberg Table as Dataset

1. Navigate to:  
**Data → Datasets**
2. Click **+ Dataset**
3. Choose **From database**
4. Select the Trino database connection created earlier
5. From the schema dropdown, select: trades_db
6. From the table dropdown, select: iceberg_trades
7. Click **Add**

### Create Charts

1. Navigate to: **Charts → + Chart**
2. Select: **Dataset:** `iceberg_trades`, **Visualization Type:** (Table, Bar Chart, Time-series, etc.)
3. Configure: Metrics (COUNT, SUM, AVG), Dimensions, Filters
4. Click **Run**
5. Save the chart

### Create Dashboards (Optional)

1. Navigate to: **Dashboards → + Dashboard**
2. Add saved charts
3. Arrange the layout
4. Save the dashboard
