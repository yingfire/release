#coding:utf-8
from service_manager import ServiceManager as S
service_name = "PDW.SCM.API_v6.0"
if S(service_name).is_exists():
    print ("good")
