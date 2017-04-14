#coding:utf-8
from conf import Config as C
import os, zipfile, zlib ,time, datetime, shutil, tempfile, commands

tmp_dir = "d:\\tmp\\"
def copy_file_to_tmp():
    if not os.path.exists(tmp_dir):
        os.mkdir(tmp_dir)
    source_dir = "\\\\"+C.SOURCE_IP+"\\share"
    commands.getoutput("xcopy %s %s" %(source_dir,tmp_dir))


def get_release_info():
    with C.CONNECTION.cursor() as cursor:
        sql = "SELECT * FROM web_backup_info WHERE TIME=(SELECT TIME FROM web_backup_info ORDER BY TIME DESC LIMIT 0,1)"
        cursor.execute(sql)
        result = cursor.fetchall()
    return result


def release_file(release_info):
    pass



def delete_tmp_dir():
    #删除临时目录
    shutil.rmtree(tmp_dir)
    pass


def main():
    release_info = get_release_info()
    copy_file_to_tmp()
    release_file(release_file)
    delete_tmp_dir()


if __name__ == "__main__":
    main()
