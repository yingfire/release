#coding:utf-8
import re,time
from conf import Config as C
class conf(object):
    def __init__(self,package_name):
        self.package_name = package_name
    def get_web_dir(self):
        version = self.package_name.split("_")[0]
        package_type = self.package_name.split("_")[1]
        regex = "v[0-9]?[6-9]{1}\.[3-9]{1}"
        reobj = re.compile(regex)
        if package_type == "service":
            web_dir = C.SERVICE_DIR + "\\\\PDW.SCM.API_" + version
        else:
            if reobj.search(version):
                web_dir = C.WEB_DIR + "\\" +version + "\\" + package_type
            else:
                if package_type == "rom":
                    web_dir = C.WEB_DIR + "\\" + version
                else:
                    web_dir = C.WEB_DIR + "\\" + version + "\\" + package_type
        return web_dir

