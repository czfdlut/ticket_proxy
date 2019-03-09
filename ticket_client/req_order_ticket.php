<?php

require_once("common/data.php");
require_once("common/http_request.php");
require_once("common/helper.php");

/* 申请订票 */
function req_order_ticket($access_token)
{
    global $appid, $appsecret, $extra_code;
    $sign = '';
    $ver = '1.0';
    $timestamp = time(); //'1550130142439';
    $cmd = '3004';
    $token = $access_token;
    $openid = '';
    
    $merchantCode = $appid;
    $merchantName = "美团订票系统";
    $bizNo = "20190322";
    $bizType = 'DP';
    $bizName = '订票';
    $bizBrief = '用户订票';
    $bizTime = date("Y-m-d h:i:s");
    $orderNo = '0000000';
    $orderType = '0';
    $orderDate = date("Y-m-d");
    $fromStation = '西安';
    $toStation = '北京西';
    $trainCode = 'G666';
    $trainType = 'G';
    $seatType = '0';
    $tomorrow = strtotime("tomorrow");
    $startTime = "2019-03-23 13:00:00";//date("Y-m-d h:i:s", $tomorrow);
    $endTime = $startTime;
    $ticketTime = $startTime;
    $ticketType = '1';
    $noSeatFlag = 'Y';
    $ticketNum = '1';
    $idType = '1';
    $idNo = '1:440101200702060012';
    $IdName = '张三';
    $ticketPrices = '68.5';
    $couponValue = "50.0";
    $bonusFlag = '2.0';
    $serviceFee = '5.0';
    $insureFee = '3.0';
    $expressFee = '10.0';
    $payType = '1';
    $mobile = '18688886666';
    $userId = '1111';
    $address = '陕西渭南';
    $requestID = '20190322';
    $ticketObtainMode = '1';
    $officeId = '2';
    $ticketTakpePoint = '1';
    $reserved = '预留';
    $haiNum = 0;
    $allocationFlag = 'Y';
    $remark = "备注";
        
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
            'orderNo' => $orderNo,
            'orderType' => $orderType,
            'orderDate' => $orderDate,
            'fromStation' => $fromStation,
            'toStation' => $toStation,
            'trainCode' => $trainCode,
            'trainType' => $trainType,
            'seatType' => $seatType,
            'startTime' => $startTime,
            'endTime' => $endTime,
            'ticketTime' => $ticketTime,
            'ticketType' => $ticketType,
            'noSeatFlag' => $noSeatFlag,
            'ticketNum' => $ticketNum,
            'idType' => $idType,
            'idNo' => $idNo,
            'IdName' => $IdName,
            'ticketPrices' => $ticketPrices,
            'couponValue' => $couponValue,
            'bonusFlag' => $bonusFlag,
            'serviceFee' => $serviceFee,
            'insureFee' => $insureFee,
            'expressFee' => $expressFee,
            'payType' => $payType,
            'userId' => $userId,
            'address' => $address,
            'requestID' => $requestID,
            'ticketObtainMode' => $ticketObtainMode,
            'officeId' => $officeId,
            'ticketTakpePoint' => $ticketTakpePoint,
            'reserved' => $reserved,
            'haiNum' => $haiNum,
            'allocationFlag' => $allocationFlag,
            'remark' => $remark
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

    $uri = "https://www.xt-kp.com/Ticket/reqOrderTicket.json";
    //$uri = "http://127.0.0.1:80/Ticket/reqOrderTicket.json";
    //$uri = "http://test.maidaopiao.com/Ticket/reqOrderTicket.json";
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 1000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");
    
}

?>

