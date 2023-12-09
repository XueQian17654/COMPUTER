function go() {
    url = "./add?name=" + encodeURIComponent($('#computer').val()) + '&val=' + encodeURIComponent($('#what').val()) + '&val3=' + encodeURIComponent($('#command').val()) + '&val5=' + encodeURIComponent($('#val5').val())
    $.get(url)
    get_()
}

function get_() {
    $.ajax({
        url: "/all", dataType: "json", success: function (data) {
            // 更新设备列表 
            var comList = $("#com");
            var selectedComputer = comList.find(".selected").attr("id");
            comList.empty();

            $.each(data[0], function (computername, status) {
                var computerHtml = `<h3 onclick="click_('${computername}')" id="${computername}" style="background-color: ${computername === selectedComputer ? "#c4c4c4" : "#fff"}" class="${computername === selectedComputer ? `selected` : ""} ${status.r ? 'online' : 'offline'}">${computername}</h3>`;
                comList.append(computerHtml);
            });

            // 更新任务和结果表格 
            var selectedComputerName = $("#computer").val();
            var renwuTable = $("#renwu_t");
            var resultTable = $("#result_t");
            renwuTable.empty();
            resultTable.empty();

            renwuTable.append('<tr><td>类型</td><td>参数1</td><td>参数2</td></tr>');
            $.each(data[1], function (computername, tasks) {
                if (computername === selectedComputerName) {
                    $.each(tasks, function (i, task) {
                        var taskHtml = `<tr><td>${task[0]}</td><td>${task[1]}</td><td>${task[2]}</td></tr>`;
                        renwuTable.append(taskHtml);
                    });
                }
            });

            resultTable.append('<tr><td>时间</td><td>任务</td><td>结果</td></tr>');
            $.each(data[2], function (computername, replies) {
                if (computername === selectedComputerName) {
                    $.each(replies, function (i, reply) {
                        var replyHtml = `<tr><td>${reply.time}</td><td>${reply.os}</td><td>${reply.result}</td></tr>`;
                        resultTable.append(replyHtml);
                    });
                    old_replies[computername] = replies
                } else if (old_replies[computername] == undefined || old_replies[computername].toString() !== replies.toString()) {
                    $("#" + computername).css("background-color", "#ffd1b2");
                }
            });
        }
    });
}

function click_(computername) {
    var selectedComputer = $("#com").find(".selected");
    if (computername == selectedComputer.prop("id")) {
        return
    }

    get_()
    $('#renwu_').hide(200)
    $('#renwu_').show(200)

    if (selectedComputer) {
        selectedComputer.css("background-color", "#fff");
        selectedComputer.removeClass("selected");
    }
    $("#" + computername).addClass("selected");
    $("#" + computername).css("background-color", "#c4c4c4");
    $("#computer").val(computername);

    // 更新任务和结果表格 
    var renwuTable = $("#renwu_t");
    var resultTable = $("#result_t");
    renwuTable.empty();
    resultTable.empty();
    var data = JSON.parse($.ajax({ url: "/all", dataType: "json", async: false }).responseText);
    $.each(data[1], function (computername, tasks) {
        if (computername === computername) {
            $.each(tasks, function (i, task) {
                var taskHtml = `<tr><td>${task[0]}</td><td>${task[1]}</td><td>${task[2]}</td></tr>`;
                renwuTable.append(taskHtml);
            });
        }
    });
    $.each(data[2], function (computername, replies) {
        if (computername === computername) {
            $.each(replies, function (i, reply) {
                var replyHtml = `<tr><td>${reply.os[0]}</td><td>${reply.result}</td><td>${reply.time}</td></tr>`;
                resultTable.append(replyHtml);
            });
        }
    });
}

function smaller() {
    if (small) {
        $('.list').show(1000)
        $("#renwu_").animate({width:'-=300px'}, 900);
        small = false;
    } else {
        $('.list').hide(800)
        setTimeout(function () {

        $("#renwu_").animate({width:'+=300px'}, 1100);
        }, 500);
        small = true;
    }
}

function size_cge() {
    if (small) {
        $("#renwu_").css('width', '100vw');
    } else {
        $("#renwu_").css('width', 'calc(100vw - 300px)');
    }
}

var small = false
var old_replies = {}

window.onresize = size_cge

$(document).ready(function () {
    get_()
    setInterval(get_, 5000);
});
