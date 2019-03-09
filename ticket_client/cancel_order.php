<?php

require_once("common/data.php");
require_once("common/http_request.php");
require_once("common/helper.php");

/* 订单退单(退单条件：已支付&未出票) */
function cancel_order($access_token)
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
    $bizNo = '20190302';
    $bizType = 'DPQX';
    $mobile = '18688886666';
    $orderId  = '0000000'; //20190302';
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

    $type = 2;
    $header = array();
    $post_data = "";
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
    else if ($type == 2)
    {
        $tmp = "";
        make_form_request_v2($content, $tmp, $post_data);
        $content_type = sprintf("Content-type: %s; charset='utf-8'", $tmp); 
        $header = array(
	        $content_type,
            "ticket-uid: for_test",
	        "Accept: application/json", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
        );
    }
 
    $ret_data = "";
    $uri = "https://www.xt-kp.com/Ticket/orderCancel.json";
    #$uri = "http://127.0.0.1:8080/Ticket/orderCancel.json";
    //$uri = "http://test.maidaopiao.com/Ticket/orderCancel.json";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

}

?>

