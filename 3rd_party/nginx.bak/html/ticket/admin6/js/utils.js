
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
