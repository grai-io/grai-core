SCRIPT_DIR=$(dirname -- "$0")/schemas
PGUSER="${POSTGRES_USER}"
PGPASSWORD="${POSTGRES_PASSWORD}"
PG_DB="${POSTGRES_DB}"
HOST=localhost
PORT=5432


for file in $(find $SCRIPT_DIR -type f -name '*.sql' | sort)
do
  echo "Executing init script $file"
  PGPASSWORD=$PGPASSWORD psql -h localhost -p 5432 -U $PGUSER -d $PG_DB  -f $file -W
done
