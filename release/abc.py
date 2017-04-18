from conf import Config as C
import re
import sys
# def change_webconfig_version():
#     file_name = C.WEB_DIR+"\\"+"v6.2"+"\\"+"Web.config"
#
#     re_version = "(?<=value=\")(\d+\.)+\d+\.+\d*"
#     old_version_obj = re.compile(re_version, re.I)
#     with open(file_name,'r+') as f:
#         buffer_file = f.read()
#         f.close()
#         if old_version_obj:
#             old_version = re.search(old_version_obj, buffer_file).group(0)
#             old_number = old_version.split(".")[2]
#             new_number = int(old_number) + 1
#             new_version = re.sub(old_number,str(new_number),old_version)
#             print (old_version+" ==> "+new_version)
#             with open(file_name,'w') as f:
#                 change_version = re.sub(old_version,new_version,buffer_file)
#                 f.writelines(change_version)
#                 f.close
#change_webconfig_version()
def release_single_file(single_version_info):
    #tmp_release_package_name = tmp_dir + version + "_"
    print (single_version_info[1])



release_single_file(sys.argv)
