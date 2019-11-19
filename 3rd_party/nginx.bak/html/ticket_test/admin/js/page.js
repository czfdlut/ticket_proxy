function page(name, container, start, total) {
    if (total === 0) return;
    var pagesize = 10;
    var max = 4;
    var no_click = 'javascript:void(0)';
    var totalPage = Math.ceil(total / pagesize);
    var s = start === undefined ? 0 : +start;
    var startPage = Math.ceil(s / pagesize) + 1;
    var currentPage = startPage;
    var page = typeof container === 'string' ? $(container) : container;
    var previous_disabled = s < pagesize;
    var previous_s = (startPage - 2) * pagesize;
    var previous_href = previous_disabled ? no_click : 'report.html?n='+ name +'&s='+ previous_s +'&c='+ pagesize;
    var previous = $('<li class="paginate_button previous"><a href="'+ previous_href +'">上一页</a></li>');
    var home_href = 'report.html?n='+ name +'&s=0&c='+ pagesize;
    var home = $('<li class="paginate_button"><a href="'+ home_href +'">首页</a></li>');
    page.append(home);
    if (previous_disabled) previous.addClass('disabled');
    var next_s = startPage * pagesize;
    var next_disabled = currentPage >= totalPage;
    var next_href = next_disabled ? no_click : 'report.html?n='+ name +'&s='+ next_s +'&c='+ pagesize;
    var next = $('<li class="paginate_button next"><a href="'+ next_href +'">下一页</a></li>');
    if (next_disabled) next.addClass('disabled');
    page.append(previous);

    var pages = totalPage === 1 ? 1
        : totalPage <= max ? totalPage
        : max + 1;
    startPage = currentPage + max > totalPage ? currentPage + totalPage - (currentPage + max) : currentPage;
    startPage = startPage <= 0 ? 1 : startPage;
    var hasDot = startPage + max < totalPage;
    if (pages > 0) {
        var i = 0;
        while (i < pages){
            var nm = startPage + i;
            var n = (nm - 1) * pagesize;
            var p_href = nm === currentPage ? no_click : 'report.html?n='+ name +'&s='+ n +'&c=10';
            var p = $('<li class="paginate_button"><a href="'+ p_href +'">'+ nm +'</a></li>');
            if (nm === currentPage) p.addClass('active');
            page.append(p);
            i++;
        }
    }
    if (hasDot) {
        var dot = $('<li class="paginate_button"><a href="javascript:void(0)">…</a></li>');
        dot.addClass('disabled');
        page.append(dot);
        var lastPage = $('<li class="paginate_button"><a href="report.html?n='+ name +'&s='+ (totalPage - 1) * pagesize +'&c=10">'+ totalPage +'</a></li>');
        if (currentPage === totalPage) lastPage.addClass('active');
        page.append(lastPage);
    }
    page.append(next);
}