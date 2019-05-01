# -*- coding: utf-8 -*
from util import request_query, add_headers
from ticket_util import create_sign
import tornado.web
from datetime import datetime
import json

class TicketReportHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.url = "http://test.maidaopiao.com/Ticket/reqOrderTicket.json"
        
    @property
    def ticket_token(self):
        return self.application.ticket_token
    
    @property
    def logger(self):
        return self.application.logger
    
    @property
    def mysql_client(self):
        return self.application.mysql_client

    def finish_err_msg(self, msg):
        self.logger.error(str(msg))
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()
        
    @tornado.gen.coroutine
    def http_request_server(self, headers, body):
        return request_query(self.url, headers=headers, data=body, timeout=60)

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()
        
        sql = "select totalBalance from account_balance where uid='%s' and totalBalance > 1.0 limit 1" % uid
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.finish_err_msg(str(err))
            return       

        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))

