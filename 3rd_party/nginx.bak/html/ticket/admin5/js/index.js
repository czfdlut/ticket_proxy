// var domain = 'http://test.maidaopiao.com:8080';
var domain = '';

// 订单列表字段
var orderFieldsName = {
    orderType: '订单类型',
    ticketPrices: '票价',
    trainType: '列车类型',
    paynotifystatus: '支付回调结果',
    userPhone: '联系电话',
    getTicketNum: '取票张数',
    expressFee: '快递费',
    idNo: '乘客证件上传序号',
    bizBrief: '业务摘要',
    merchantName: '商户名称',
    payType: '支付类型',
    idName: '乘客姓名',
    bizName: '业务名称',
    officeId: '出票窗口ID',
    ticketNum: '客票数量',
    payquerystatus: '支付结果查询',
    paynofifycontent: '支付回调结果',
    serviceFee: '服务费数量',
    bizNo: '业务流水编号',
    merchantCode: '商户系统编号',
    idType: '乘客证件类型',
    orderNo: '订单流水号',
    outTicketNum: '出票张数',
    payquerycontent: '支付结果查询',
    haiNum: '孩票张数',
    fromStation: '业务日期',
    fromStation: '乘车站',
    insureFee: '保险费',
    bizType: '业务类型',
    paychecked: '支付是否一致',
    ticketObtainMode: '出票方式',
    ticketObtainMode: 1,
    totalPrices: "总票价",
    insureFeeNum: '乘意险数量',
    orderStatus: '订单状态',
    remark: '备注',
    trainCode: '站车次',
    expressFeeNum: '快递车票张数',
    disstatus: '出票状态',
    seatType: '席位类型',
    requestId: '请求流水号',
    startTime: '乘车发车时间',
    ticketTakePoint: '取票点ID',
    flowId: '处理流水Id',
    serviceFeeNum: '服务费数量',
    noSeatFlag: '接受无座',
    refundPrices: '已退金额',
    ticketType: '票种',
    userId: '会员ID',
    couponValue: '优惠卷',
    toStation: '到站',
    ticketTime: '乘车日期',
    bonusFlag: '积分兑换',
    endTime: '乘车到站时间',
    outStatus: '出票状态'
}

// 显示的表头字段
var thFields = [
    'orderNo',
    'orderType',
    'ticketPrices',
    'trainType',
    'paynotifystatus',
    'userPhone',
    'getTicketNum'
]

function setStore(name, obj) {
    window.localStorage.setItem(name, obj);
}

function getStore(name) {
    var objStr = window.localStorage.getItem(name);
    return objStr ? JSON.parse(objStr) : {};
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
    var tit = '';
    var msg = '';
    if (res.statusText) {
        tit = res.status;
        msg = html_decode(res.responseText);
    }

    if (res && res.errcode && res.errcode !== 0) {
        tit = res.errmsg;
        msg = html_decode(JSON.stringify(res.data));
    }
    $('.toast').html('<h2>'+tit+'</h2>'+'<p>'+msg+'</p>').show();
    setTimeout(function() {
        $('.toast').hide();
    }, 5000);
}

