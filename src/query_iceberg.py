from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("QueryIcebergHiveCatalog") \
    .config("spark.sql.catalog.hive_catalog", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.hive_catalog.type", "hive") \
    .config("spark.sql.catalog.hive_catalog.uri", "thrift://hive-metastore:9083") \
    .config("spark.sql.catalog.hive_catalog.warehouse", "s3a://lakehouse/warehouse") \
    .getOrCreate()

print("\n=== DATABASES ===")
spark.sql("SHOW DATABASES IN hive_catalog").show(truncate=False)

print("\n=== TABLES in trades_db ===")
spark.sql("SHOW TABLES IN hive_catalog.trades_db").show(truncate=False)

print("\n=== SAMPLE DATA ===")
spark.sql("SELECT * FROM hive_catalog.trades_db.iceberg_trades LIMIT 10").show(truncate=False)

spark.stop()
