#coding:utf-8
from conf import Config as C
import os, zipfile, zlib ,time

now_time = str(int(time.time()))
backup_dir = "d:/backups/" + now_time

#获取发布文件名称
def select_release_packages():
    source_dir = "\\\\"+C.SOURCE_IP+"\\share"
    #判断上传目录是否存在,不存在则创建
    if not os.path.exists(source_dir):
        print ("发布目录不存在,请检测")
    #获取发布软件的名称
    package_names = os.listdir(source_dir)
    #将发布文件进行排序,负责会出现字典值混乱现象
    package_names.sort()
    version_info_dict = {}
    for package_name in package_names:
        #获取版本号
        version = package_name.split('_')[0]
        name_info = package_name.split('_')[1].split('.')[0]
        #版本号去重
        if not version_info_dict.has_key(version):
            #设置默认值(默认都没有发布)
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
    #----------------------------------------------------

#备份web目录
def backup_release_dir(version_info_dict):
    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)
    #根据字典中的key值进行对应的备份
    for key in version_info_dict.keys():
        print (key)
        service_status = version_info_dict[key]["service"]
        #判断是否有服务发布
        if service_status:
            backup_service_dir(key)
        web_dir = C.WEB_DIR
        os.chdir(web_dir)
        z = zipfile.ZipFile(backup_dir + '/' + key + '.zip', 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirname, filenames in os.walk(key):
            for filename in filenames:
                z.write(os.path.join(dirpath, filename))
        z.close()

#备份服务
def backup_service_dir(key):
    service_dir = C.SERVICE_DIR
    os.chdir(service_dir)
    #print ("有服务"+str(key))
    z = zipfile.ZipFile(backup_dir + '/' + key + '_service.zip', 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirname, filenames in os.walk("PDW.SCM.API_"+key):
        for filename in filenames:
            z.write(os.path.join(dirpath, filename))
    z.close()

#将备份信息插入数据库
def insert_backup_info_to_db(version_info_dict):
    for key in version_info_dict.keys():
        value = version_info_dict[key]
        with C.CONNECTION.cursor() as cursor:
            sql = "INSERT INTO `web_backup_info` (`hostname`, `VERSION`, `rom`, `wx`, `bn`, `service`, `TIME`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            params = (C.HOSTNAME,key,value["rom"],value["wx"],value["bn"],value["service"],now_time)
            cursor.execute(sql,params)
        C.CONNECTION.commit()

def delete_more_than_30days_packages():
    #批处理每天会清除
    pass

def main():
    #获取发布信息
    version_info_dict = select_release_packages()
    #备份文件
    backup_release_dir(version_info_dict)
    #将发布信息存储到数据库中,以便于发布脚本读取
    insert_backup_info_to_db(version_info_dict)
if __name__ == '__main__':
    main()
