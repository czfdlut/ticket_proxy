# -*- coding: utf-8 -*
from mysql_client import MySqlClient
from redis_client import RedisClient
from req_ticket import ReqTicketHandler
from req_order_ticket import ReqOrderTicketHandler
from order_cancel import OrderCancel
from req_ticket_callback import ReqTicketCallBack
from util import logger_handler
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import configparser
import argparse
from datetime import datetime
from tornado.httpclient import AsyncHTTPClient

class Test1Handler(tornado.web.RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        http_client = AsyncHTTPClient()
        response = yield http_client.fetch('https://www.baidu.com')
        print('response: ', response.body)

class StatusCheck(tornado.web.RequestHandler):
    @property
    def logger(self):
        return self.application.logger

    @tornado.gen.coroutine
    def get(self):
        print("headers: ", self.request.headers)
        self.finish("proxy server ok\n")

    @tornado.gen.coroutine
    def post(self):
        print("headers: ", self.request.headers)
        self.finish("proxy server ok\n")

class EventApplication(tornado.web.Application):
    def __init__(self, publish):
        log_name = "proxy_sever"
        config_path = "./conf/config_test.conf"
        if publish == 1:
            config_path = "./conf/config.conf"
                    
        try:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
            log_path = self.config.get("LOG", "path")
        except Exception as e:
            raise Exception(e)

        self.logger = logger_handler(log_name, logpath=log_path, debug=publish)

        self.mysql_db = MySqlClient(config_path, "MYSQL", self.logger)
        self.redis_client = RedisClient(config_path, "REDIS", self.logger)

        self.redis_client.connect()
        self.mysql_db.connect()

        tornado.web.Application.__init__(self, [
            (r"/status", StatusCheck),
            (r"/Ticket/reqTicket.json", ReqTicketHandler),
            (r"/Ticket/reqOrderTicket.json", ReqOrderTicketHandler),
            (r"/Ticket/orderCancel.json", OrderCancel),
            (r"/TicketOrder/callback", ReqTicketCallBack),
            (r"/test", Test1Handler),
        ], debug=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", help="address", type=str, default="0.0.0.0")
    parser.add_argument("--port", help="server port online:9002, test:7002", type=int, default=9002)
    parser.add_argument("--publish", help="0:test | 1:online", type=int, default=0)
    args = parser.parse_args()
    
    print("args.bind:", args.bind)
    print("args.port:", args.port)
    print("args.publish:", args.publish)
    
    application = EventApplication(args.publish)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(args.port, args.bind)
    tornado.ioloop.IOLoop.current().start()
