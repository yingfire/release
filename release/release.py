#coding:utf-8
from conf import Config as C
from sys import argv
import os, zipfile, zlib , shutil, re ,subprocess,commands

tmp_dir = "d:\\tmp\\"
service_dir = C.SERVICE_DIR
#拷贝发布文件到本地临时目录
def copy_file_to_tmp():
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    source_dir = "\\\\"+C.SOURCE_IP+"\\share"
    os.system("xcopy /q %s %s" %(source_dir,tmp_dir))


#从数据库获取具体需要发布的信息
def get_release_info():
    with C.CONNECTION.cursor() as cursor:
        sql = "SELECT * FROM web_backup_info WHERE TIME=(SELECT TIME FROM web_backup_info ORDER BY TIME DESC LIMIT 0,1)"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

#发布所有的版本
def release_all_file(release_info):
    for version_info in release_info:
        print "------------" + str(version_info["version"]) + "--------------"
        for key in version_info.keys():
            if version_info[key] == 1:  #1为True
                version = str(version_info["version"])
                tmp_release_package_name = tmp_dir + version + "_" + key + ".zip"
                #print (tmp_release_package_name)
                if key != "service":
                    rom_dir = ""
                    if key == "rom":
                        rom_dir = C.WEB_DIR + "\\" +version
                    else:
                        rom_dir = C.WEB_DIR + "\\" +version + "\\" + str(key)
                    #解压文件
                    f = zipfile.ZipFile(tmp_release_package_name, 'r')
                    for file in f.namelist():
                        f.extract(file, rom_dir)
                    #修改版本号
                    change_webconfig_version(rom_dir,key)
                else:
                    release_service(version,key)
                    pass

#修改版本号
def change_webconfig_version(rom_dir,key):
    #file_name = C.WEB_DIR+"\\"+"v6.2"+"\\"+"Web.config"
    file_name = rom_dir + "\\" + "Web.config"
    re_version = "(?<=value=\")(\d+\.)+\d+\.+\d*"
    #获取版本号的对象
    old_version_obj = re.compile(re_version, re.I)
    with open(file_name,'r+') as f:
        #将配置文件存储到buffer_file当中
        buffer_file = f.read()
        f.close()
        if old_version_obj:
            old_version = re.search(old_version_obj, buffer_file).group(0)
            old_number = old_version.split(".")[2]
            new_number = int(old_number) + 1
            new_version = re.sub(old_number,str(new_number),old_version)
            print (key)
            print (old_version+" ==> "+new_version)
            with open(file_name,'w') as f:
                change_version = re.sub(old_version,new_version,buffer_file)
                f.writelines(change_version)
                f.close


def release_single_file(release_info,single_version_info):
    print (single_version_info[1])
    #版本标识信息,1为数据库中有记录
    status = 1
    flag = 0
    for version_info in release_info:
        #print (version_info)
        if flag == 1:
            break
        #判断输入版本是否记录在数据库中
        if single_version_info[1] in version_info.values():
            for key in version_info.keys():
                #判断输入的参数,是否在数据库中记录
                if version_info[key] == 1 and key in single_version_info:
                    version = str(version_info["version"])
                    tmp_release_package_name = tmp_dir + version + "_" + key + ".zip"
                    if key != "service":
                        rom_dir = ""
                        if key == "rom":
                            rom_dir = C.WEB_DIR + "\\" + version
                        else:
                            rom_dir = C.WEB_DIR + "\\" + version + "\\" + str(key)
                        # 解压文件
                        f = zipfile.ZipFile(tmp_release_package_name, 'r')
                        for file in f.namelist():
                            f.extract(file, rom_dir)
                        # 修改版本号
                        change_webconfig_version(rom_dir, key)
                        status = 1
                    else:
                        #服务的发布方法
                        release_service(version,key)
                        status = 1
                        flag = 1
                        break
                    print "-------------------------"
        else:
            status = 0
    if status == 0:
        print("No info is logged in the database,Please check the input information!!!")

def release_service(version,key):
    service_dir = C.SERVICE_DIR + "\\PDW.SCM.API_"+ version
    print ("release directory" + C.SERVICE_DIR +"\\PDW.SCM.API_"+ version)
    status = subprocess.Popen('cmd.exe /C sc query PDW.SCM.API_'+version+'| find "RUNNING" /c')
    #status为0,则服务未启动或不存在
    status_number = status.wait()
    if not status_number:
        stop = subprocess.Popen("cmd.exe /C sc stop PDW.SCM.API_" + version)
        stop.wait()
        tmp_release_package_name = tmp_dir + version + "_" + key + ".zip"
        f = zipfile.ZipFile(tmp_release_package_name, 'r')
        for file in f.namelist():
            f.extract(file, service_dir)
        start = subprocess.Popen("cmd.exe /C sc start PDW.SCM.API_" + version)
        start.wait()
    else:
        if os.path.exists(service_dir):
            print ("PDW.SCM.API_" + version + "The service is not started, or is not installed, please follow the specific idc operation")


#删除发布产生的临时文件
def delete_tmp_dir():
    #删除临时目录
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

#程序主体
def main():
    #防止上次中断脚本,产生的临时目录影响本次执行
    delete_tmp_dir()
    #获取数据库中发布信息
    release_info = get_release_info()
    #拷贝文件到临时目录
    copy_file_to_tmp()
    #判断是否有参数传入
    if len(argv) == 1:
        #没有参数,执行全部发布
        release_all_file(release_info)
    else:
        #有参数根据参数执行对应软件包发布
        release_single_file(release_info,argv)
    print "--------Release is complete--------"


if __name__ == "__main__":
    main()
