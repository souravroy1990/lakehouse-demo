# -------------------------
# FLINK CUSTOM IMAGE (Hive 3.1.3 compatible)
# Switch to this section for machine with x86 architecture (e.g. Intel/AMD)
# -------------------------
FROM flink:1.18.1-scala_2.12-java8

# Switch to root for installing system packages
USER root

# -------------------------------------------------------------------
#  Install Python and dependencies (for PyFlink, Faker, Kafka testing)
# -------------------------------------------------------------------
RUN apt-get update && apt-get install -y python3 python3-pip && \
    ln -sf /usr/bin/python3 /usr/bin/python && \
    pip install --no-cache-dir apache-flink==1.18.0 confluent_kafka faker && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch to this section for machine with ARM architecture (e.g. Apple Silicon)
# FROM flink:1.18.0-scala_2.12

# USER root

# RUN apt-get update && apt-get install -y \
#     python3 \
#     python3-pip \
#     build-essential \
#     openjdk-11-jdk \
#     wget \
#     && ln -sf /usr/bin/python3 /usr/bin/python \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# RUN export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac)))) && \
#     echo "JAVA_HOME=$JAVA_HOME" >> /etc/environment

# ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
# ENV PATH=$JAVA_HOME/bin:$PATH

# RUN pip install --no-cache-dir \
#     apache-flink==1.18.0 \
#     confluent_kafka \
#     faker

# Remains same in Windows & Mac
# -------------------------------------------------------------------
#  Environment setup
# -------------------------------------------------------------------
ENV FLINK_HOME=/opt/flink
ENV FLINK_LIB_DIR=${FLINK_HOME}/lib
ENV HADOOP_CONF_DIR=/opt/hadoop/conf
ENV HIVE_CONF_DIR=/opt/hive/conf
ENV FLINK_CLASSPATH=${FLINK_LIB_DIR}/*

# -------------------------------------------------------------------
#  Add connector + dependency jars
# -------------------------------------------------------------------

# Iceberg runtime (Flink 1.18 + Hive catalog)
ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-flink-runtime-1.18/1.6.0/iceberg-flink-runtime-1.18-1.6.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-hive-runtime/1.6.0/iceberg-hive-runtime-1.6.0.jar ${FLINK_LIB_DIR}/

# Hadoop shaded + AWS + core
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-shaded-hadoop-2-uber/2.8.3-10.0/flink-shaded-hadoop-2-uber-2.8.3-10.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-common/2.10.1/hadoop-common-2.10.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-hdfs/2.10.1/hadoop-hdfs-2.10.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-client/2.10.1/hadoop-client-2.10.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-hdfs-client/2.10.1/hadoop-hdfs-client-2.10.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/2.10.1/hadoop-aws-2.10.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.11.901/aws-java-sdk-bundle-1.11.901.jar ${FLINK_LIB_DIR}/

# Hive dependencies (3.1.3 instead of 4.0.0-beta)
ADD https://repo1.maven.org/maven2/org/apache/hive/hive-metastore/3.1.3/hive-metastore-3.1.3.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hive/hive-exec/3.1.3/hive-exec-3.1.3.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/hive/hive-common/3.1.3/hive-common-3.1.3.jar ${FLINK_LIB_DIR}/

# Calcite dependencies matching Hive 3.1.3
ADD https://repo1.maven.org/maven2/org/apache/calcite/calcite-core/1.26.0/calcite-core-1.26.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/calcite/calcite-linq4j/1.26.0/calcite-linq4j-1.26.0.jar ${FLINK_LIB_DIR}/

# Common libraries
ADD https://repo1.maven.org/maven2/com/google/guava/guava/28.2-jre/guava-28.2-jre.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/google/guava/failureaccess/1.0.1/failureaccess-1.0.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/commons-lang/commons-lang/2.6/commons-lang-2.6.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/commons/commons-lang3/3.12.0/commons-lang3-3.12.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/commons-configuration/commons-configuration/1.10/commons-configuration-1.10.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/commons-collections/commons-collections/3.2.2/commons-collections-3.2.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/commons-io/commons-io/2.11.0/commons-io-2.11.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/commons-codec/commons-codec/1.15/commons-codec-1.15.jar ${FLINK_LIB_DIR}/

# XML + Thrift + HTTP + Logging
ADD https://repo1.maven.org/maven2/com/fasterxml/woodstox/woodstox-core/6.5.1/woodstox-core-6.5.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/codehaus/woodstox/stax2-api/4.2.1/stax2-api-4.2.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/thrift/libthrift/0.14.2/libthrift-0.14.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/httpcomponents/httpclient/4.5.13/httpclient-4.5.13.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/httpcomponents/httpcore/4.4.13/httpcore-4.4.13.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/google/code/findbugs/jsr305/3.0.2/jsr305-3.0.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/google/protobuf/protobuf-java/2.5.0/protobuf-java-2.5.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-core/2.15.2/jackson-core-2.15.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-databind/2.15.2/jackson-databind-2.15.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/com/fasterxml/jackson/core/jackson-annotations/2.15.2/jackson-annotations-2.15.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/slf4j/slf4j-api/1.7.36/slf4j-api-1.7.36.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/thrift/libfb303/0.9.3/libfb303-0.9.3.jar ${FLINK_LIB_DIR}/

# Zookeeper + Curator + Netty
ADD https://repo1.maven.org/maven2/org/apache/curator/curator-framework/4.3.0/curator-framework-4.3.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/curator/curator-client/4.3.0/curator-client-4.3.0.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/zookeeper/zookeeper/3.6.3/zookeeper-3.6.3.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/io/netty/netty-all/4.1.94.Final/netty-all-4.1.94.Final.jar ${FLINK_LIB_DIR}/

# Kafka + JSON connectors
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.1.0-1.18/flink-sql-connector-kafka-3.1.0-1.18.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.1.0-1.18/flink-connector-kafka-3.1.0-1.18.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.3.2/kafka-clients-3.3.2.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/flink/flink-json/1.18.0/flink-json-1.18.0.jar ${FLINK_LIB_DIR}/

# Paimon connectors
ADD https://repo1.maven.org/maven2/org/apache/paimon/paimon-bundle/1.3.1/paimon-bundle-1.3.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/paimon/paimon-flink-1.18/1.3.1/paimon-flink-1.18-1.3.1.jar ${FLINK_LIB_DIR}/
ADD https://repo1.maven.org/maven2/org/apache/paimon/paimon-hive-connector-3.1/1.3.1/paimon-hive-connector-3.1-1.3.1.jar ${FLINK_LIB_DIR}/

# -------------------------------------------------------------------
#  Verify & cleanup
# -------------------------------------------------------------------
RUN chmod 644 ${FLINK_LIB_DIR}/*.jar && \
    ls -lh ${FLINK_LIB_DIR} | grep flink-dist

# Switch back to flink user for runtime
USER flink

WORKDIR ${FLINK_HOME}

# Default entrypoint (works for both JM/TM)
CMD ["/docker-entrypoint.sh", "jobmanager"]
