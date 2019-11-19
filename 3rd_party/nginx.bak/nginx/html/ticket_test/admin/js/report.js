// 页面加载完成
$(function () {
    setList(null, true, '加载中');
    var args = getQueryStringArgs();
    var name = args.n;
    var start = args.s;
    var pagesize = args.p;
    get_report(name, start, pagesize);
    $('.nav-item').removeClass('nav-item__actived');
    $('.nav-item[name="' + name + '"]').addClass('nav-item__actived');
});

function get_report(table, start, pagesize) {
    var settings = getSetting({
        method: 'GET',
        url: '/Ticket/report.json?table='+ table +'&start='+ (start || 0) +'&pagesize='+ (pagesize || 10),
    });
    return $.ajax(settings)
        .done(function (res) {
            showTip(res);
            if (res.total) {
                setList(res, false, '');
                page(table, '.pagination', start, res.total);
            }
            return res;
        })
        .catch(function(e) {
            showTip(e);
        });
}

function setList(res, isEmpty, msg) {
    var data = isEmpty ? {
        total: 0,
        marks: [],
        values: []
    } : res;
    var reportList = $('#reportList');
    var list = data.values;
    var marks = data.marks;
    var size = marks.length;
    if (size) {
        var thead = ['<tr>'];
        var i = 0;
        while(i < size) {
            thead.push('<th>'+ marks[i] +'</th>');
            i++;
        }
        thead.push('</tr>');
        reportList.find('thead').html(thead.join(''));
    }

    var total = list.length;
    var j = 0;
    var tbody = [];
    if (total > 0) {
        while(j < total) {
            var item = list[j];
            tbody.push('<tr>');
            var z = 0;
            while(z < size) {
                tbody.push('<td>'+item[z]+'</td>');
                z++;
            }
            tbody.push('</tr>');
            j++;
        }
    } else {
        tbody.push('<tr>');
        tbody.push('<td style="line-height:50px;text-align:center;background:#fff;">'+ msg +'</td>');
        tbody.push('</tr>');
    }
    reportList.find('tbody').html(tbody.join(''));
}