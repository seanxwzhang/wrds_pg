#!/usr/bin/env python
import logging
from wrds2postgres.wrds2postgres import wrds_update, list_accessible_tables

logger = logging.getLogger("wrds_pg")

def update_all_accessible_tables(schema):
    accessibles, _ = list_accessible_tables(schema)
    if not accessibles:
        logger.warn(f"No accessible tables in {schema}")
    else:
        logger.info(f"Updating {len(accessibles)} tables")
        for table in accessibles:
            wrds_update(table, schema)

update_all_accessible_tables("csmar")