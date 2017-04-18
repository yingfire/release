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
                tmp_release_package_name = tmp_dir + str(version_info["version"]) + "_" + key + ".zip"
                #print (tmp_release_package_name)
                if key != "service":
                    rom_dir = ""
                    if key == "rom":
                        rom_dir = C.WEB_DIR + "\\" +str(version_info["version"])
                    else:
                        rom_dir = C.WEB_DIR + "\\" +str(version_info["version"]) + "\\" + str(key)
                    #解压文件
                    f = zipfile.ZipFile(tmp_release_package_name, 'r')
                    for file in f.namelist():
                        f.extract(file, rom_dir)
                    #修改版本号
                    change_webconfig_version(rom_dir,key)
                else:
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

def release_single_file(version, rom=0, wx=0, bn=0, service=0):
    #tmp_release_package_name = tmp_dir + version + "_"
    pass

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
        pass
    delete_tmp_dir()


if __name__ == "__main__":
    main()
