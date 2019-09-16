#!/usr/bin/env python3
from sqlalchemy import create_engine
import os, sys
from wrds2postgres import wrds2postgres

wrds2postgres.wrds_update("globalvoteresults", "risk")
wrds2postgres.wrds_update("vavoteresults", "risk")
wrds2postgres.wrds_update("issrec", "risk")
