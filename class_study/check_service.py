import win32service,time
service_name = "PDW.SCM.API_v6.0"
scm = win32service.OpenSCManager(None, None, win32service.SC_MANAGER_ALL_ACCESS)
py_handle = win32service.OpenService(scm, service_name, win32service.SC_MANAGER_ALL_ACCESS)
status = win32service.QueryServiceStatus(py_handle)

statuses = win32service.EnumServicesStatus(scm, win32service.SERVICE_WIN32, win32service.SERVICE_STATE_ALL)
for (shortname,desc,status) in statuses:
    if shortname == service_name and status[1] == 4:
        win32service.ControlService(py_handle, win32service.SERVICE_CONTROL_STOP)
        time.sleep(5)
        win32service.StartService(py_handle, None)






