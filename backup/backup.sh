#!/bin/bash

# Environment variables
BACKUP_DIR=/backups
DB_NAME=${P_DATABASE}
DB_USER=${P_USER}
DB_PASSWORD=${P_PASSWORD}
DB_HOST=postgres_db

# Create a timestamp
TIMESTAMP=$(date +'%Y%m%d%H%M')

# Export the password so pg_dump can use it
export PGPASSWORD=${DB_PASSWORD}

# Create the backup
pg_dump -h ${DB_HOST} -U ${DB_USER} ${DB_NAME} > ${BACKUP_DIR}/${DB_NAME}_${TIMESTAMP}.sql

# Cleanup old backups (older than 7 days)
find ${BACKUP_DIR} -type f -name "*.sql" -mtime +7 -exec rm {} \;
