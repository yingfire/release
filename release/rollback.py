#coding:utf-8
from conf import Config as C
from sys import argv
import os, zipfile, zlib ,time,subprocess



#获取发布信息
def get_release_info():
    with C.CONNECTION.cursor() as cursor:
        sql = "SELECT * FROM web_backup_info WHERE TIME=(SELECT TIME FROM web_backup_info ORDER BY TIME DESC LIMIT 0,1)"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
def rollback(release_info,single_version_info):
    version_list = []
    index = 0
    #获取最后一次备份时间戳
    the_last_backup_time = release_info[1]["time"]
    backup_dir = "d:\\backups\\" + str(the_last_backup_time) + "\\"
    for version_info in release_info:
        #print version_info["version"]
        version_list.append(version_info["version"])
        #判断输入版本号是否在数据库中
        if version_list.count(single_version_info[1]) == 1:
            #判断传入参数是还原web还是service
            if len(argv) == 3 and single_version_info[2] == "service" and version_info["service"] == 1:
                #判断数据库中是否有服务的备份
                backup_file_name = backup_dir + single_version_info[1] + "_service.zip"
                rollback_dir = C.SERVICE_DIR
                #关闭服务
                service_dir = C.SERVICE_DIR + "\\PDW.SCM.API_" + single_version_info[1]
                print (service_dir)
                #覆盖文件
                status = subprocess.Popen('cmd.exe /C sc query PDW.SCM.API_' + single_version_info[1] + '| find "RUNNING" /c')
                # status为0,则服务未启动或不存在
                status_number = status.wait()
                if not status_number:
                    stop = subprocess.Popen("cmd.exe /C sc stop PDW.SCM.API_" + single_version_info[1])
                    stop.wait()
                    time.sleep(5)
                    f = zipfile.ZipFile(backup_file_name, 'r')
                    for file in f.namelist():
                        f.extract(file, rollback_dir)
                    start = subprocess.Popen("cmd.exe /C sc start PDW.SCM.API_" + single_version_info[1])
                    start.wait()
                #启动服务
                else:
                    print ("PDW.SCM.API_" + single_version_info[1] + "The service is not started, or is not installed, please follow the specific idc operation")
                break
            elif len(argv) == 2:
                backup_file_name = backup_dir + single_version_info[1] + ".zip"
                rollback_dir = C.WEB_DIR
                f = zipfile.ZipFile(backup_file_name, 'r')
                for file in f.namelist():
                    f.extract(file, rollback_dir)
                print (backup_file_name)
                break
        else:
            index += 1
    if index >= len(release_info):
        print ("No info is logged in the database,Please check the input information!!!")

def main():
    release_info = get_release_info()
    #get_release_info()
    if len(argv) == 1:
        print ('''Please enter the version or service which you want to restore.
    such as: 
        python rollback.py v6.1 
        or
        python rollback.py v6.1 service''')
    else:
        rollback(release_info,argv)


if __name__ == "__main__":
    main()