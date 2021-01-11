__import_mysql() {
echo "Running the start_mysql function."
echo "Import validation server api data from backup."
echo $MYSQL_USER
echo $MYSQL_PASSWORD
echo $MYSQL_DATABASE
mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < /scripts/validation_server_api_backup.sql
echo "Finished validation server api data from backup."
}

# Call all functions
__import_mysql
