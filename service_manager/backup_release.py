#coding:utf-8
from conf import Config as C
from service_manager import ServiceManager as S
import os, zipfile, zlib ,time,shutil,re

now_time = str(int(time.time()))
backup_dir = "d:/backups/" + now_time
if not os.path.exists(backup_dir):
    os.mkdir(backup_dir)

web_dir = C.WEB_DIR
service_dir = C.SERVICE_DIR
web_cluster = C.WEB_CLUSTER
web_status = C.WEB_STATUS
tmp_dir = "d:\\tmp\\"

#获取发布文件名称
def select_release_packages():
    source_dir = "\\\\"+C.SOURCE_IP+"\\share"
    #判断上传目录是否存在,不存在则创建
    if not os.path.exists(source_dir):
        print ("release directory does not exist, please check it")
    #获取发布软件的名称
    package_names = os.listdir(source_dir)
    #print (package_names)
    version_info_dict = {"service":[],"rom":[],"wx":[],"bn":[]}
    for package_name in package_names:
        package_info_dict = {}
        release_info = ["service","rom","wx","bn"]
        for name in release_info:
            if name in package_name:
                version = package_name.split('_')[0]
                package_info_dict["package_name"] = package_name
                package_info_dict["version"] = version
                version_info_dict[name].append(package_info_dict)
    #print (version_info_dict)
    return version_info_dict


#拷贝发布文件到本地临时目录
def copy_file_to_tmp():
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    source_dir = "\\\\"+C.SOURCE_IP+"\\share"
    os.system("xcopy /q %s %s" %(source_dir,tmp_dir))

#发布web
def backup_and_release_web_dir(version_info_dict):
    for key in version_info_dict.keys():
        if key != "service" and version_info_dict[key] != []:
            web_info = version_info_dict[key]
            for web_info_dict in web_info:
                version = web_info_dict["version"]
                print (web_info_dict["package_name"])
                #如果加入6.3则在这里判断路径
                regex = "[0-9]?[6-9]{1}\.[3-9]{1}"
                reobj = re.compile(regex)
                if reobj.search(version):
                    web_dir_re = web_dir
                    rom_dir = web_dir_re + "\\" + version + "\\" + str(key)
                else:
                    web_dir_re = web_dir + "\\" + web_cluster
                    if key == "rom":
                        rom_dir = web_dir_re + "\\" + version
                    else:
                        rom_dir = web_dir_re + "\\" + version + "\\" + str(key)
                os.chdir(web_dir_re)
                z = zipfile.ZipFile(backup_dir + '/' + version + '.zip', 'w', zipfile.ZIP_DEFLATED)
                for dirpath, dirname, filenames in os.walk(version):
                    #过滤乱码文件
                    try:
                        for filename in filenames:
                            z.write(os.path.join(dirpath, filename))
                    except WindowsError,error_info:
                        pass
                        #print (error_info)
                z.close()
                tmp_release_package_name=tmp_dir + version + "_" + key + ".zip"
                f = zipfile.ZipFile(tmp_release_package_name, 'r')
                for file in f.namelist():
                    f.extract(file, rom_dir)
                change_webconfig_version(rom_dir, key)

#修改版本号
def change_webconfig_version(rom_dir,key):
    #file_name = C.WEB_DIR+"\\"+"v6.2"+"\\"+"Web.config"
    file_name = rom_dir + "\\" + "Web.config"
    re_version = "(?<=value=\")(\d+\.)+\d+\.+\d*"
    #获取版本号的对象
    old_version_obj = re.compile(re_version, re.I)
    try:
        with open(file_name,'r+') as f:
            #将配置文件存储到buffer_file当中
            buffer_file = f.read()
            f.close()
            if old_version_obj:
                old_version = re.search(old_version_obj, buffer_file).group(0)
                old_number = old_version.split(".")[2]
                new_number = int(old_number) + 1
                new_version = re.sub(old_number,str(new_number),old_version)
                print (old_version+" ==> "+new_version)
                with open(file_name,'w') as f:
                    change_version = re.sub(old_version,new_version,buffer_file)
                    f.writelines(change_version)
                    f.close
    except IOError, error_info:
        print (error_info)

#发布服务
def backup_and_release_service_dir(version_info_dict):
    service_info = version_info_dict["service"]
    for service_info_dict in service_info:
        service_name = "PDW.SCM.API_" + service_info_dict["version"]
        print (service_name)
        if S(service_name).is_exists():
            version = service_info_dict["version"]
            #备份服务
            os.chdir(service_dir)
            z = zipfile.ZipFile(backup_dir + '/' + version + '_service.zip', 'w', zipfile.ZIP_DEFLATED)
            for dirpath, dirname, filenames in os.walk("PDW.SCM.API_" + version):
                for filename in filenames:
                    z.write(os.path.join(dirpath, filename))
            z.close()
        if S(service_name).status() == "RUNNING":
            S(service_name).stop()
            # 拷贝文件
            tmp_release_package_name=tmp_dir + version + "_service.zip"
            f = zipfile.ZipFile(tmp_release_package_name, 'r')
            for file in f.namelist():
                f.extract(file, service_dir+"\\PDW.SCM.API_"+version)
            S(service_name).start()
        else:
            tmp_release_package_name=tmp_dir + version + "_service.zip"
            f = zipfile.ZipFile(tmp_release_package_name, 'r')
            for file in f.namelist():
                f.extract(file, service_dir+"\\PDW.SCM.API_"+version)

#删除发布产生的临时文件
def delete_tmp_dir():
    # 删除临时目录
    if os.path.exists(tmp_dir):
        shutil.rmtree(tmp_dir)

#主体程序
def main():
    #拷贝文件到临时目录
    delete_tmp_dir()
    copy_file_to_tmp()
    #获取发布信息
    version_info_dict = select_release_packages()
    if web_status:
        #发布web
        backup_and_release_web_dir(version_info_dict)
    else:
        #发布服务
        backup_and_release_service_dir(version_info_dict)
    #删除临时文件
    delete_tmp_dir()


if __name__ == "__main__":
    main()

