__export_mysql() {
echo "Running the export_mysql function."

echo "Export tax calculator data to backup."

# mysqldump -u$MYSQL_USER -p$MYSQL_PASSWORD tpc_tax_calculator inputs_basecase_tpc inputs_tpc InVarsCB_tpc simlaws_tpc tpc_helpterms > ./WebApp/scripts/tpc_tax_calculator_backup.sql
mysqldump -uroot -proot  --all-databases > ./scripts/validation_server_api_backup.sql

echo "Finished exporting tax calculator data to backup."

}

# Call all functions
__export_mysql
