<?php

require_once("common/data.php");
require_once("common/http_request.php");
require_once("common/helper.php");

/* 查询余票 */
function req_ticket($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = time(); //'1550130142439';
    $cmd = '4000';
    $token = $access_token;
    $openid = '';
    
    $merchant_code = $appid;
    $merchant_name = "美团订票系统";
    $train_id = "G101";
    $start_station_id = 'beijing-01';
    $arrival_station_id = 'shanghai-01';
       
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
            'merchant_code' => $merchant_code,
            'merchant_name' => $merchant_name,
            'train_id' => $train_id,
            'start_station_id' => $start_station_id,
            'arrival_station_id' => $arrival_station_id
        )
    );
    
    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;
    
    $type = 2;
    $post_data = "";
    $header = array();
    if ($type == 1) 
    {
        $post_data = make_request($content);
        $header = array(
            "Content-type: application/x-www-form-urlencoded;charset='utf-8'", 
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
    $uri = "http://test.maidaopiao.com/Ticket/reqTicket.json";
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");
    
}

?>

