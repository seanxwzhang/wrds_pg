#!/usr/bin/env python

import logging
import click
import sys
import traceback
from importlib import import_module
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from os import getenv, walk, path

NON_SCHEMA_FOLDERS = {"doc", "pg"}
logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger("wrds_pg")

def init(schemas):
    pg_host = getenv("PGHOST")
    pg_db = getenv("PGDATABASE")
    pg_user = getenv("PGUSER")
    pg_pass = getenv("PGPASS")
    logger.setLevel(getenv("LOGLEVEL", "DEBUG"))

    engine = create_engine("postgresql://{}:{}@{}/{}".format(pg_user, pg_pass, pg_host, pg_db))
    
    for schema_name in schemas:
        if not engine.dialect.has_schema(engine, schema_name):
            logger.info("Creating schema {}".format(schema_name))
            engine.execute(CreateSchema(schema_name))

    logger.info("Initialization complete")

@click.command()
@click.argument("targets", nargs=-1)
def main(targets):
    dirnames = [dirname for dirname in next(walk('.'))[1] if not dirname.startswith('.') and dirname not in NON_SCHEMA_FOLDERS]
    schemas = [schema for schema in dirnames if path.isfile(f"{schema}/update.py")]
    init(schemas)
    failed_update, target_schemas = [], []
    if len(targets) == 0:
        target_schemas = schemas
    else:
        for target in targets:
            if target in schemas:
                target_schemas.append(target)
            else:
                logger.error(f"Unsupported WRDS schema {target}")
                raise Exception(f"Unsupported WRDS schema {target}")
    logger.info(f"Schemas to be updated: {target_schemas}")
    for schema in target_schemas:
        logger.info(f"Updating schema {schema}")
        try:
            import_module(f"{schema}.update")
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            failed_update.append(schema)
            logger.info(f"Failure occured when updating {schema}")
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
        logger.info(f"Schema {schema} updated")

    logger.info("")

if __name__ == "__main__":
    main() # pylint: disable=no-value-for-parameter