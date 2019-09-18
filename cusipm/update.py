#!/usr/bin/env python3
from wrds2postgres.wrds2postgres import wrds_update

updated = wrds_update("issuer", "cusipm")
updated = wrds_update("issue", "cusipm")
