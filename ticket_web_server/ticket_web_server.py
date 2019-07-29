# -*- coding: utf-8 -*
from redis_client import RedisClient
from mysql_client import MySqlClient
from order_request import OrderRequestHandler
from order_cancel_request import OrderCancelRequestHandler
from ticket_report import TicketReportHandler
from upload_img_request import UploadImgHandler
from req_ticket_callback import ReqTicketCallBack
from util import logger_handler
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import configparser
from datetime import datetime
import argparse

class EventApplication(tornado.web.Application):

    def __init__(self, publish):
        log_name = "ticket_web_sever"
        config_path = "./conf/config_test.conf"
        if publish == 1:
            config_path = "./conf/config.conf"

        try:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
            log_path = self.config.get("LOG", "path")
        except Exception as e:
            raise Exception(e)
            
        self.ticket_token = {
                    "appid":      "14324152292", 
                    "appsecret":  "59a69169ff81415dfc30ac652353f69f", 
                    "extra_code": "abx23579436", 
                    "ticket_uid": "proxy_test_uid"
                    }

        self.logger = logger_handler(log_name, logpath=log_path, debug=publish)

        self.mysql_db = MySqlClient(config_path, "MYSQL", self.logger)            
        self.redis_client = RedisClient(config_path, "REDIS", self.logger)
        
        self.mysql_db.connect()
        self.redis_client.connect()
                           
        tornado.web.Application.__init__(self, [
            (r"/Ticket/uploadIdImg.json", UploadImgHandler),
            (r"/Ticket/reqOrderTicket.json", OrderRequestHandler),
            (r"/Ticket/orderCancel.json", OrderCancelRequestHandler),
            (r"/Ticket/report.json", TicketReportHandler),
            (r"/TicketOrder/callback", ReqTicketCallBack),
        ], debug=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", help="address", type=str, default="0.0.0.0")
    parser.add_argument("--port", help="server port online:9001, test:7001", type=int, default=9001)
    parser.add_argument("--publish", help="0:test | 1:online", type=int, default=0)
    args = parser.parse_args()

    print("args.bind:", args.bind)
    print("args.port:", args.port)
    print("args.publish:", args.publish)

    application = EventApplication(args.publish)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(args.port, args.bind)
    tornado.ioloop.IOLoop.current().start()


