#!/bin/bash

SCRIPT_DIR=$(dirname -- "$0")
HOST="${DB_HOST:-localhost}"
PORT="${DB_PORT:-"1433"}"
MSSQL_SA_PASSWORD="${MSSQL_SA_PASSWORD:-"GraiGraiGr4i"}"
SERVER="tcp:$HOST,$PORT"
RETRY_LIMIT=${RETRY_LIMIT:-30}
SQL_CMD_DIR=${SQL_CMD_DIR-"/opt/mssql-tools18/bin"}


${SQL_CMD_DIR}/sqlcmd -S $SERVER -U sa -P $MSSQL_SA_PASSWORD -Q 'SELECT 1' -No -b -o /dev/null
DBSTATUS=$?

if [[ $DBSTATUS -ne 0 ]]; then
  echo "Waiting for database to become ready"
  sleep 1
fi

i=1
while [[ $DBSTATUS -ne 0 ]] && [[ $i -lt $RETRY_LIMIT ]]; do
  i=$((i + 1))

  ${SQL_CMD_DIR}/sqlcmd -S $SERVER -U sa -P $MSSQL_SA_PASSWORD -Q 'SELECT 1' -No -b -o /dev/null
  DBSTATUS=$?

  if [[ $DBSTATUS -ne 0 ]]; then
    echo "Retrying connection..."
    sleep 1
  fi

done

if [[ $DBSTATUS -ne 0 ]]; then
	echo "ERROR: SQL Server took more than $RETRY_LIMIT seconds to start up or one or more databases are not in an ONLINE state"
	exit 1
fi

echo "Database ready"
for file in $(find $SCRIPT_DIR -type f -name '*.sql' | sort)
   do
     echo "Executing init script $file"
     ${SQL_CMD_DIR}/sqlcmd -U sa -P $MSSQL_SA_PASSWORD -l 30 -e -i $file -No
   done
