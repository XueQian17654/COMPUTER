#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#         version_added:: 1.0.0         #
from flask import *
import time
import socket
import requests

app = Flask(__name__)
app.secret_key = '...'
host = 'http://xueqian.pro:1902'
name = socket.gethostname()


# host = 'http://192.168.3.10:1902'


def RCOOC(computer, command):
    a = requests.get(host + f'/kuaisu?val=command&val3={command}&name={computer}')
    try:
        return eval(a.json()['result'])
    except:
        return a.json()['result']


def RCOOCs(computer, command, fanhui):
    a = requests.get(f'{host}/kuaisu?val=commands&val3={command}&val5={fanhui}&name={computer}')
    try:
        return eval(a.json()['result'])
    except:
        return a.json()['result']


@app.route('/')
def zy():
    if session.get('lu') is None:
        n = []
        for i in requests.get(host + '/c/computers').json():
            if i == name:
                n.append({'name': i, 'su': 'jsg', 'bz': '(此电脑)'})
            else:
                n.append({'name': i, 'su': 'jsg', 'bz': ''})
        return render_template('1.html', a=n, title={'name': '网络上的计算机', 'lu': 'Network'})
    elif session.get('name') in requests.get(host + '/c/computers').json():
        n = RCOOCs(session.get('lu').split('/')[0], '''n = []
for i in psutil.disk_partitions():
    if i.device[:1] == os.getenv("SystemDrive")[:1]:
        n.append({'name': i.device[:1], 'su': 'xtp', 'bz': ''})
    else:
        n.append({'name': i.device[:1], 'su': 'pan', 'bz': ''})''', 'n')
        return render_template('1.html', a=n, title=session)
    else:
        n = RCOOCs(session.get('lu').split('/')[0], '''n = []
for i in os.listdir("''' + session.get('lu')[len(session.get('lu').split('/')[0]) + 1:] + '''"):
    if os.path.isfile("''' + session.get('lu')[len(session.get('lu').split('/')[0]) + 1:] + '''" %2B i):
        n.append({'name': i, 'su': i.split('.')[-1], 'bz': ''})
    else:
        n.append({'name': i, 'su': 'wjj', 'bz': ''})''', 'n')
        return render_template('1.html', a=n, title=session)


@app.route('/go')
def go():
    try:
        print(session['lu'])
    except Exception as e:
        print(e)
    if request.args.get('name') in requests.get(host + '/c/computers').json():
        session['lu'] = request.args.get('name') + '/'
        session['name'] = request.args.get('name')
    elif len(session['lu'].split('/')) == 2:
        session['lu'] += request.args.get('name') + ':' + '/'
        session['name'] = request.args.get('name') + ':'
    else:
        session['lu'] += request.args.get('name') + '/'
        session['name'] = request.args.get('name')
    return redirect('/')


@app.route('/to')
def to():
    l = request.args.get('lu')
    if l == 'Network':
        session['lu'] = None
    else:
        if l[-1] != '/':
            l += '/'
        session['lu'] = l
        session['name'] = l.split('/')[-2]
    return redirect('/')


if __name__ == '__main__':
    print(" * Run's time: " + time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time())))
    app.run(host='192.168.3.10', port=1904, debug=False)
