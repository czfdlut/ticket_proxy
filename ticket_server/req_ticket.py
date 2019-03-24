# -*- coding: utf-8 -*
#####################################################
##                                  ##
##         req_ticket 查询余票      ##
##                                  ##
#####################################################
from util import request_query
import tornado.web
from datetime import datetime
import json
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient
import tornado.httpclient

class ReqTicketHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.url = self.config.get("REQ-API", "url")
        self.timeout = self.config.getint("REQ-API", "timeout")

    @property
    def logger(self):
        return self.application.logger

    @property
    def mysql_db(self):
        return self.application.mysql_db

    @property
    def redis_client(self):
        return self.application.redis_client

    @property
    def config(self):
        return self.application.config

    def finish_err_msg(self, msg):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()

    def content_type_from_headers(self):
        for k,v in self.request.headers.items():
            if k.lower() == "content-type":
                return {k: v}
        return {}

    def check_request_param(self):
        try:
            param = json.loads(self.get_argument("param"))
        except Exception as err:
            return "Error: %s" % err, None

        if "train_id" not in param:
            return "Error: not found train_id", None

        if "start_station_id" not in param:
            return "Error: not found start_station_id", None

        if "arrival_station_id" not in param:
            return "Error: not found arrival_station_id", None

        return None, param

    def join_db_data(self, uid, param, server_resp_data):
        hdata = {"uid": uid}
        try:
            resp_data = json.loads(server_resp_data)
            hdata["errmsg"]  = resp_data["errmsg"]
            try:
                if resp_data["errcode"] != "OK":
                    hdata["status"] = 0
                else:
                    hdata["status"] = 1
            except:
                hdata["status"] = 0
        except Exception as err:
            self.logger.error("Error: %s" % err)
            return None

        if "merchantCode" in param:
            hdata["merchantCode"] = param["merchantCode"]

        if "merchantName" in param:
            hdata["merchantName"] = param["merchantName"]

        if "bizNo" in param:
            hdata["bizNo"] = param["bizNo"]

        if "bizName" in param:
            hdata["bizName"] = param["bizName"]

        if "orderDate" in param:
            hdata["orderDate"] = param["orderDate"]

        if "orderNo" in param:
            hdata["orderNo"] = param["orderNo"]

        if "ticketPrices" in param:
            hdata["ticketPrices"] = param["ticketPrices"]

        if "mobile" in param:
            hdata["mobile"] = param["mobile"]

        if "requestID" in param:
            hdata["requestID"] = param["requestID"]

        if "merchantCode" in param:
            hdata["merchantCode"] = param["merchantCode"]

        #if "orderTicketFlow" in param:
        #    hdata["orderTicketFlow"] = param["orderTicketFlow"]

        #hdata["orderTicketFlow"] = resp_data["data"]["orderTicketFlow"]
        hdata["updateTime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return hdata

    def set_response_header(self, headers):
        for k, v in headers.items():
            self.set_header(k, v)

    def set_response_status(self, status):
        self.set_status(status)

    def get_uid_from_headers(self):
        for k,v in self.request.headers.items():
            if k.lower() == "ticket-uid":
                return v
        return None

    def add_headers(self, headers, k, v):
        is_exist_kv = False
        for k ,v in headers.items():
            if k.lower() == k.lower():
                is_exist_kv = true

        if is_exist_kv:
            headers[k] = v

    @tornado.gen.coroutine
    def reqeust_proxy_server(self, headers, body):
        return request_query(self.url, headers=headers, data=body, timeout=self.timeout)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        print("----")
        start_time = datetime.now()

        uid = self.get_uid_from_headers()
        self.logger.info("ticket uid: %s url: %s " % (uid, self.url))
        ## uid合法性校验
        sql = "select totalBalance from account_balance where uid='%s' and totalBalance > 1.0 limit 1" % uid
        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            self.finish_err_msg(r"非法uid")
            return

        self.logger.info("account balance: %s" % qs[0][0])
        
        ##请求参数检查 
        err, param = self.check_request_param()
        if err is not None:
            self.logger.error(err)
            self.finish_err_msg(r"参数错误")
            return

        self.logger.info("reqeust_body: %s " % self.request.body)
        
        ##查询余票信息
        sql = "select * from ticket where train_id='%s' and start_station_id='%s' and arrival_station_id='%s' limit 1" % (param['train_id'], param['start_station_id'], param['arrival_station_id'])
        self.logger.info("sql: %s" % sql)
        qs, err = self.mysql_db.execute_query_sql(sql)
    
        self.logger.info("ticket info: %s" % qs)

        if qs is None or len(qs) == 0:
            self.finish_err_msg(r"非法参数")
            return

        self.logger.info("ticket info: %s" % qs[0][0])

        ##通知client
        resp_headers = {"Content-Type":"application/json"}
        self.set_response_header(resp_headers)
        self.set_response_status(200)

        #hdata = self.join_db_data(uid, param, resp_data)
        #self.logger.info("hdata: %s" % json.dumps(hdata))
        resp_data = "query ticket success!"

        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

