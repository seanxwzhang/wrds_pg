#!/usr/bin/env python3

import click
import logging
import sys
import traceback
import time
from os import getenv
from importlib import import_module, reload
from common import get_wrds_engine, SafeRun
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine, reflection
from sqlalchemy.schema import Index, Table
        
LOG_FORMAT = "%(asctime)s [%(filename)s] [%(levelname)s]: %(message)s"
logging.shutdown()
reload(logging)
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('wrdscli')

@SafeRun(logger)
def _create_index(meta: MetaData, engine: Engine, table: Table, column: str):
    logger.info(f'Creating index on {table.schema}.{table.name}')
    index = Index(f'{table.name}_{column}_idx', table.columns[column])
    index.create(bind=engine)
    logger.info('Done.')


def create_single_column_indice(schema, column):
    engine = get_wrds_engine()
    meta = MetaData(schema=schema)
    logger.info(f'Reflecting DB on schema {schema}...')
    meta.reflect(bind=engine)
    insp = reflection.Inspector.from_engine(engine)
    count, success, failure, skip = 0, 0, 0, 0
    try:
        for table in meta.tables.values():
            count += 1
            indices = insp.get_indexes(table.name, schema=schema)
            idx_columns = {name for names in [index['column_names'] for index in indices] for name in names}
            if not indices or (column in table.columns.keys() and column not in idx_columns):
                if _create_index(meta, engine, table, column) == 0:
                    success += 1
                else:
                    failure += 1
            elif column not in table.columns.keys():
                logger.info(f'{schema}.{table} doesn\'t have column {column}, skipping')
                skip = 1
            elif column in idx_columns:
                logger.info(f'Index on {column} already present in {schema}.{table}, skipping')
                skip += 1
    finally:
        logger.info(f'Created {success} indices, failed {failure} tables, skipped {skip} tables, checked {count}/{len(meta.tables)}.')

if __name__ == '__main__':
    logger.setLevel(getenv("LOGLEVEL", "DEBUG"))
    create_single_column_indice('comp', 'gvkey')

