#!/bin/bash

source secret.env
export PGHOST="localhost"
export PGDATABASE="wrds"
export PGUSER="wrds"

PG_ACCESS_LINE="wrds-pgdata.wharton.upenn.edu:9737:wrds:$WRDS_ID:$WRDS_PASS"
PG_ACCESS_PATH="$HOME/.pgpass"
touch $PG_ACCESS_PATH
echo "Setting up pgacess file"
grep -qxF "$PG_ACCESS_LINE" $PG_ACCESS_PATH || echo "$PG_ACCESS_LINE" >> $PG_ACCESS_PATH

