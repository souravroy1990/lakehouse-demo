FROM duckdb/duckdb:latest

# Create a persistent database location
WORKDIR /data

# Copy init SQL
COPY init.sql /init.sql

# Default command:
CMD ["duckdb", "/data/duckdb.db", "-init", "/init.sql"]