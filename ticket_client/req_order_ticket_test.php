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
    $timestamp = '1559548103316';//strval(time() * 1000); //'1550130142439';
    $cmd = '3004';
    $token = $access_token;
    $openid = '23ED8BDB61B06DDA97EE2AC461FE6C1E';
    
    $merchantCode = "12345";
    $merchantName = "美团";
    $bizNo = "20190602";
    $bizType = 'DP';
    $bizName = '订票';
    $bizBrief = '订票';
    $bizTime = "2019-06-02 22:30:00"; //date("Y-m-d h:i:s");
    $orderNo = '1559450224387_16645';
    $orderType = 'DP'; //test
    $orderDate = "2019-06-02";//date("Y-m-d");
    $fromStation = '西安';
    $toStation = '北京西';
    $trainCode = 'G666';
    $trainType = 'A';
    $seatType = '1';
    $tomorrow = strtotime("tomorrow");
    $startTime = "2019-06-02 22:30:00";//strval(date("Y-m-d h:i:s", $tomorrow)); //"2019-04-21 13:00:00"
    $endTime = $startTime;
    $ticketTime = $startTime;
    $ticketType = '1';
    $noSeatFlag = 'Y';
    $ticketNum = '1';
    $idType = '1';
    $idNo = '1:440101200702060012';
    $IdName = '陈志丰';
    $ticketPrices = '68.5';
    $couponValue = "50.0";
    $bonusFlag = '2.0';
    $serviceFee = '5.0';
    $insureFee = '3.0';
    $expressFee = '10.0';
    $payType = '0';
    $mobile = '18600477264';
    $userId = '1';
    $address = '北京';
    $requestID = '1559450224387_16645';//strval(date("Ymdhis"));
    $ticketObtainMode = '1';
    $officeId = '1';
    $ticketTakpePoint = '1';
    $reserved = '1';
    $haiNum = '0';
    $allocationFlag = 'Y';
    $remark = "";
        
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
            'bizName' => $bizName,
            'bizBrief' => $bizBrief,
            'bizTime' => $bizTime,
            'orderNo' => $orderNo,
            'orderType' => $orderType,
            'orderDate' => $orderDate,
            'fromStation' => $fromStation,
            'toStation' => $toStation,
            'tranCode' => $trainCode,
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
            'mobile' => $mobile,
            'userId' => $userId,
            'address' => $address,
            'requestID' => $requestID,
            'ticketObtainMode' => $ticketObtainMode,
            'officeId' => $officeId,
            'ticketTakePoint' => $ticketTakpePoint,
            'reserved' => $reserved,
            'haiNum' => $haiNum,
            'allocationFlag' => $allocationFlag,
            'remark' => $remark,
            'appid' => $appid,
            'secret' => $appsecret,
            'totalPrices' => $ticketPrices,
            'trainCode' => $trainCode
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
        $content_type = sprintf("Content-Type: %s; charset='utf-8'", $tmp); 
        $header = array(
	        $content_type,
	        "Accept: */*", 
	        "Cache-Control: no-cache", 
	        "Pragma: no-cache",
            "ticket-uid: for_test",
            "Expect:"
        );
    }
	//"Accept: application/json", 
    //"Expect: 100-continue"
    $uri = "https://www.xt-kp.com/Ticket/reqOrderTicket.json";
    //$uri = "http://test.maidaopiao.com/Ticket/reqOrderTicket.json";
    $ret_data = "";
    $errcode = request_xiti($header, $uri, $post_data, 2000, 2, $ret_data);
    print_r("ec=".$errcode."\n");
    print_r("ret=".$ret_data."\n");
    
}

$token = "9fd42d25e764acb17451c9c981860c97";
req_order_ticket($token);

?>

