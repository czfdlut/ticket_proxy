# -*- coding: utf-8 -*
#####################################################
##                              ##
##         cancel order        ##
##                              ##
#####################################################
from util import request_query
import tornado.web
from datetime import datetime
import json
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient
import tornado.httpclient

class OrderCancel(tornado.web.RequestHandler):
    def initialize(self):
        self.url = self.config.get("CACEL-API", "url")
        self.timeout = self.config.getint("CACEL-API", "timeout")

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

    def update_balance(self, uid, balance):
        sql = "update account_balance set balance=%f where uid='%s'" % (balance, uid)
        self.mysql_db.execute_sql(sql)

    def finish_err_msg(self, msg):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()
        self.logger.info("finish order cacel reqeust=====================end")

    def content_type_from_headers(self):
        for k,v in self.request.headers.items():
            if k.lower() == "content-type":
                return {k: v}
        return {}

    def get_ticket_prices(self, uid, request_body):
        try:
            param = json.loads(self.get_argument("param"))
            orderId = param["orderId"]
        except Exception as err:
            self.logger.error("Error: %s" % err)
            return None
        
        sql = "select ticketPrices from order_ticket where uid='%s' and orderNo ='%s' limit 1" \
            % (uid, orderId)
        qs, err = self.mysql_db.execute_query_sql(sql)
        print("qs:", qs, "err:", err)
        if err is not None:
            self.logger.error(str(err))
            return None        

        if len(qs) == 0:
            self.logger.info("sql return empty results")
            return None

        if qs[0][0] is None:
            self.logger.error("not found uid:%s orderid:%s" %(uid, orderId))
            return None
        ticket_prices = qs[0][0]
               
        return ticket_prices

    def check_request_param(self):
        try:
            param = json.loads(self.get_argument("param"))
        except Exception as err:
            return "Error: %s" % err

        if "merchantCode" not in param:
            return "Error: not found merchantCode"

        if "bizNo" not in param:
            return "Error: not found bizNo"

        if "bizType" not in param:
            return "Error: not found bizType"

        if "orderId" not in param:
            return "Error: not found orderId"

        if "requestID" not in param:
            return "Error: not found requestID"

        return None

    def join_db_data(self, uid, server_resp_data, ticket_prices):
        hdata = {"uid": uid}
        success = 1
        try:
            param = json.loads(self.get_argument("param"))
            resp_data = json.loads(server_resp_data)
            hdata["errmsg"]  = resp_data["errmsg"]
            try:
                if (resp_data["errcode"] != "OK"):
                    success = 0
                else:
                    success = 1
            except:
                success = 0 
        except Exception as err:
            self.logger.error("Error: %s" % err)
            return None
        
        if "merchantCode" in param:
            hdata["merchantCode"] = param["merchantCode"]

        if "merchantName" in param:
            hdata["merchantName"] = param["merchantName"]

        if "bizNo" in param:
            hdata["bizNo"] = param["bizNo"]
            hdata["bizName"] = "cancel_ticket"
            
        if "bizType" in param:
            hdata["bizType"] = param["bizType"]
        
        if "orderId" in param:
            hdata["orderId"] = param["orderId"]

        if "requestID" in param:
            hdata["requestID"] = param["requestID"]

        if success == 1:
            hdata["orderTicketFlow"] = resp_data["data"]["orderTicketFlow"]
            hdata["cancelStatus"] = resp_data["data"]["cancelStatus"]
        else:
            hdata["cancelStatus"] = 1


        if hdata["cancelStatus"] != 0:
            ticket_prices = 0

        hdata["ticket_prices"] = ticket_prices
        hdata["update_Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return hdata
    
    def set_response_header(self, headers):
        for k, v in headers.items():
            self.set_header(k, v)

    def set_response_status(self, status):
        self.set_status(status)

    def get_uid_from_headers(self):
        for k,v in self.request.headers.items():
            print(k,"->",v)
            if k.lower() == "ticket-uid":
                return v
        return None
    
    @tornado.gen.coroutine    
    def reqeust_proxy_server(self, headers, body):
        return request_query(self.url, headers=headers, data=body, timeout=self.timeout)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()

        uid = self.get_uid_from_headers()
        #uid = "for_test"
        self.logger.info("ticket uid: %s url: %s" % (uid, self.url))

        ##参数检查
        err = self.check_request_param()
        if err is not None:
            self.logger.info("check param failed")
            self.logger.error(err)
            self.finish_err_msg(err)
            return
        
        self.logger.info("query prices")
        ##查询票价
        ticket_prices = self.get_ticket_prices(uid, self.request.body)
        #if ticket_prices is None:
        #    self.logger.error("orderId error")
        #    self.finish_err_msg("orderId error")
        #    return
        
        self.logger.info("notify client")
        ##notify client
        resp_headers = {"Content-Type":"application/json"}
        self.set_response_header(resp_headers)
        self.set_response_status(200)
 
        ##请求西铁
        headers = self.content_type_from_headers()
        resp_headers, resp_data, status_code, err  = yield tornado.gen.Task(self.reqeust_proxy_server, headers, self.request.body)
        
        self.logger.info("resp_headers:%s\n resp_data:%s\n status_code:%s\n err:%s" % (resp_headers, resp_data, status_code, err))    

        ##请求失败
        if err is not None:         
            self.logger.error("request error:%s" % err)
            self.write(err)
            self.finish()
            return

        ##插入退单表
        hdata = self.join_db_data(uid, resp_data, ticket_prices)
        print("hdata: ", hdata)

        self.logger.info("hdata: %s" % str(hdata))         
        if hdata is None:
            self.logger.error("db data error")
            self.write(resp_data)
            self.finish()
            return
        
        ##退单锁
        lock_cancel_order_uid = "ticket_uid_%s_lock_cancel" % uid
        lock = self.redis_client.acquire(lock_cancel_order_uid, 3)
        self.mysql_db.insert("order_cancel", hdata)
        self.redis_client.release(lock)
        
        ##退单成功
        if hdata["cancelStatus"] == 0:
            ##更新reids余额
            balance_uid = "ticket_balance_uid_%s" % uid
            self.redis_client.incrbyfloat(balance_uid, uid, ticket_prices)
        
        self.set_header("Content-Type", "application/json;charset=UTF-8")          
        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))
  
        #self.update_balance(uid, balance)
        #self.redis_client.hset("ticket-uid", uid, balance)
       
