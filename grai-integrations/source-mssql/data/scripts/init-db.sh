
sleep_time="${SLEEP_TIME:-30}"

sleep $sleep_time
for file in /init/schema/*.sql
   do
     echo "Executing init script $file"
     /opt/mssql-tools/bin/sqlcmd -U sa -P $MSSQL_SA_PASSWORD -l 30 -e -i $file
   done
sleep infinity
