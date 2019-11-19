# -*- coding: utf-8 -*
from util import request_query, add_headers, get_time_stamp13
from ticket_util import get_access_token, create_sign, make_form_request_v2, join_token_command
import tornado.web
from datetime import datetime
import json
import urllib

class OrderRequestHandler(tornado.web.RequestHandler):
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
        self.set_status(200)
        self.finish()
   
    @tornado.gen.coroutine
    def http_request_server(self, headers, body):         
        url = "http://test.maidaopiao.com:8081" +  self.request.path
        self.logger.info("request url ", url)
        return request_query(url, headers=headers, data=body, timeout=10)
   
    #@tornado.web.asynchronous
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
              
        #data["appid"] = appid
        #data["secret"] = appsecret
        
        #data["bizNo"] = "20190602"
        #data["bizTime"] = "2019-06-02 22:30:00"
        #data["startTime"] = "2019-06-02 22:30:00"
        #data["endTime"] = data["startTime"]
        #data["ticketTime"] = data["startTime"]
        #data["idNo"] = "1:440101200702060012"
        #data["ticketPrices"] = "68.5"
        #data["totalPrices"] = data["ticketPrices"]
        #data["couponValue"] = "50.0"
        #data["bonusFlag"] = "2.0"
        #data["serviceFee"] = "5.0"
        #data["insureFee"] = "3.0"
        #data["expressFee"] = "10.0"
        #data["ticketObtainMode"] = "1"
        #data["trainCode"] = data["trainCode"]
        
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

        a = post_data.encode(encoding='utf-8')



        headers = {"Content-Type" : content_type, "ticket-uid" : ticket_uid}
        resp_headers, resp_data, status_code, err = yield tornado.gen.Task(self.http_request_server, headers, a)
        
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

