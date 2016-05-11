#!/usr/bin/env python
"""
.. module::  django_core_utils_test.mysql_init
   :synopsis:  MySql initialization module.

MySql initialization module.

"""
from __future__ import print_function
import os
import getopt
import sys
import MySQLdb


db_host = None
root_user = os.environ.get('MYSQL_ROOT_USER', 'root')
passwd = os.environ['MYSQL_ROOT_PASSWORD']
user = os.environ.get('MYSQL_USER', 'test_user')


def _usage():
    print('%s -h -d <db host>' % sys.argv[0])


def _args_error(exit_code=1):
    _usage()
    sys.exit(exit_code)


try:
    opts, args = getopt.getopt(sys.argv[1:], "hd:", ["help", "db_host="])
except getopt.GetoptError:
    _args_error()


for opt, arg in opts:
    if opt == "-h":
        _args_error(0)
    elif opt in ("-d", "--db_host"):
        db_host = arg

if not db_host:
    _args_error()

conn = MySQLdb.connect(host=db_host, user=root_user, passwd=passwd)
cursor = conn.cursor()


flush_query = "FLUSH PRIVILEGES;"
_grant = "GRANT ALL PRIVILEGES ON *.* TO '{}'@'%' WITH GRANT OPTION;"
grant_query = _grant.format(user)
user_query = "select user, host from mysql.user;"


def _exec_query(db_cursor, db_query, verbose=True):
    results = db_cursor.execute(db_query)
    if verbose:
        print("%s returned: %s" % (db_query, results))

try:

    _exec_query(cursor, user_query)
    for item in cursor:
        print(item)

    for query in flush_query, grant_query, flush_query:
        _exec_query(cursor, query)


except MySQLdb.Error as ex:
    print(ex)
finally:
    cursor.close()
    conn.close()
