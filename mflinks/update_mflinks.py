#!/usr/bin/env python3
from wrds2postgres.wrds2postgres import wrds_update

updated = wrds_update("mflink1", "mfl", force=True)
updated = wrds_update("mflink2", "mfl")
