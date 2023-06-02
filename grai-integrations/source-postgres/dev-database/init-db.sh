SCRIPT_DIR=$(dirname -- "$0")/schemas
PGUSER="${POSTGRES_USER:-grai}"
PGPASSWORD="${POSTGRES_PASSWORD:-grai}"
PG_DB="${POSTGRES_DB:-grai}"
HOST="${HOST:-localhost}"
PORT="${PORT:-5433}"


for file in $(find $SCRIPT_DIR -type f -name '*.sql' | sort)
do
  echo "Executing init script $file"
  PGPASSWORD=$PGPASSWORD psql -h localhost -p $PORT -U $PGUSER -d $PG_DB  -f $file -W
done
