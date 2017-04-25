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
    SOURCE_IP = "139.199.211.70"
    WEB_DIR = "D:\\websites\\vpchn.rom.paidui.com\\h1"
    SERVICE_DIR = "D:\\winservices"


