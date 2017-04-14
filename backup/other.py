# -*- coding=utf-8 -*-
# !/usr/bin/env python

import zipfile
import StringIO

fd = open("test1.zip")
zip_data = fd.read()
fio = StringIO.StringIO(zip_data)
f = zipfile.ZipFile(file=fio)
# print filename list
print repr(f.namelist())