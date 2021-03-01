#!/bin/bash
# Database backup script for validation server api DB
# Purpose: Call DB backup script to save current DB contents to backup file
# Command: ./backup.sh
#

echo "-----------------------------------------------------"
echo "Starting backup:  $(date)"
echo "-----------------------------------------------------"
SECONDS=0

# Create DB Backup
echo "-----------------------------------------------------"
echo "Export database"
echo "-----------------------------------------------------"
docker exec -i -t db_server bash ./scripts/export_mysql_backup.sh


minutes=$((SECONDS/60))
seconds=$((SECONDS%60))

echo "-----------------------------------------------------"
echo "Ending backup:  $(date)"
echo "Backup took $minutes minutes and $seconds seconds."
echo "-----------------------------------------------------"
