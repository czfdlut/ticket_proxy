
<?php

require_once("common/data.php");
require_once("common/http_request.php");
require_once("common/helper.php");

/* 获得token */
function get_access_token()
{
    global $appid, $appsecret, $extra_code;
    $cmd = '1001';
    $openid = '';
    $timestamp = time(); //'1550130142439';
    $token = '';
    $ver = '1.0';
    $sign = '';
        
    $content = array(
        'sign' => $sign,
        'ver' => $ver,
        'command' => $cmd,
        'token' => $token,
        'param' => array(
            'appid' => $appid,
            'secret' => $appsecret
        ),
        'timestamp' => $timestamp,
        'openid' => $openid
    );
    //display($content);

    $sign = create_sign($content, $extra_code);
    $content['sign'] = $sign;

    //display($content);

    $post_data = json_encode($content);
    //print_r($post_data);
    $uri = "https://test.maidaopiao.com/base/doAction";
    $header = array(
	    "Content-type: application/json;charset='utf-8'", 
	    "Accept: application/json", 
	    "Cache-Control: no-cache", 
	    "Pragma: no-cache", 
    );
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");

    $ret_array = json_decode($ret_data, true);
    //print_r($ret_array);
    return $ret_array['data']['token'];
}


?>


