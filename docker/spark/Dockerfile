# ==========================================
# 🏗️ Stage 1 — Builder (use local Spark tarball)
# ==========================================
FROM eclipse-temurin:8-jdk AS builder

USER root
RUN apt-get update && apt-get install -y wget tar ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp

# ✅ Use pre-downloaded Spark tarball (located in project-root/jars)
COPY ../../jars/spark-3.5.1-bin-hadoop3.tgz /tmp/spark.tgz

# Extract Spark and slim down unnecessary files
RUN echo "📦 Extracting local Spark tarball..." && \
    tar -xzf /tmp/spark.tgz && \
    mv spark-3.5.1-bin-hadoop3 /opt/spark && \
    rm -f /tmp/spark.tgz && \
    rm -rf /opt/spark/examples /opt/spark/data /opt/spark/R /opt/spark/python/test /opt/spark/kubernetes/tests && \
    echo "✅ Spark installed at /opt/spark"

# ==========================================
# 🚀 Stage 2 — Runtime (Spark + Java 8 + Iceberg + S3)
# ==========================================
FROM eclipse-temurin:8-jdk

USER root
COPY --from=builder /opt/spark /opt/spark

RUN mkdir -p /opt/spark/custom-jars

# 🧊 Iceberg 1.6 + Paimon (optional)
ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.6.0/iceberg-spark-runtime-3.5_2.12-1.6.0.jar /opt/spark/custom-jars/

# ☁️ Hadoop AWS + SDK (for S3)
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar /opt/spark/custom-jars/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar /opt/spark/custom-jars/

# Paimon Spark connector (match Paimon core version)
ADD https://repo1.maven.org/maven2/org/apache/paimon/paimon-spark-3.5/1.3.1/paimon-spark-3.5-1.3.1.jar /opt/spark/custom-jars/
ADD https://repo1.maven.org/maven2/org/apache/paimon/paimon-bundle/1.3.1/paimon-bundle-1.3.1.jar /opt/spark/custom-jars/

# Optional: any local jars
# COPY ../../jars/*.jar /opt/spark/custom-jars/

# 🌍 Environment setup
ENV JAVA_HOME=/opt/java/openjdk
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$JAVA_HOME/bin:$PATH
ENV SPARK_CLASSPATH=/opt/spark/custom-jars/*
ENV SPARK_DIST_CLASSPATH=$SPARK_HOME/jars/*:/opt/spark/custom-jars/*

RUN apt-get update && apt-get install -y python3 python3-pip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /opt/spark
CMD ["bash"]
