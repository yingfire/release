#coding:utf-8
from conf import Config as C
import os, zipfile

#获取发布文件名称
def select_release_packages():
    source_dir = "d:/source"
    #判断上传目录是否存在,不存在则创建
    if not os.path.exists(source_dir):
        os.mkdir(source_dir)
    pachage_name = os.listdir(source_dir)
    print ("获取发布文件名")
    type(pachage_name)
    print (pachage_name)
    return pachage_name
def backup_release_dir():
    pass

def main():
    select_release_packages()

if __name__ == '__main__':
    main()



