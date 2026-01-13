import org.apache.iceberg.Table
import org.apache.iceberg.spark.Spark3Util
import org.apache.iceberg.spark.actions.SparkActions

val table = Spark3Util.loadIcebergTable(spark, "hive_catalog.trades_db.iceberg_trades")

SparkActions.get(spark).rewriteDataFiles(table).execute()
