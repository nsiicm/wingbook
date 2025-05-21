#!/bin/bash
. /etc/container.env
# Set the date format
DATE=$(date +\%Y-\%m-\%d_\%H-\%M-\%S)

# Define backup filename
FILENAME="backup_$DATE.sql"
echo $POSTGRES_PASSWORD
echo $POSTGRES_USER
echo $POSTGRES_DB
echo $POSTGRES_HOST
export PGPASSWORD=$POSTGRES_PASSWORD
# Perform the backup using pg_dump
pg_dump -h "$POSTGRES_HOST" -U "$POSTGRES_USER" -d "$POSTGRES_DB" > "/backups/$FILENAME"

# Optional: compress
# gzip /backups/$FILENAME

 cd /backups || exit 1
ls -1t backup_*.sql | tail -n +31 | xargs -r rm --

echo "Backup created: $FILENAME"