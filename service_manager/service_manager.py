#coding:utf-8
import win32service,time,datetime
class ServiceManager(object):
    def __init__(self, name):
        self.name = name
        self.scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
        try:
            self.handle = win32service.OpenService(self.scm, self.name, win32service.SC_MANAGER_ALL_ACCESS)
        except Exception, error_info:
            print (error_info)

    def is_exists(self):
        statuses = win32service.EnumServicesStatus(self.scm, win32service.SERVICE_WIN32, win32service.SERVICE_STATE_ALL)
        for (short_name, desc, status) in statuses:
            if short_name == self.name:
                return True

    def start(self):
        try:
            if self.handle:
                win32service.StartService(self.handle, None)
        except Exception, erro_info:
            print (self.name ,erro_info)

    def stop(self):
        try:
            status_info = win32service.ControlService(self.handle, win32service.SERVICE_CONTROL_STOP)
        except Exception, erro_info:
            print (erro_info)
        if status_info[1] == win32service.SERVICE_STOPPED:
            print (self.name + "stop success")
        elif status_info[1] == win32service.SERVICE_STOP_PENDING:
            start_time = datetime.datetime.now()
            while True:
                if (datetime.datetime.now() - start_time).seconds > 20:
                    return (self.name + " stop long time")
                time.sleep(1)
                if win32service.QueryServiceStatus(self.handle)[1] == win32service.SERVICE_STOPPED:
                    return (self.name + "stop success")
        else:
            print (self.name + "stop failed")

    def status(self):
        try:
            status_info = win32service.QueryServiceStatus(self.handle)
            status = status_info[1]
            if status == win32service.SERVICE_STOPPED:
                return "STOPPED"
            elif status == win32service.SERVICE_START_PENDING:
                return "STARTING"
            elif status == win32service.SERVICE_STOP_PENDING:
                return "STOPPING"
            elif status == win32service.SERVICE_RUNNING:
                return "RUNNING"
        except Exception, erro_info:
            pass