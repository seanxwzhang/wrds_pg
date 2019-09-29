#!/usr/bin/env python

import yaml
import traceback
import sys
from os import path, walk
from sqlalchemy import create_engine

def load_config():
    '''
    Load all configs (merge if key overlaps) into a dict
    '''
    script_path = path.abspath(__file__)
    config_path = path.realpath(path.join(script_path, '../../config'))
    res = {}
    for root, _, configs in walk(config_path):
        for config in configs:
            with open(path.join(root, config)) as f:
                res.update(yaml.safe_load(f))
    return res

def get_wrds_engine():
    config = load_config()
    user = config['PGUSER']
    pw = config['PGPASS']
    host = config['PGHOST']
    db = config['PGDATABASE']
    return create_engine(f'postgresql://{user}:{pw}@{host}/{db}')

class SafeRun(object):

    def __init__(self, logger):
        self.logger = logger

    def __call__(self, func, *args, **kwargs):
        def func_wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return 0
            except (KeyboardInterrupt, SystemExit):
                self.logger.error('Exiting')
                raise
            except:
                self.logger.error(f"Exception happened during safe run")
                self.logger.error(traceback.format_exception(*(sys.exc_info())))
                return 1
        return func_wrapper