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

    HOSTNAME = "ali_hd_service01"
    SOURCE_IP = "10.20.1.2"
    WEB_DIR = "D:\\websites\\vpchd.rom.paidui.com\\h1"
    SERVICE_DIR = "D:\\winservices"


