# -*- coding: utf-8 -*
from redis_client import RedisClient
from mysql_client import MySqlClient
from transform_reqeust import TransformRequestHandler
from ticket_report import TicketReportHandler
from util import logger_handler
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import configparser
from datetime import datetime

tornado.options.define("port", default=9001, type=int, help="port")
tornado.options.define("bind", default="0.0.0.0", type=str, help="address bind to")
tornado.options.define("debug", help="0:info | 1:debug", type=int, default=0)

class EventApplication(tornado.web.Application):

    def __init__(self):
        log_name = "ticket_web_sever"
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

        self.logger = logger_handler(log_name, logpath=log_path, debug=tornado.options.options.debug)

        self.mysql_db = MySqlClient(config_path, "MYSQL", self.logger)            
        self.redis_client = RedisClient(config_path, "REDIS", self.logger)
        
        self.mysql_db.connect()
        self.redis_client.connect()
                           
        tornado.web.Application.__init__(self, [
            (r"/Ticket/uploadIdImg.json", TransformRequestHandler),
            (r"/Ticket/queryTicketResult.json", TransformRequestHandler),
            (r"/Ticket/orderCancel2.json", TransformRequestHandler),
            (r"/Ticket/reqTicket.json", TransformRequestHandler),
            (r"/Ticket/reqOrderTicket.json", TransformRequestHandler),
            (r"/Ticket/orderCancel.json", TransformRequestHandler),
            (r"/Ticket/report.json", TicketReportHandler),
        ], debug=True)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = EventApplication()
    print("port: ", tornado.options.options.port)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(tornado.options.options.port, tornado.options.options.bind)
    tornado.ioloop.IOLoop.current().start()

