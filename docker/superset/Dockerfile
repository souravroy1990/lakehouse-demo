FROM apache/superset:3.0.0

USER root

# Install netcat for waiting script
RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

# Install Trino SQLAlchemy drivers
RUN pip install --no-cache-dir sqlalchemy-trino trino

USER superset
