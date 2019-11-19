
// 格式化时间
function formatTime(time, fmt) {
    if (!time) return time;
    const datetime = parse2Date(time);
    var o = {
        'M+': datetime.getMonth() + 1, // 月份
        'd+': datetime.getDate(), // 日
        'h+': datetime.getHours(), // 小时
        'm+': datetime.getMinutes(), // 分
        's+': datetime.getSeconds(), // 秒
        'q+': Math.floor((datetime.getMonth() + 3) / 3), // 季度
        'S': datetime.getMilliseconds() // 毫秒
    };
    if (/(y+)/.test(fmt)) {
        const regMatch = RegExp.$1;
        const year = (datetime.getFullYear() + '').substr(4 - regMatch.length);
        fmt = fmt.replace(regMatch, year);
    }
    for (var k in o) {
        if (new RegExp('(' + k + ')').test(fmt)) {
            const regMatch = RegExp.$1;
            const num = o[k];
            const doubleNum = ('00' + num).substr(('' + num).length);
            const regVal = (regMatch.length === 1) ? num : doubleNum;
            fmt = fmt.replace(regMatch, regVal);
        }
    }

    return fmt;
}

// 转换为日期
function parse2Date(time) {
    if (time instanceof Date) return time;
    if (time === undefined) return new Date();
    const str = typeof time === 'number' ? time
        : !isNaN(+time) ? +time
            : String(time).replace(/(\d+)-(\d+)-(\d+)(\s+|T)/g, '$1/$2/$3 ');
    return new Date(str);
}

function getQueryStringArgs() {
    var qs = (location.search.length > 0 ? location.search.substring(1) : "");
    var args = {};
    var items = qs.length ? qs.split("&") : [];
    var item = null;
    var name = null;
    var value = null;
    var len = items.length;
    for (var i = 0; i < len; i++) {
        item = items[i].split("=");
        name = decodeURIComponent(item[0]);
        value = decodeURIComponent(item[1]);
        if (name.length) {
            args[name] = value;
        }
    }
    return args;
}

function html_decode(str) {
    var s = "";
    if (str.length == 0) return "";
    s = str.replace(/>/g, "&gt;");
    s = s.replace(/</g, "&lt;");
    s = s.replace(/ /g, " ");
    s = s.replace(/'/g, "\'");
    s = s.replace(/"/g, "\"");
    s = s.replace(/<br>/g, "\n");
    return s;
}
    
function showTip(res) {
    clearTimeout(window.__TIP);
    var tit = '';
    var msg = '';
    if (res.statusText) {
        tit = res.status;
        msg = html_decode(res.responseText);
    }

    if (res && res.errcode && res.errcode !== 0) {
        msg = html_decode(res.errmsg);
    }
    if (msg) {
        $('.toast').html('<h2>'+tit+'</h2>'+'<p>'+msg+'</p>').show();
        window.__TIP = setTimeout(function() {
            $('.toast').hide();
        }, 5000);
    }
}

function getSetting(option) {
    var setting =  {
        "async": true,
        "crossDomain": true,
        "method": "POST",
        "headers": {
            "Content-Type": "application/json",
            "cache-control": "no-cache",
        },
        "processData": false,
        "contentType": false,
        "dataType": "json",
        "mimeType": "multipart/form-data"
    };
    return Object.assign(setting, option);
}
