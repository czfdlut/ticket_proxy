# -*- coding: utf-8 -*
#####################################################
##                              ##
##         req_order            ##
##                              ##
#####################################################
from util import request_query, add_headers
import tornado.web
from datetime import datetime
import json
from tornado.concurrent import Future
from tornado.httpclient import AsyncHTTPClient
import tornado.httpclient

class ReqOrderTicketHandler(tornado.web.RequestHandler):
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
        self.set_status(200)
        self.write({"errcode": -1, "errmsg": str(msg), "data": {}})
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

        if "ticketPrices" not in param:
            return "Error: not found ticketPrices", None

        if float(param["ticketPrices"]) < 1.0 or float(param["ticketPrices"]) > 3000:
            return "Error: money out of money", None

        if "merchantCode" not in param:
            return "Error: not found merchantCode", None

        if "bizNo" not in param:
            return "Error: not found bizNo", None

        if "bizName" not in param:
            return "Error: not found bizName", None

        if "bizTime" not in param:
            return "Error: not found bizTime", None

        if "orderDate" not in param:
            return "Error: not found orderDate", None

        if "ticketPrices" not in param:
            return "Error: not found ticketPrices", None

        if "payType" not in param:
            return "Error: not found payType", None

        if "requestID" not in param:
            return "Error: not found requestID", None

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

    @tornado.gen.coroutine
    def reqeust_proxy_server(self, headers, body):
        return request_query(self.url, headers=headers, data=body, timeout=self.timeout)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()

        uid = self.get_uid_from_headers()
        self.logger.info("ticket uid: %s url: %s " % (uid, self.url))
        ## uid合法性校验
        sql = "select totalBalance from account_balance where uid='%s' and totalBalance > 1.0 limit 1" % uid
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.finish_err_msg(str(err))
            return

        if len(qs) == 0 or qs[0][0] is None:
            self.finish_err_msg(r"非法uid")
            return

        self.logger.info("account balance: %s" % qs[0][0])
        
        ##请求参数检查 
        err, param = self.check_request_param()
        if err is not None:
            self.logger.error(err)
            self.finish_err_msg(err)
            return

        self.logger.info("reqeust_body: %s " % self.request.body)
        
        ##账户余额检查
        balance_uid = "ticket_balance_uid_%s" % uid
        trans_balance = self.redis_client.get(balance_uid)
        if trans_balance is None:
            self.logger.error("not found ticket_balance: %s" % balance_uid)
            self.finish_err_msg(r"金额错误")
            return

        self.logger.info("trans_balance: %s" % float(trans_balance))

        cur_balance = self.redis_client.hget("ticket-uid", uid)
        if len(cur_balance) == 0:
            self.finish_err_msg(r"金额错误")
            return

        self.logger.info("current_balance: %s" % cur_balance)

        ##票价检查
        ticket_prices = float(param["ticketPrices"])
        if float(trans_balance) < ticket_prices or float(cur_balance) < ticket_prices:
            self.finish_err_msg(r"金额超限")
            return

        self.logger.info("ticket_prices: %f" % ticket_prices)
        trans_after_balance = self.redis_client.incrbyfloat(balance_uid, -1.0 * ticket_prices)
        if trans_after_balance is None:
	        self.finish_err_msg(r"交易非法")
	        return

        if float(trans_after_balance) < 0.01:
            self.redis_client.incrbyfloat(balance_uid, ticket_prices)
            self.finish_err_msg(r"交易非法")
            return

        ##请求西铁
        headers = self.content_type_from_headers()
        resp_headers, resp_data, status_code, err = yield tornado.gen.Task(self.reqeust_proxy_server, headers, self.request.body)
        
        self.logger.info("resp_headers:%s\n resp_data:%s\n status_code:%s\n err:%s" % (resp_headers, resp_data, status_code, err))

        if err is not None:
            self.logger.error("request error:%s" % err)
            self.redis_client.incrbyfloat(balance_uid, ticket_prices)
            self.write(err)
            self.finish()
            return

        ##notify client
        add_headers(resp_headers, "Content-Type", "application/json;charset=UTF-8")    
        self.set_response_header(resp_headers)
        self.set_response_status(200)

        self.logger.info("test: %s" % str("test"))
        hdata = self.join_db_data(uid, param, resp_data)
        self.logger.info("hdata: %s" % json.dumps(hdata))

        ##下单失败
        if hdata is None or hdata["status"] == 0:
            self.redis_client.incrbyfloat(balance_uid, ticket_prices)
            self.write("{uid : testggg}")
            self.finish()
            self.logger.info("cost time: %s" %((datetime.now() - start_time)))
            return

        if hdata is None:
            self.logger.error("db data error")
            self.write(resp_data)
            self.finish()
            self.logger.info("cost time: %s" %((datetime.now() - start_time)))
            return

        ##下单成功
        lock_req_order_uid = "ticket_uid_%s_lock_req" % uid
        lock = self.redis_client.acquire(lock_req_order_uid, 1)
        self.mysql_db.insert("order_ticket", hdata)
        self.redis_client.release(lock)

        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

