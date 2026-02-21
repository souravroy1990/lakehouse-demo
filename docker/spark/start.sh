#!/bin/bash
set -e

echo "🚀 Starting Spark Master..."
/opt/spark/sbin/start-master.sh --host spark --port 7077 --webui-port 8080

echo "⚙️  Starting Spark Worker..."
/opt/spark/sbin/start-worker.sh spark://spark:7077 --webui-port 8081

echo "⏳ Waiting for worker registration..."
sleep 10

echo "📡 Starting Spark ThriftServer (Hive 4 + Iceberg + S3)..."

/opt/spark/sbin/start-thriftserver.sh \
  --master spark://spark:7077 \
  --conf spark.driver.extraClassPath=/opt/spark/custom-jars/* \
  --conf spark.executor.extraClassPath=/opt/spark/custom-jars/* \
  --conf spark.sql.catalogImplementation=hive \
  --conf spark.sql.extensions=org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions \
  --conf spark.sql.catalog.hive_catalog=org.apache.iceberg.spark.SparkCatalog \
  --conf spark.sql.catalog.hive_catalog.type=hive \
  --conf spark.sql.catalog.hive_catalog.uri=thrift://hive-metastore:9083 \
  --conf spark.sql.catalog.hive_catalog.warehouse=s3a://lakehouse/warehouse \
  --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
  --conf spark.hadoop.fs.s3a.path.style.access=true \
  --conf spark.hadoop.fs.s3a.access.key=admin \
  --conf spark.hadoop.fs.s3a.secret.key=password

echo "✅ Spark 3.5.1 with Hive 4 started."
tail -f /opt/spark/logs/* 2>/dev/null || sleep infinity
