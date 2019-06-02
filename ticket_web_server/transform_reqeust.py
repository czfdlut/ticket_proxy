# -*- coding: utf-8 -*
from util import request_query, add_headers
from ticket_util import get_access_token, create_sign, make_form_request_v2
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
        self.logger.error(str(msg))
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
        key = "access_token_%s" % ticket_uid
        access_token = str(self.redis_client.get(key))

        print("------ ", self.ticket_token)
        print("-----key-- ", key)
        self.logger.info("redis_access_token=%s" % access_token)

        if access_token is None:
            access_token = get_access_token(data, extra_code)
            self.redis_client.set(key, access_token)
            self.redis_client.expire(key, 3600)
        
        self.logger.info("access_token=%s" % access_token)
        if access_token is None or len(access_token) == 0:
            self.finish_err_msg(r"验证失败")
            return
              
        data["token"] = str(access_token)
        sign = create_sign(data, extra_code) 
        data["sign"] = sign

        content_type, post_data = make_form_request_v2(data)
        self.logger.info("content_type:%s" % content_type)
        self.logger.info("post-data:%s" % post_data)

        headers = {"Content-Type" : content_type, "ticket-uid" : ticket_uid}
        resp_headers, resp_data, status_code, err = yield tornado.gen.Task(self.http_request_server, headers, post_data)
        self.logger.info("resp_headers:%s \t resp_data:%s\t status_code:%s\t err:%s" % (resp_headers, resp_data, status_code, err))
        if err is not None:
            self.finish_err_msg(str(err))
            return
        
        resp_headers["Content-Type"] = "application/json;charset=UTF-8" 
        self.set_response_header(resp_headers)

        self.write(resp_data)
        self.finish()
        
        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

