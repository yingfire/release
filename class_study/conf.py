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
    SOURCE_IP = "139.199.211.70"
    WEB_DIR = "D:\\websites\\vpchd.rom.paidui.com"
    WEB_CLUSTER = "h1"
    SERVICE_DIR = "D:\\winservices"
    #当服务器为web时为True,service时为False
    #WEB_STATUS = True
    WEB_STATUS = False

