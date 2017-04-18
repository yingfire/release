# b_site.py
# coding=utf-8
# -----------------------------------------------------------------------
# Copyright (C)， 2015 PAIDUI.COM
# 脚本名:      b_site.py
# 脚本用途:    备份站点文件和发布，剔除log、logs文件夹和 .log、.logs结尾的日志文件
# 脚本位置:    /u1/scripts/
# 脚本修改历史:
#  <作者>      <日期>       <版本 >    <描述>
#  黄起        16/02/25       1.0      新建
# 版权: GPL
# -----------------------------------------------------------------------
# 要预先安装curl.exe验证文件
#
# 定义时间、目录变量
import os
import sys
import shutil
import time
import zipfile
import re

# 定义时间，目录变量
today = time.strftime('%Y%m%d%H%M', time.localtime())
for i in range(1, len(sys.argv)):
    site_name = pool_name = sys.argv[i].lower()
    if os.path.exists(r'D:\websites\rom.paidui.com'):
        source_dir = "D:/websites/rom.paidui.com/h1/" + site_name + '/'
    if os.path.exists(r'D:\websites\sz.rom.paidui.com'):
        source_dir = "D:/websites/sz.rom.paidui.com/h1/" + site_name + '/'
    target_dir = "d:/backup/" + site_name

    # 备份文件
    if not os.path.exists(r'd:\backup'):
        os.mkdir(r'd:\backup')
    if not os.path.exists(source_dir):
        print "Directory %s not found!!!" % (source_dir)
        continue
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir, ignore=shutil.ignore_patterns('*.txt', '*.log'))
    # 压缩备份文件
    f = zipfile.ZipFile(target_dir + "_" + today + ".zip", 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(target_dir):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename))
    f.close()

    # 需发布的站点文件
    desktop_dir = r'C:/Users/Administrator/Desktop'
    rar_path = desktop_dir + '/' + site_name
    if not os.path.exists(rar_path):
        print "WebFile %s  not found!!!" % (rar_path)
        continue
    to_folder = desktop_dir + '/' + site_name + '/'

    # 新发布站点文件覆盖原程序文件
    for src_dir, dirs, files in os.walk(to_folder):
        dst_dir = src_dir.replace(to_folder, source_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)

            # 等待更新version
            #    print u"请更新版本号"
            #    os.system("pause")
            # 更新version
    ver = re.compile("(?<=value=\")(\d+\.)+\d+", re.I)
    f = open(source_dir + "/Web.config", 'r+')
    alllines = f.read()
    f.close()
    i = re.search(ver, alllines)
    if i:
        print "Old Version:" + i.group(0)
        j = i.group(0).split('.')
        k = int(j[-1]) + 1
        #将group中的old_number 替换为新的number
        m = re.sub(j[-1] + "(?!\.)", str(k), i.group(0))
        print "New Version:" + m
        #将文件中的oldversion替换为新的version
        f = open(source_dir + "/Web.config", 'w')
        str = re.sub(i.group(0), m, alllines)
        f.writelines(str)
        f.close()

    # 重启IIS service
    cmd_iis = [r'"C:\Windows\System32\iisreset"']
    cmd_iis.append(r'/restart')
    os.popen(' '.join(cmd_iis))

    # 删除临时文件夹
    if re.search('/', site_name):
        p_dir = site_name.split('/')[0]
        del_dir = desktop_dir + '/' + p_dir + '/'
    else:
        del_dir = to_folder
    shutil.rmtree(del_dir)
    shutil.rmtree(target_dir)
