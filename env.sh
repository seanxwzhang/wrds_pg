#!/bin/bash

export PGHOST="localhost"
export PGDATABASE="wrds"
export PGUSER="wrds"
export WRDS_ID=""
export WRDS_PASS=""

PG_ACCESS_LINE = `wrds-pgdata.wharton.upenn.edu:9737:wrds:$WRDS_ID:$WRDS_PASS`
PG_ACCESS_PATH = `~/.pgpass`
touch $PG_ACCESS_PATH
grep -qxF $PG_ACCESS_LINE $PG_ACCESS_PATH || echo $PG_ACCESS_LINE >> $PG_ACCESS_PATH

