#!/bin/sh

# Export all env vars for cron jobs
printenv > /etc/container.env

cron -f