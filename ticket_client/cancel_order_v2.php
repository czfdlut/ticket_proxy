<?php

require_once("common/data.php");
require_once("common/http_request.php");
require_once("common/helper.php");

/* 订单撤单(撤单条件：未支付) */
function cancel_order_v2($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = time(); //'1550130142439';
    $cmd = '3007';
    $token = $access_token;
    $openid = '';
        
    $merchantCode = $appid;
    $merchantName = '美团';
    $bizNo = '20190224';
    $bizType = 'DPQX';
    $mobile = '18688886666';
    $orderId  = '20190224';
    $requestID = '20191224';
    
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'timestamp' => $timestamp,
        'openid' => $openid,
        'param' => array(
            'merchantCode' => $merchantCode,
            'merchantName' => $merchantName,
            'bizNo' => $bizNo,
            'bizType' => $bizType,
            'mobile' => $mobile,
            'orderId' => $orderId,
            'requestID' => $requestID
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    $post_data = make_request($content);
    $uri = "https://www.xt-kp.com/Ticket/orderCancel2.json";
    $header = array(
	    "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
	    "Accept: application/json", 
	    "Cache-Control: no-cache", 
	    "Pragma: no-cache",
    );
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

}

?>


