<?php

require_once("common/http_request.php");
require_once("common/helper.php");

/* 查询余票 */
function req_order_callback()
{
    $sign = '';
    $ver = '1.0';
    $timestamp = strval(time() * 1000); //'1550130142439';
    $cmd = '9000';
    $extra_code = 'abx23579436';
       
    $appsecret = "08512be88f3ff4ee8638370e610d0259";
    $merchant_code = "12345";
    $merchant_name = "美团订票系统";
    $biz_no = "20190605123456";
    $biz_type = "DP";
    $biz_time = "2019-06-05 14:30:00";
    $order_id = "DP_20190605";
    $request_id = "REQ_20190605";
    $express_no = "20190605123456";
    $ticket_prices = "198.5";
    $ticket_pic = "http://ticket.jpg";
    $order_status = "3";
    $remark = "备注";
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'timestamp' => $timestamp,
        'param' => array(
            'appSecret' => $appsecret,
            'merchantCode' => $merchant_code,
            'merchantName' => $merchant_name,
            'bizNo' => $biz_no,
            'bizType' => $biz_type,
            'bizTime' => $biz_time,
            'orderId' => $order_id,
            'requestID' => $request_id,
            'expressNo' => $express_no,
            'ticketPrices' => $ticket_prices,
            'ticketPic' => $ticket_pic,
            'orderStatus' => $order_status,
            'remark' => $remark
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;
    
    $type = 1;
    $post_data = "";
    $header = array();
    if ($type == 1) 
    {
        //"Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
        $post_data = make_request($content);
        $header = array(
            "Content-type: application/json;charset='utf-8'", 
            "Accept: application/json", 
            "Cache-Control: no-cache", 
            "Pragma: no-cache",
            "ticket-uid: for_test"
        );

    }
    else if ($type == 2)
    {
        $tmp = "";
        make_form_request_v2($content, $tmp, $post_data);
        print_r($tmp."\n");
        print_r($post_data."\n");
        $content_type = sprintf("Content-type: %s; charset='utf-8'", $tmp); 
        $header = array(
	        $content_type,
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
            "ticket-uid: for_test",
            //"Expect: 100-continue"
        );
    }

    //$uri = "http://127.0.0.1:9002/Ticket/reqTicket.json";
    $uri = "http://test.maidaopiao.com:8080/TicketOrder/callback";
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");
    
}

req_order_callback();

?>

