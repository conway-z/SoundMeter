import os
import pymysql
import sys


# class readbi:
#     name = None
#     age = None
#     def __init__(self, user, pwd):
#         self.name = user
#         self.pwd = pwd

def read_mysql_bi(dbname):
    host = ''
    user = ''
    pwd = ''
    if dbname == "local":
        host = '127.0.0.1'
        user = 'root'
        pwd = 'shuqin'
    if dbname == "bisyn":
        host = '192.168.253.250'
        user = 'bigdata'
        pwd = 'w8ijjqOiy0C'
    if dbname == "bidev":
        host = '192.168.253.181'
        user = 'bigdata'
        pwd = 'dataqin.com'

    config = {
              'host':host,
              'port':3306,
              'user':user,
              'password':pwd,
              'db':'bi',
              'charset':'utf8mb4',
              'cursorclass':pymysql.cursors.DictCursor,
              }
    return config

def a():
    print("I am a")