#!/bin/bash

SCRIPT_DIR=$(dirname -- "$0")
HOST="${DB_HOST:-localhost}"
PORT="${DB_PORT:-"1433"}"
MSSQL_SA_PASSWORD="${MSSQL_SA_PASSWORD:-"GraiGraiGr4i"}"
SERVER="tcp:$HOST,$PORT"
i=0
COMPLETED=0

echo "Waiting for database to become ready"
while [[ $COMPLETED -ne 1 ]] && [[ $i -lt 30 ]]; do
  i=$((i + 1))
  COMPLETED=1
	#DBSTATUS=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa -P "$MSSQL_SA_PASSWORD" -S "$SERVER")
  DBSTATUS=$(/opt/mssql-tools/bin/sqlcmd -S localhost,1433 -U sa -P $MSSQL_SA_PASSWORD -Q 'select 1' -b -o /dev/null)
  if [[ $DBSTATUS -ne 0 ]]; then
    COMPLETED=0
  else
    echo "Retrying connection..."
    sleep 1
  fi

done

if [[ $COMPLETED -ne 1 ]]; then
	echo "ERROR: SQL Server took more than 60 seconds to start up or one or more databases are not in an ONLINE state"
	exit 1
fi
echo "Database ready"

for file in $(find . -type f -name '*.sql' | sort)
   do
     echo "Executing init script $file"
     /opt/mssql-tools/bin/sqlcmd -U sa -P $MSSQL_SA_PASSWORD -l 30 -e -i $file -S "$SERVER"
   done
