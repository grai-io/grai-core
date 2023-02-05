#!/bin/bash

SCRIPT_DIR=$(dirname -- "$0")

i=0
COMPLETED=0

echo "Waiting for database to become ready"
while [[ $COMPLETED -ne 1 ]] && [[ $i -lt 60 ]]; do
  i=$((i + 1))
  COMPLETED=1
	DBSTATUS=$(/opt/mssql-tools/bin/sqlcmd -h -1 -t 1 -U sa -P "$MSSQL_SA_PASSWORD")
	ERRCODE=$?

  if [[ $DBSTATUS -ne 0 ]]; then
    COMPLETED=0
  fi

  if [[ $ERRCODE -ne 0 ]]; then
    COMPLETED=0
  fi

	sleep 1
done

if [[ $COMPLETED -ne 1 ]]; then
	echo "ERROR: SQL Server took more than 60 seconds to start up or one or more databases are not in an ONLINE state"
	exit 1
fi

for file in $(find $SCRIPT_DIR -type f -name '*.sql' | sort)
   do
     echo "Executing init script $file"
     /opt/mssql-tools/bin/sqlcmd -U sa -P $MSSQL_SA_PASSWORD -l 30 -e -i $file
   done
