import re
regex = "[0-9]?[6-9]{1}\.[3-9]{1}"
version = "6.1"
reobj = re.compile(regex)
if reobj.search(version):
    print "1"
else:
    print "2"