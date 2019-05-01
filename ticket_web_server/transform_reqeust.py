# -*- coding: utf-8 -*
from util import request_query, add_headers
from ticket_util import create_sign, make_form_request_v2
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
    """
    def get_access_token(self)
        return "test-123456"

    def create_sign(self, data, extra_code):
        keys = data.keys()
        keys.sort()
        #print [key for key in keys]
        #print [data[key] for key in keys]
        message = ""
        for k in keys:
            value = data[k]
            if k != "sign":
                if k != "param":
                    message = message + value
                else:
                    tmp = json.dumps(value)
                    message = message + tmp

        message = message + extra_code
        sign = md5(message)
        print message
        return sign

    def make_form_request_v2(self, data):
        boundary = "-----------------------------7d83e2d7a141e"
        multipart_header_fmt = "multipart/form-data; boundary=%s"
        multipart_fmt = "--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
        multipart_end_fmt = "--%s--\r\n"
        header = multipart_header_fmt % (boundary)

        body = "";
        keys = data.keys()
        keys.sort()
        for k in keys:
            value = data[k]
            if k != "param":
                tmp = multipart_fmt % (boundary, k, value)
                #print(tmp)
                body = body + tmp
            else:
                new_value = json.dumps(value)
                tmp = multipart_fmt % (boundary, k, new_value)
                #print(tmp)
                body = body + tmp

        tmp = multipart_end_fmt % (boundary)
        #print(tmp)
        body = body + tmp
        return header, body
    """
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        print("st=========")
        start_time = datetime.now()
        self.set_status(200)
        self.finish_err_msg("ok")
 
        key = "access_token_%s" % self.ticket_token["ticket-uid"]
        access_token = self.redis_client.get(key)
        if access_token is None:
            access_token = get_access_token()
            self.redis_client.set(key, access_token)
            self.redis_client.expire(key, 3600)
        
        if len(access_token) == 0:
            self.finish_err_msg(r"验证失败")
            return
              
        try:
            data = json.loads(self.request.body)
        except Exception as e:
            self.finish_err_msg(str(e))
            return
        
        data["token"] = access_token
        sign = create_sign(data, "abx23579436") #self.ticket_token["extra_code"])
        data["sign"] = sign
        
        content_type, post_data = make_form_request_v2(data)
                 
        headers = {
                   "Content-type": "%s; charset='utf-8'" % content_type
                   "Accept": "application/json",
                   "Cache-Control: no-cache", 
                   "Pragma: no-cache",
                   "ticket-uid": self.ticket_token["ticket-uid"]
                  }
 
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

