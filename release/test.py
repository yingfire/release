import subprocess,os,sys,commands
#service_dir = D:\\winservices
#status = subprocess.Popen('cmd.exe /C sc query PDW.SCM.API_v6.1| find "RUNNING" /c')
#status_number = status.wait()


commands.getstatusoutput('sc query PDW.SCM.API_v6.1| find "RUNNING" /c')


os.system("sc query PDW.SCM.API_v6.1| find "RUNNING" /c")

