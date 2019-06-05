import tornado.web
from datetime import datetime
import json

class ReqTicketCallBack(tornado.web.RequestHandler):
    @property
    def logger(self):
        return self.application.logger

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        start_time = datetime.now()
       
        resp_data = {
            "errcode" : "0",
            "errmsg" : {
                "order_status" : "3",
                "data" : "确认成功"
             }
        }
        #post_data = bytes(json.dumps(resp_data), 'utf8')
        post_data = json.dumps(resp_data)
        #resp_data = {"callback": "ok"} 
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write(post_data)
        self.finish()

        self.logger.info("order ticket cost time: %s" %((datetime.now() - start_time)))

