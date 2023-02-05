#!/usr/bin/env bash

sleep_time="${SLEEP_TIME:-30}"
script_dir=$(dirname -- "$0")

sleep $sleep_time
for file in $(find $script_dir -type f -name '*.sql' | sort)
   do
     echo "Executing init script $file"
     /opt/mssql-tools/bin/sqlcmd -U sa -P $MSSQL_SA_PASSWORD -l 30 -e -i $file
   done
