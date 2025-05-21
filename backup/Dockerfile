# Use a lightweight Linux image with cron and Postgres client tools
FROM debian:bookworm-slim

# Install cron and PostgreSQL client
RUN apt-get update && \
    apt-get install -y cron postgresql-client && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create backup directory
RUN mkdir -p /backups

# Copy backup script and cron job definition
COPY backup.sh /usr/local/bin/backup.sh
COPY crontab.txt /etc/cron.d/db-backup
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

# Set permissions
RUN chmod +x /usr/local/bin/backup.sh && \
    chmod 0644 /etc/cron.d/db-backup && \
    chmod +x /usr/local/bin/entrypoint.sh

# Apply the cron job
RUN crontab /etc/cron.d/db-backup

# Ensure the backup directory is a volume
VOLUME ["/backups"]

# Run the cron daemon
CMD ["/usr/local/bin/entrypoint.sh"]