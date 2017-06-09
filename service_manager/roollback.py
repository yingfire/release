#coding:utf-8
import zipfile
from sys import argv
from other_conf import conf as c
from service_manager import ServiceManager as S

class roollback(object):
    def __init__(self,web_type,package_name,roollback_time):
        self.web_type = web_type
        self.package_name = package_name
        self.roollback_time = roollback_time

    #解压文件
    def unzip_file(self):
        backup_file_name = "d:\\backups\\" + self.roollback_time + "\\" + self.package_name + ".zip"
        web_dir = c(self.package_name).get_web_dir()
        print web_dir
        try:
            f = zipfile.ZipFile(backup_file_name, 'r')
            for file in f.namelist():
                f.extract(file, web_dir)
        except IOError,error_info:
            print (error_info)
    #判断参数是否一致
    def judge_parameters_are_consistent(self):
        web_types = ["wx","rom","bn"]
        if self.web_type == "service" and self.package_name.split("_")[1] == "service":
            return True
        elif self.web_type == "web" and self.package_name.split("_")[1] in web_types:
            return True
        else:
            return False



def main():
    #判断传入参数个数
    if len(argv) == 4:
        # 判断参数是否一致
        if roollback(argv[1],argv[2],argv[3]).judge_parameters_are_consistent():
            #判断是不是还原服务
            if argv[2].split("_")[1] == "service":
                service_name = "PDW.SCM.API_" + argv[2].split("_")[0]
                print service_name
                #判断服务是否安装
                if S(service_name).is_exists():
                    if S(service_name).status() == "RUNNING":
                        S(service_name).stop()
                        roollback(argv[1], argv[2], argv[3]).unzip_file()
                        S(service_name).start()
                    else:
                        roollback(argv[1], argv[2], argv[3]).unzip_file()
            else:
                roollback(argv[1], argv[2], argv[3]).unzip_file()
        else:
            print "Please enter the correct parameters"
    else:
        print "Please enter the correct parameters, such as :web v6.2_wx 20170609  or service v6.2_service 20170609"
        # roollback("web","v6.2_service","20170609").unzip_file()

if __name__ == "__main__":
    main()
