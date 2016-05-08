"""
.. module::  configs.common.db
   :synopsis:  Django database settings file.

Django database settings file.

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os


DB_ENGINE_SQLITE = 'sqlite'
DB_ENGINE_POSTGRES = 'postgres'
DB_ENGINE_MYSQL = 'mysql'

db_engine = os.getenv('DB_ENGINE', DB_ENGINE_SQLITE)
print('Using db_engine', db_engine)
if db_engine == DB_ENGINE_POSTGRES:
    from .postgres import *  # @UnusedWildImport
elif db_engine == DB_ENGINE_MYSQL:
    from .mysql import *  # @UnusedWildImport
else:
    from .sqlite import *  # @UnusedWildImport
