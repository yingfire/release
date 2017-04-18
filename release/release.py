#coding:utf-8
from conf import Config as C
from sys import argv
import os, zipfile, zlib , shutil, re

tmp_dir = "d:\\tmp\\"
#拷贝发布文件到本地临时目录
def copy_file_to_tmp():
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    source_dir = "\\\\"+C.SOURCE_IP+"\\share"
    os.system("xcopy  %s %s" %(source_dir,tmp_dir))

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
                    release_service(version)
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

def release_service (version):
    print ("服务发布暂未使用")
    print ("发布目录"+C.SERVICE_DIR+version)
    pass

def release_single_file(release_info,single_version_info):
    print (single_version_info[1])
    #版本标识信息,1为数据库中有记录
    status = 1

    for version_info in release_info:
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
                    else:
                        #服务的发布方法
                        release_service(version)
                        pass
                    print "-------------------------"
            status = 1
        else:
            status = 0
    if not status:
        print("No info is logged in the database,Please check the input information!!!")

#删除发布产生的临时文件
def delete_tmp_dir():
    #删除临时目录
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

#程序主体
def main():
    #防止上次中断脚本,产生的临时目录影响本次执行
    delete_tmp_dir()
    release_info = get_release_info()
    copy_file_to_tmp()
    if len(argv) == 1:
        release_all_file(release_info)
    else:
        release_single_file(release_info,argv)
    delete_tmp_dir()


if __name__ == "__main__":
    main()
