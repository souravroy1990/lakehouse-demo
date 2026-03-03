from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("QueryPaimonCatalog") \
    .config("spark.sql.extensions", "org.apache.paimon.spark.extensions.PaimonSparkSessionExtensions") \
    .config("spark.sql.catalog.paimon", "org.apache.paimon.spark.SparkCatalog") \
    .config("spark.sql.catalog.paimon.warehouse", "s3a://lakehouse/paimon/warehouse") \
    .config("spark.sql.catalog.paimon.metastore", "hive") \
    .config("spark.sql.catalog.paimon.uri", "thrift://hive-metastore:9083") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .getOrCreate()

print("\n=== DATABASES in paimon catalog ===")
spark.sql("SHOW DATABASES IN paimon").show(truncate=False)

print("\n=== TABLES in trades_db (Paimon) ===")
spark.sql("SHOW TABLES IN paimon.trades_db").show(truncate=False)

print("\n=== SAMPLE DATA FROM paimon_trades ===")
spark.sql("SELECT * FROM paimon.trades_db.paimon_trades LIMIT 10").show(truncate=False)

spark.stop()
