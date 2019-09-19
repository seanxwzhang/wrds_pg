#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "$DIR/secret.env"
export PGDATABASE="wrds"
export PGUSER="wrds"

WRDS_ACCESS_LINE="wrds-pgdata.wharton.upenn.edu:9737:wrds:$WRDS_ID:$WRDS_PASS"
PG_ACCESS_LINE="$PGHOST:$PGDATABASE:$PGUSER:$PGPASS"
PG_ACCESS_PATH="$HOME/.pgpass"
if [ -f $PG_ACCESS_PATH ] ; then 
    rm $PG_ACCESS_PATH
fi 
touch $PG_ACCESS_PATH
echo "Setting up pgacess file"
grep -qxF "wrds-pgdata.wharton.upenn.edu:9737:wrds" $PG_ACCESS_PATH || echo "$WRDS_ACCESS_LINE" >> $PG_ACCESS_PATH
grep -qxF "$PGHOST:$PGDATABASE" $PG_ACCESS_PATH || echo "$PG_ACCESS_LINE" >> $PG_ACCESS_PATH
chmod 600 $PG_ACCESS_PATH

