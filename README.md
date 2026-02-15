# 🧠 Modern Open Lakehouse Demo — Python + Apache Iceberg + Paimon + Flink + Spark + Kafka + Hive + Superset

Welcome to the **Zero-to-Lakehouse** project — a fully open-source, production-style real-time data lakehouse, built entirely with:

- 🐍 **Python**
- 🔥 **Apache Kafka** (stream ingestion)
- ⚡ **Apache Flink** (stream processing)
- ❄️ **Apache Iceberg** (ACID tables)
- 🪶 **Apache Paimon** (streaming-first lakehouse tables)
- 🗂 **Hive Metastore** (catalog layer)
- 🚀 **Apache Spark & Trino** (interactive SQL engines)
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

### Check fake trades streaming into Kafka:

```bash
docker logs -f docker-fake-data-producer-1
```

## 🔥 2. Kafka

### Enter the Kafka container and verify topics and messages:

```bash
docker exec -it docker-kafka-1 /bin/bash

kafka-topics --bootstrap-server localhost:9092 --list

kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic fake-data-topic \
  --from-beginning \
  --max-messages 10
```

## 🗂 3. Hive Metastore & Lake Storage Verification

### Enter the Hive Metastore container and verify that the Hadoop S3 (MinIO) filesystem is accessible:

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
```

## Query Paimon Data

```sql
DESCRIBE paimon_trades;
SELECT * FROM paimon_trades LIMIT 10;
```

## 🔥 5. Trino Iceberg Query Reference

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

## 🔥 6. Apache Superset – Trino Iceberg Integration

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