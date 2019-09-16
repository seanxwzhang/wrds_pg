#!/bin/bash

source secret.env
export PGDATABASE="wrds"
export PGUSER="wrds"

WRDS_ACCESS_LINE="wrds-pgdata.wharton.upenn.edu:9737:wrds:$WRDS_ID:$WRDS_PASS"
PG_ACCESS_LINE="$PGHOST:$PGDATABASE:$PGUSER:$PGPASS"
PG_ACCESS_PATH="$HOME/.pgpass"
touch $PG_ACCESS_PATH
echo "Setting up pgacess file"
grep -qxF "$WRDS_ACCESS_LINE" $PG_ACCESS_PATH || echo "$WRDS_ACCESS_LINE" >> $PG_ACCESS_PATH
grep -qxF "$PG_ACCESS_LINE" $PG_ACCESS_PATH || echo "$PG_ACCESS_LINE" >> $PG_ACCESS_PATH
chmod 600 $PG_ACCESS_PATH

