#coding:utf-8
import pymysql.cursors
class Config():
    CONNECTION = pymysql.connect(
         host='123.56.2.52',
         user='release_test',
         password='test',
         db='release',
         port=53307,
         charset='utf8mb4',
         cursorclass=pymysql.cursors.DictCursor)

    HOSTNAME = "localhost"


