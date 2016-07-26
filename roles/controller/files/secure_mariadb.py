#!/usr/bin/env python2
import socket
import pymysql

import argparse

parser = argparse.ArgumentParser(description='Do everything that mysql_secure_installation does, but then better.')
parser.add_argument('-p', '--password', dest='password', help='Password for root. 1: change it to this. 2: use this if previous pw does not work.')
parser.add_argument('-o', '--oldpassword', dest='oldpassword', help='Previous password for root.', default='')

parser.add_argument('-s', '--socket', dest='socket', help='Socket file to use.', default='/var/lib/mysql/mysql.sock')
args = parser.parse_args()

try:
    conn = pymysql.connect(user='root', passwd=args.oldpassword, db='mysql', unix_socket=args.socket)
    print('Using oldpassword')
except:
    conn = pymysql.connect(user='root', passwd=args.password, db='mysql', unix_socket='/var/lib/mysql/mysql.sock')
    print('Using password')

print('open cursos')
c=conn.cursor()

print('update password')
c.execute("UPDATE mysql.user SET Password = PASSWORD('{0}') WHERE User = 'root'".format(args.password))

print("find user ''")
c.execute("select host from mysql.user where user = ''")
hosts=c.fetchall()
hosts=[ r[0] for r in hosts ]

for h in [socket.gethostname(), 'localhost']:
    print("check ''@'{0}'".format(h))
    if h in hosts:
        print("clean ''@'{0}'".format(h))
        c.execute("DROP USER ''@'{0}'".format(h))

print("find databases")
c.execute("SHOW DATABASES")
DBs=c.fetchall()
DBs=[ r[0] for r in DBs ]

print("check database test")
if 'test' in DBs:
    print("drop database test")
    c.execute("DROP DATABASE test")

print("flush privs")
c.execute("FLUSH PRIVILEGES")

print("done")
