#!/usr/bin/env python
"""
.. module::  django_core_utils_test.mysql_check
   :synopsis:  MySql connectivity check module.

MySql connectivity check module.  Intended to debug mysql connectivity
from local host.

For this to work:
1) Launch db container:
    docker-compose -f docker-compose-mysql.yml up -d db-mysql
2) Obtain docker machine ip:
    docker-machine ip
3) Update the configuration variables below:
   host, root_user, root_passwd, port, db_user

"""
from __future__ import print_function
import MySQLdb

# set host to output of: docker-machine ip
host = '192.168.99.100'
# set root_user to MySql root account
root_user = 'root'
# set root_passwd to root account password
root_passwd = 'rootpassword'
# set user to target user being configured
db_user = 'test_user'
port = 3306
mydb = MySQLdb.connect(host=host, user=root_user,
                       passwd=root_passwd, port=port)
cursor = mydb.cursor()

try:
    user_query = "select user, host from mysql.user;"
    results = cursor.execute(user_query)
    print("%s returned: %s" % (user_query, results))
    for index, user in enumerate(cursor):
        print("%s:%s" % (index, user))
#     print ("1. Granting of privileges returned", results)
#     granting_1 = "FLUSH PRIVILEGES;"
#     results = cursor.execute(granting_1)
#     print ("1. Granting of privileges returned", results)
#     granting_2 = "GRANT ALL PRIVILEGES ON *.* TO \
#        'test_user'@'%' WITH GRANT OPTION;"
#     results = cursor.execute(granting_2)
#     print ("2. Granting of privileges returned", results)
#     granting_3 = "FLUSH PRIVILEGES;"
#     results = cursor.execute(granting_3)
#     print ("3. Granting of privileges returned", results)


except MySQLdb.Error as ex:
    print(ex)
finally:
    cursor.close()
    mydb.close()
