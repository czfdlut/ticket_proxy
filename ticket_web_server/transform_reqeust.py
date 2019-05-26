# -*- coding: utf-8 -*
from util import request_query, add_headers
from ticket_util import get_access_token, create_sign, make_form_request_v2
import tornado.web
from datetime import datetime
import json

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
    
    def set_default_headers(self):
        print("setting headers!!!")
        self.set_header("Access-Control-Allow-Origin", "*") 
        self.set_header("Access-Control-Allow-Credentials", "true")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization,postman-token")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def finish_err_msg(self, msg):
        self.logger.error(str(msg))
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()
   
    @tornado.web.asynchronous
    @tornado.gen.coroutine 
    def option(self):
        print("option========")
        self.set_status(204)
        self.finish()
        return
        
    @tornado.gen.coroutine
    def http_request_server(self, headers, body):         
        url = "http://test.maidaopiao.com/" +  self.request.path
        return request_query(self.url, headers=headers, data=body, timeout=60)
   
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        print("st=========")
        start_time = datetime.now()
        self.set_status(200)
        self.finish_err_msg("ok")
 
        request_data =""
        print("request.body=%s" % self.request.body)
        try:
            request_data = json.loads(self.request.body) 
            print("data=%s" % request_data)
        except Exception as e:
            self.finish_err_msg(str(e))
            return
        print("**************************")
        ticket_uid="test_meituan"
        if "ticket-uid" in self.ticket_token.keys():
            ticket_uid = self.ticket_token["ticket-uid"]
        key = "access_token_%s" % ticket_uid
        print("**************************")
        
        access_token = self.redis_client.get(key)
        print("token=%s" % access_token)

        if access_token is None:
            access_token = get_access_token(request_data, "abx23579436")
            self.redis_client.set(key, access_token)
            self.redis_client.expire(key, 3600)
        
        print("token=%s" % access_token)
        if len(access_token) == 0:
            self.finish_err_msg(r"验证失败")
            return
              
        data["token"] = access_token
        sign = create_sign(data, "abx23579436") #self.ticket_token["extra_code"])
        data["sign"] = sign
        
        content_type, post_data = make_form_request_v2(data)
                 
        headers = {
                   "Content-type": "%s; charset='utf-8'" % content_type,
                   "Accept": "application/json",
                   "Cache-Control" : "no-cache", 
                   "Pragma" : "no-cache",
                   "ticket-uid": self.ticket_token["ticket-uid"]
                  }
 
        print("head=%s" % headers)
        print("post-data=%s" % post_data)
        resp_headers, resp_data, status_code, err = yield tornado.gen.Task(self.http_request_server, headers, post_data)
        self.logger.info("resp_headers:%s\n resp_data:%s\n status_code:%s\n err:%s" % (resp_headers, resp_data, status_code, err))
        if err is not None:
            self.finish_err_msg(str(err))
            return
        
        add_headers(resp_headers, "Content-Type", "application/json;charset=UTF-8")    
        self.set_response_header(resp_headers)

        self.write(resp_data)
        self.finish()
        
        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