// 页面加载完成
$(function () {

    // 初始默认值
    var todayTime = formatTime(new Date(), 'yyyy-MM-dd');
    $('input[name="bizTime"], input[name="orderDate"]').val(todayTime);
    var requestID = new Date().getTime() + '_' + Math.ceil(Math.random() * 100000);
    $('input[name="requestID"], input[name="orderNo"]').val(requestID);
    $('input[name="bizNo"]').val('DP_' + requestID);

    // 日期组件
    $(".datepicker").datepicker({
        dateFormat: 'yy-mm-dd',
        beforeShow: function (input) {
            $(input).css({
                "position": "relative",
                "z-index": 999999
            });
        }
    });

    // 关闭弹窗
    $('.pop-close, .close').on('click', function () {
        $(this).parents('.pop-box').hide();
        $('.pop-bg').hide();
    });

    // 显示表单弹窗
    $('.tool .btn').on('click', function () {
        $('.datepicker').css({'z-index':0});
        var id = $(this).attr('id').replace(/\-btn/, '');
        var pop = $('#' + id + "-pop");
        pop.show();
        if (pop.get(0)) {
            $('.pop-bg').show();
        }
        var inputs = pop.find('form input');
        var input_num = inputs.length;
        var action = pop.find('.btn-primary').attr('data-action');
        var oldData = getStore(action);
        for(var i = 0; i < input_num; i++) {
            var input = inputs[i];
            if (oldData[input.name] !== undefined &&  oldData[input.name] !== 'undefined') {
                input.value = oldData[input.name];
            }
        }
    });

    function readfile(name, file, callback) {
        var reader = new FileReader();
        reader.readAsDataURL(file.files[0]);
        reader.onloadend = function(){
            callback(name, reader.result);
        }
    }

    // 弹窗提交 
    $(".btn-submit").on('click', function () {
        var action = $(this).attr('data-action');
        if (typeof window[action] === 'function') {
            var form = $(this).parents('.pop-box').find('form');
            var formData = form.serializeArray();
            var obj = {}
            formData.forEach(function (d) {
                obj[d.name] = d.value
            });
            var files = form.find('input[type="file"]');
            var files_num = files.length;
            var f = 0;
            for(var i = 0; i < files_num; i++) {
                var file = files[i];
                if (file.files[0]) {
                    readfile(file.name, file, function(name, result){
                        obj[name] = result;
                        f++;
                        if (f === files_num) {
                            var objData = JSON.stringify(obj);
                            setStore(action, objData);
                            window[action](objData);
                        }
                    });
                } else {
                    obj[file.name] = null;
                    f++;
                    if (f === files_num) {
                        var objData = JSON.stringify(obj);
                        setStore(action, objData);
                        window[action](objData);
                    }
                }
            }
            if (files_num === 0) {
                var objData = JSON.stringify(obj);
                setStore(action, objData);
                window[action](objData);
            }
        }
    });

    // 查询订单列表
    getTicket();
    $('.btn-getTicket').on('click', function() {
        getTicket();
    });
});

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
        "mimeType": "multipart/form-data"
    };
    return Object.assign(option, setting);
}

// 订票接口
function getTicket() {
    setList(null, true, '加载中');

    var formData = $('#getTicket-form').serializeArray();
    var obj = {}
    formData.forEach(function (d) {
        obj[d.name] = d.value
    });
    var settings = getSetting({
        url: domain + "/Ticket/queryTicketResult.json",
        data: JSON.stringify(obj)
    });
    return $.ajax(settings)
        .done(function (res) {
            if (res.data && Array.isArray(res.data.orderList)) {
                setList(res, false, '');
            } else {
                setList(null, true, '无数据');
            }
            showTip(res);
        })
        .catch(function(e) {
            showTip(e);
            setList(null, true, '无数据');
        });
}

// 更新订单列表数据
function setList(orderData, isEmpty, msg) {
    var data = isEmpty ? {
        data: {
            total: 0,
            orderList: []
        }
    } : orderData;
    var orderList = $('#orderList');
    var thead = ['<tr>'];
    var list = data.data.orderList;
    var size = thFields.length;
    var i = 0;
    while(i < size) {
        var name = orderFieldsName[thFields[i]] || thFields[i];
        thead.push('<th>'+ name +'</th>');
        i++;
    }
    thead.push('</tr>');
    orderList.find('thead').html(thead.join(''));

    var total = data.data.total;
    var j = 0;
    var tbody = [];
    if (total > 0) {
        while(j < total) {
            tbody.push('<tr>');
            var z = 0;
            while(z < size) {
                tbody.push('<td>'+list[j][thFields[z]]+'</td>');
                z++;
            }
            tbody.push('</tr>');
            j++;
        }
    } else {
        tbody.push('<tr>');
        tbody.push('<td style="line-height:50px;text-align:center;background:#fff;" colspan='+ thFields.length +'>'+ msg +'</td>');
        tbody.push('</tr>');
    }
    orderList.find('tbody').html(tbody.join(''));
}

// 申请订票
function reqTicket(formData) {
    var settings = getSetting({
        url: domain + "/Ticket/reqOrderTicket.json",
        data: formData
    });
    return $.ajax(settings)
        .done(function (res) {
            showTip(res);
            return res;
        })
        .catch(function(e) {
            showTip(e);
        });
}

// 上传乘车人身份证
function ticketUploadIdImg(formData) {
    var settings = getSetting({
        url: domain + "/Ticket/uploadIdImg.json",
        data: formData
    });
    return $.ajax(settings)
        .done(function (res) {
            showTip(res);
            return res;
        })
        .catch(function(e) {
            showTip(e);
        });
}

// 订单退单
function orderCancel(formData) {
    var settings = getSetting({
        url: domain + "/Ticket/orderCancel.json",
        data: formData
    });
    return $.ajax(settings)
        .done(function (res) {
            showTip(res);
            return res;
        })
        .catch(function(e) {
            showTip(e);
        });
}