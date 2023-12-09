var coms = {}
$.get('./all', function (data, status) {
    for (const i in data[0]) {
        coms[i] = { 'renwu': data[1][i], 'result': data[2][i] }
    }
})
_get()
setInterval(_get, 1000)

// coms_old = {}
function _get(a__) {
    $.get('./all', function (data, status) {
        // console.log(data[1])
        computers = data[0]
        a = ''
        for (const i in computers) {
            try {
                if (coms[i]['renwu'].toString() == data[1][i].toString()) {
                    z = ''
                } else {
                    z = 'color:#00fffe;'
                    if (i == $('#computer').val()) {
                        coms[i]['renwu'] = data[1][i]
                    }
                }
            } catch (err) {
                coms[i] = { 'renwu': data[1][i], 'result': [] }
                // coms_old[i] = {'renwu': data[1][i], 'result': []}
                z = 'color:#00fffe;'
            }

            if (coms[i]['result'].toString() == data[2][i].toString()) {
                ax = ''
            } else {
                // console.log(coms[i]['result'])
                // console.log(data[2][i])
                // console.log(coms[i]['result'] == data[2][i])
                ax = 'color:#00fffe;'
                if (i == $('#computer').val()) {
                    coms[i]['result'] = data[2][i]
                }
            }


            if (computers[i]['r']) {
                x = ''
            } else {
                x = ' （不在线）'
            }
            if ($('#computer').val() == i) {
                y = ` style="background:#f60;"`
            } else {
                y = ` style="${z}${ax}"`
            }
            a += `<h3${y} onclick="click_('${i}')">${i}${x}</h3>`
        }
        $('#com').html(a)
        if (i == $('#computer').val()) {
            upd()
        }
    })
}


function upd() {
    name = $('#computer').val()
    renwu_t = '<tr><td>任务</td></tr>'
    for (i of coms[name]['renwu']) {
        renwu_t += `<tr><td>${i}</td></tr>`
    }

    result_t = '<tr><td>时间</td><td>任务</td><td>结果</td></tr>'
    for (i of coms[name]['result']) {
        result_t += `<tr><td>${i['time']}</td><td>${i['os']}</td><td>${i['result']}</td></tr>`
    }

    $('#renwu_t').html(renwu_t)
    $('#result_t').html(result_t)
}

function click_(name) {
    $('#computer').val(name)
    _get(1)
    $('#renwu_').show()
    upd()
}
