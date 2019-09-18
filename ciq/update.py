#!/usr/bin/env python3
from sqlalchemy import create_engine
from wrds2postgres.wrds2postgres import wrds_update, run_file_sql, make_engine
from wrds2postgres.wrds2postgres import make_engine, wrds_id

engine = make_engine()

updated = wrds_update("wrds_gvkey", "ciq", fix_missing=True)
if updated:
    engine.execute("CREATE INDEX ON ciq.wrds_gvkey (companyid)")

updated = wrds_update("wciklink_gvkey", "wrdssec")
updated = wrds_update("wciklink_names", "wrdssec")
# updated = wrds_update("wciklink_cusip", "wrdssec")

updated = wrds_update("wrds_cusip", "ciq", fix_missing=True)
if updated:
    engine.execute("CREATE INDEX ON ciq.wrds_cusip (companyid)")

updated = wrds_update("wrds_cik", "ciq", fix_missing=True)
if updated:
    engine.execute("CREATE INDEX ON ciq.wrds_cik (companyid)")

updated = wrds_update("wrds_keydev", "ciq", fix_missing=True)
if updated:
    engine.execute("CREATE INDEX ON ciq.wrds_keydev (keydeveventtypeid)")
    engine.execute("CREATE INDEX ON ciq.wrds_keydev (companyid)")

wrds_update("wrds_professional", "ciq", fix_cr=True)
wrds_update("ciqkeydeveventtype", "ciq", fix_cr=True)
wrds_update("ciqkeydevobjectroletype", "ciq", fix_cr=True)
wrds_update("ciqfininstance", "ciq")
wrds_update("ciqfinperiod", "ciq")
wrds_update("ciqgvkeyiid", "ciq")
wrds_update("ciqkeydevstatus", "ciq")
wrds_update("ciqkeydev", "ciq", fix_cr=True)
engine.dispose()
