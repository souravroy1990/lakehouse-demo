-- Extensions
INSTALL httpfs;
LOAD httpfs;

INSTALL iceberg;
LOAD iceberg;

INSTALL avro;
LOAD avro;

-- MinIO (S3-compatible) settings
SET s3_endpoint='minio:9000';
SET s3_access_key_id='admin';
SET s3_secret_access_key='password';
SET s3_use_ssl=false;
SET s3_url_style='path';

-- Allow Iceberg metadata version guessing (safe for demo)
SET unsafe_enable_version_guessing = true;