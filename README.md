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
                          └───────────┬──────────┘
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
                          └───────┬────┬──────┘
                                  │    │
                    Writes ACID   │    │ Writes Streaming
                   batch/stream   │    │ upserts/append
                        ▼    ▼
                ┌──────────────┐      ┌──────────────┐
                │   Iceberg    │      │    Paimon     │
                │  (ACID OLAP  │      │ Real-time OLAP│
                │   Tables)    │      │ Tables)        │
                └───────┬─────┘       └───────┬────────┘
                        │                    │
                        │ Metadata via Hive  │
                        ▼                    ▼
                ┌──────────────────────────────────┐
                │          Hive Metastore           │
                │   (Unified Catalog for both)      │
                └───────────────┬───────────────────┘
                                │
                                ▼
                     ┌───────────────────────────────┐
                     │   Query Layer (SQL Engines)   │
                     │   ┌───────────┐  ┌──────────┐ │
                     │   │   Spark   │  │  Trino    │ │
                     │   └───────────┘  └──────────┘ │
                     └───────────────────────┬────────┘
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
    /kafka                  → Kafka + Zookeeper
    /superset               → Superset initialization
    /minio                  → MinIO S3 bucket
/src                        → Source code
    /utils/kafka_utils.py   → PyFlink job writing to Iceberg + Paimon
    /data_generator.py      → Stream Data generator
    /flink_job.py           → Flink job
```

## 🚀 How to Run the Entire Lakehouse

```bash
cd docker
docker compose up -d
```

Wait ~30 seconds for all services to initialize.

## 📡 1. Data Generator

Check fake trades streaming into Kafka:

```bash
docker logs -f docker-fake-data-producer-1
```



