FROM postgres:latest

# Install cron
RUN apt-get update && apt-get install -y cron

# Add backup script and cron job file
COPY backup.sh /usr/local/bin/backup.sh
COPY cronjob /etc/cron.d/backup

# Give execution rights on the cron job and the backup script
RUN chmod 0644 /etc/cron.d/backup && chmod +x /usr/local/bin/backup.sh

# Apply cron job
RUN crontab /etc/cron.d/backup

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
