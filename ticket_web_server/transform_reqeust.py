# -*- coding: utf-8 -*
from util import request_query, add_headers, get_time_stamp13
from ticket_util import get_access_token, create_sign, make_form_request_v2, join_token_command
import tornado.web
from datetime import datetime
import json
import urllib

class TransformRequestHandler(tornado.web.RequestHandler):
    @property
    def ticket_token(self):
        return self.application.ticket_token
    
    @property
    def logger(self):
        return self.application.logger
    
    @property
    def redis_client(self):
        return self.application.redis_client
       
    def set_response_header(self, headers):
        for k, v in headers.items():
            self.set_header(k, v)

    def finish_err_msg(self, msg):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()
   
    @tornado.gen.coroutine
    def http_request_server(self, headers, body):         
        url = "http://test.maidaopiao.com" +  self.request.path
        return request_query(url, headers=headers, data=body.encode(encoding='UTF8'), timeout=10)
   
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()

        self.logger.debug("request.body=%s" % self.request.body)
        try:
            data = json.loads(self.request.body) 
        except Exception as e:
            self.finish_err_msg(str(e))
            self.logger.error(str(e))
            return
        
        """
        data = {
            "appid": "14324152292",
            "secret": "59a69169ff81415dfc30ac652353f69f",
            "merchantCode": "14324152292",
            "merchantName": "美团订票系统",
            "bizNo": "20190401",
            "bizType": "DP",
            "bizName": "订票",
            "bizBrief": "用户订票",
            "bizTime": "2019-06-02 04:12:26",
            "orderNo": "0000000",
            "orderType": "0",
            "orderDate": "2019-06-02",
            "fromStation": "西安",
            "toStation": "北京西",
            "trainCode": "G666",
            "trainType": "G",
            "seatType": "0",
            "startTime": "2019-04-21 13:00:00",
            "endTime": "2019-04-21 13:00:00",
            "ticketTime": "2019-04-21 13:00:00",
            "ticketType": "1",
            "noSeatFlag": "Y",
            "ticketNum": "1",
            "idType": "1",
            "idNo": "1:440101200702060012",
            "IdName": "张三1",
            "ticketPrices": "68.5",
            "couponValue": "50.0",
            "bonusFlag": "2.0",
            "serviceFee": "5.0",
            "insureFee": "3.0",
            "expressFee": "10.0",
            "payType": "1",
            "userId": "1111",
            "address": "陕西渭南",
            "requestID": "20190401",
            "ticketObtainMode": "1",
            "officeId": "2",
            "ticketTakpePoint": "1",
            "reserved": "预留",
            "haiNum": 0,
            "allocationFlag": "Y",
            "remark": "备注"
        } 
        """

        extra_code = self.ticket_token["extra_code"]
        ticket_uid = self.ticket_token["ticket_uid"]
        appid = self.ticket_token["appid"]
        appsecret = self.ticket_token["appsecret"]

        key = "access_token_%s" % ticket_uid
        access_token = self.redis_client.get(key)
        ##for test
        dt = join_token_command(appid, appsecret)
        access_token = get_access_token(ticket_uid, dt, extra_code)
        self.logger.info("redis_access_token=%s" % access_token)

        is_new_token = False
        if access_token is None:
            is_new_token = True
            dt = join_token_command(appid, appsecret)
            access_token = get_access_token(ticket_uid, dt, extra_code)
        
        if access_token is None:
            self.logger.info(r"验证失败: access_token=%s" % access_token)
            self.finish_err_msg(r"验证失败")
            return
        
        if is_new_token == True:
            self.redis_client.set(key, access_token)
            self.redis_client.expire(key, 3600)
            self.logger.info("update access_token:%s" % key)
              
        data["appid"] = appid
        data["secret"] = appsecret
        data["bizNo"] = "20190602"
        data["bizTime"] = "2019-06-02 22:30:00"
        data["startTime"] = "2019-06-02 22:30:00"
        data["endTime"] = data["startTime"]
        data["ticketTime"] = data["startTime"]
        data["idNo"] = "1:440101200702060012"
        data["ticketPrices"] = "68.5"
        data["totalPrices"] = data["ticketPrices"]
        data["couponValue"] = "50.0"
        data["bonusFlag"] = "2.0"
        data["serviceFee"] = "5.0"
        data["insureFee"] = "3.0"
        data["expressFee"] = "10.0"
        data["ticketObtainMode"] = "1"
        data["trainCode"] = data["tranCode"]
        
        #data2 = {"appid":"14324152292","secret":"59a69169ff81415dfc30ac652353f69f","merchantCode":"14324152292","merchantName":"美团订票系统","bizNo":"20190401","bizType":"DP","bizName":"订票","bizBrief":"用户订票","bizTime":"2019-06-02 02:53:43","orderNo":"0000000","orderType":"0","orderDate":"2019-06-02","fromStation":"西安","toStation":"北京西","trainCode":"G666","trainType":"G","seatType":"0","startTime":"2019-06-03 12:00:00","endTime":"2019-06-03 12:00:00","ticketTime":"2019-06-03 12:00:00","ticketType":"1","noSeatFlag":"Y","ticketNum":"1","idType":"1","idNo":"1:440101200702060012","IdName":"张三","ticketPrices":"68.5","totalPrices":"68.5","couponValue":"50.0","bonusFlag":"2.0","serviceFee":"5.0","insureFee":"3.0","expressFee":"10.0","payType":"1","userId":"1111","address":"北京朝阳","requestID":"20190602025343","ticketObtainMode":"1","officeId":"2","ticketTakpePoint":"1","mobile":"18688886666","reserved":"预留","haiNum":0,"allocationFlag":"Y","remark":"备注"}
        content = {
          "sign": "367dc4bea216b766ae5d0f44dc4d5169",
          "ver": "1.0",
          "command": "3004",
          "token": access_token,
          "timestamp": get_time_stamp13(),
          "openid": "23ED8BDB61B06DDA97EE2AC461FE6C1E",
          "param" : data
        }

        sign = create_sign(content, extra_code) 
        content["sign"] = sign

        content_type, post_data = make_form_request_v2(content)
        self.logger.info("content_type:%s" % content_type)
        self.logger.info("post-data:%s" % post_data)

        headers = {"Content-Type" : content_type, "ticket-uid" : ticket_uid}
        resp_headers, resp_data, status_code, err = yield tornado.gen.Task(self.http_request_server, headers, post_data)
        self.logger.info("resp_headers:%s \t resp_data:%s\t status_code:%s\t err:%s" % (resp_headers, resp_data, status_code, err))
        if err is not None:
            self.finish_err_msg(str(err))
            self.logger.error(str(err))
            return
        
        resp_headers["Content-Type"] = "application/json;charset=UTF-8" 
        self.set_response_header(resp_headers)

        self.write(resp_data)
        self.finish()
        
        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

