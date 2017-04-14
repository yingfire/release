#coding:utf-8
from conf import Config as C
import os, zipfile, zlib ,time, datetime

#获取发布文件名称
def select_release_packages():
    source_dir = "d:/source"
    #判断上传目录是否存在,不存在则创建
    if not os.path.exists(source_dir):
        os.mkdir(source_dir)
    #获取发布软件信息
    package_names = os.listdir(source_dir)
    version_info_dict = {}
    for package_name in package_names:
        version = package_name.split('_')[0]
        name_info = package_name.split('_')[1].split('.')[0]
        if not version_info_dict.has_key(version):
            value_dict = {"rom":0,"wx":0,"bn":0,"service":0}
        if name_info == "rom":
            value_dict["rom"] = 1
        elif name_info == "wx":
            value_dict["wx"] = 1
        elif name_info == "bn":
            value_dict["bn"] = 1
        else:
            value_dict["service"] = 1
        version_info_dict[version] = value_dict
    return  version_info_dict
    #_----------------------------------------------------

#备份发布目录
def backup_release_dir(version_info_dict):
    global now_time
    now_time = str(int(time.time()))
    backup_dir = "d:/backups/" + now_time
    web_dir = "d:/web"
    os.chdir(web_dir)
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    #根据字典中的key值进行对应的备份
    for key in version_info_dict.keys():
        z = zipfile.ZipFile(backup_dir+'/'+key+'.zip','w',zipfile.ZIP_DEFLATED)
        for dirpath, dirname, filenames in os.walk(key):
            for filename in filenames:
                z.write(os.path.join(dirpath,filename))
        z.close()

def insert_backup_info_to_db(version_info_dict):
    for key in version_info_dict.keys():
        value = version_info_dict[key]
        with C.CONNECTION.cursor() as cursor:
            sql = "INSERT INTO `web_backup_info` (`hostname`, `VERSION`, `rom`, `wx`, `bn`, `service`, `TIME`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql,(C.HOSTNAME,key,value["rom"],value["wx"],value["bn"],value["service"],now_time))
        C.CONNECTION.commit()

def delete_more_than_30days_packages():
    #批处理每天会清除
    pass

def main():
    version_info_dict = select_release_packages()
    backup_release_dir(version_info_dict)
    insert_backup_info_to_db(version_info_dict)
if __name__ == '__main__':
    main()



