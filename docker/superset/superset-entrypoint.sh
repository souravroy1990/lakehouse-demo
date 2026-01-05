#!/bin/bash
set -e

superset db upgrade
superset fab create-admin \
    --username admin \
    --firstname Superset \
    --lastname User \
    --email admin@superset.com \
    --password admin

superset init

exec gunicorn --bind 0.0.0.0:8088 "superset.app:create_app()"