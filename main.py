#!/usr/bin/env python

import logging
import click
import sys
import traceback
import tempfile
import time
from importlib import import_module, reload
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from os import getenv, walk, path
from wrds2postgres.wrds2postgres import wrds_update, list_accessible_tables

NON_SCHEMA_FOLDERS = {"doc", "pg", "wrdscli", "config"}
LOG_FORMAT = "%(asctime)s [%(filename)s] [%(levelname)s]: %(message)s"
logging.shutdown()
reload(logging)
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger("wrds_pg")

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            logger.info('%r  %2.2f ms' % \
                  (method.__name__, (te - ts) * 1000))
        return result
    return timed


def init(schemas):
    pg_host = getenv("PGHOST")
    pg_db = getenv("PGDATABASE")
    pg_user = getenv("PGUSER")
    pg_pass = getenv("PGPASS")

    engine = create_engine("postgresql://{}:{}@{}/{}".format(pg_user, pg_pass, pg_host, pg_db))
    
    for schema_name in schemas:
        if not engine.dialect.has_schema(engine, schema_name):
            logger.info("Creating schema {}".format(schema_name))
            engine.execute(CreateSchema(schema_name))

    logger.info("Initialization complete")

@timeit
def update_all_accessible_tables(schema, list_table, only):
    failed_updates = []
    if not only:
        accessibles, non_accessibles = list_accessible_tables(schema)
        if list_table:
            logger.info(f"Schema {schema} has {len(accessibles) + len(non_accessibles)} tables")
            logger.info(f"{accessibles + non_accessibles}")
            return failed_updates
        if not accessibles:
            logger.warn(f"No accessible tables in {schema}")
            return failed_updates
        tables2update = accessibles
    else:
        tables2update = list(only)
    logger.info(f"Updating {len(tables2update)} tables: {tables2update}")
    for table in tables2update:
        try:
            wrds_update(table, schema)
        except (KeyboardInterrupt, SystemExit):
            logger.error("user interruption, exiting")
            raise
        except:
            logger.error(f"Exception happened during updating {schema}.{table}")
            logger.error(traceback.format_exception(*(sys.exc_info())))
            failed_updates.append(f"{schema}.{table}")
    return failed_updates


@click.command()
@click.argument("targets", nargs=-1)
@click.option("-a", "--all_accessible", is_flag=True, default=False, help="Instead of following each directories' update logic, update all accessible tables in the schema")
@click.option("--list_table", is_flag=True, default=False)
@click.option("--only", multiple=True)
def main(targets, all_accessible, list_table, only):
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
            if not all_accessible and not list_table and not only:
                import_module(f"{schema}.update")
            else:
                failed_update += update_all_accessible_tables(schema, list_table, only)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            failed_update.append(schema)
            logger.error(f"Failure occured when updating {schema}")
            logger.error(traceback.format_exception(*(sys.exc_info())))
        logger.info(f"Schema {schema} updated")

    logger.warn(f"All updates finished with {len(failed_update)} failed updates: {failed_update}")

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(delete=False) as log_file:
        logger.setLevel(getenv("LOGLEVEL", "DEBUG"))
        file_handler = logging.FileHandler(log_file.name)
        file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
        logger.info(f"Saving log to file {log_file.name}")
        logger.addHandler(file_handler)
        main() # pylint: disable=no-value-for-parameter
        logger.info(f"Log saved to file {log_file.name}")
        