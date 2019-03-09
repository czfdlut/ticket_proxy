<?php

require_once("common/data.php");
require_once("common/http_request.php");
require_once("common/helper.php");

/* 订单查询 */
function query_ticket_result($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = '1551432535'; //time(); 
    $cmd = '3006';
    $token = $access_token;
    $openid = '';
    
    $merchantCode = $appid;
    $merchantName = '美团';
    $bizNo = '20190224';
    $bizType = 'DP';
    $bizName = '订票查询';
    $bizBrief = '用户订票';
    $bizTime = '2019-03-01 17:45:10'; //date('Y-m-d H:i:s');
    $orderDate = '2019-03-01';//date('Y-m-d');
    $mobile = '18688886666';
    $orderStatus = '9';
    $startBizTime = '2019-03-01 18:10:10'; //date('Y-m-d');
    $endBizTime = '2019-03-01 20:10:10'; //date('Y-m-d');
    $pageIndex = 0;
    $pageSize = 100;
    $requestID = '20190224';
    
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'timestamp' => $timestamp,
        'openid' => $openid,
        'param' => array(
            'appid' => $appid,
            'secret' => $appsecret,
            'merchantCode' => $merchantCode,
            'merchantName' => $merchantName,
            'bizNo' => $bizNo,
            'bizType' => $bizType,
            'bizName' => $bizName,
            'bizBrief' => $bizBrief,
            'bizTime' => $bizTime,
            'orderDate' => $orderDate,
            'mobile' => $mobile,
            'orderStatus' => $orderStatus,
            'startBizTime' => $startBizTime,
            'endBizTime' => $endBizTime,
            'pageIndex' => $pageIndex,
            'pageSize' => $pageSize,
            'requestID' => $requestID
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    //$uri = "https://www.xt-kp.com/Ticket/queryTicketResult.json";
    //$uri = "http://127.0.0.1:8080/Ticket/queryTicketResult.json";
    $uri = "http://test.maidaopiao.com/Ticket/queryTicketResult.json";

    /* 方法1 */
    $type = 1;
    if ($type == 1) 
    {
        $post_data = make_request($content);
        $header = array(
	        "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
        );
    }
    else if ($type == 2) {
        $post_data = make_form_request($content);
        $header = array(
	        "Content-type: multipart/form-data; charset='utf-8'", 
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
        );
    }
    else if ($type == 3)
    {
        $tmp = "";
        $post_data = "";
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
        );
    }
    //print_r($post_data);
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

}

?>

