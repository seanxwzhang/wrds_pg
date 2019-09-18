#!/usr/bin/env python3
from wrds2postgres.wrds2postgres import wrds_update, run_file_sql
from wrds2postgres.wrds2postgres import make_engine, wrds_id

wrds_update("dse", "crspa")