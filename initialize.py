#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from os import getenv
import logging

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("wrds_pg")

pg_host = getenv("PGHOST")
pg_db = getenv("PGDATABASE")
pg_user = getenv("PGUSER")
pg_pass = getenv("PGPASS")
logger.setLevel(getenv("LOGLEVEL", "DEBUG"))

engine = create_engine("postgresql://{}:{}@{}/{}".format(pg_user, pg_pass, pg_host, pg_db))

schemas = ["audit", "crsp", "crspa", "dealscan", "ibes", "rpna", "tfn", "comp"]

for schema_name in schemas:
    if not engine.dialect.has_schema(engine, schema_name):
        logger.info("Creating schema {}".format(schema_name))
        engine.execute(CreateSchema(schema_name))

logger.info("Initialization complete")