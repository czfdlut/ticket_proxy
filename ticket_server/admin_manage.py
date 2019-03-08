# -*- coding: utf-8 -*
import tornado.web
from datetime import datetime
import json

class AdminManageHandler(tornado.web.RequestHandler):
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

    def update_cacahe_balance(self, uid, total_balance, order_money):
        order_balance = order_money["order_balance"]
        cancel_balance = order_money["cancel_balance"]
        cancel2_balance = order_money["cancel2_balance"]

        cur_balance = total_balance - float(order_balance) - float(cancel_balance) - float(cancel2_balance)

        balance_uid = "ticket-uid_%s" % uid
        self.redis_client.set(cur_balance)
        self.redis_client.hset("ticket-uid", uid, cur_balance)

    def query_curday_balance(self, uid, cur_time):
        order_money = {"order_balance": None, "cancel_balance": None, "cancel2_balance": None}

        sql = "select sum(balance) from order_ticket where uid='%s' and status=1 and updateTime>'%s'" % (uid, cur_time)
        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            return order_money

        self.logger.info("order balance: %s" % qs[0][0])
        order_money["order_balance"] = qs[0][0]

        sql = "select sum(balance) from order_cancel where uid='%s' and cancelStatus=1 and updateTime>'%s'" % (uid, cur_time)
        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            return order_money

        self.logger.info("cancel balance: %s" % qs[0][0])
        order_money["cancel_balance"] = qs[0][0]

        sql = "select sum(balance) from order_cancel2 where uid='%s' and status=1 and updateTime>'%s'" % (uid, cur_time)
        qs = self.mysql_db.execute_query_sql(sql)
        if qs is None or len(qs) == 0:
            return order_money

        self.logger.info("cancel balance: %s" % qs[0][0])
        order_money["cancel2_balance"] = qs[0][0]

        return order_money

    def get(self):
        print("--------------------------------bbb")
        self.logger.info("%s%s?%s" % (self.request.host, self.request.path, self.request.query))

        # uid = self.get_argument("uid", default=None, strip=True)
        # query_time = self.get_argument("query_time", default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), strip=True)
        #
        # start_time = datetime.now()
        #
        # uid = self.get_argument('uid')
        #
        # self.set_header("Content-Type", "application/json;charset=UTF-8")
        #
        # sql = "select balance,updateTime from account_balance where uid='%s' order by updateTime desc limit 1" % uid
        # qs = self.mysql_db.execute_query_sql(sql)
        # if qs is None or len(qs) == 0:
        #     self.finish_err_msg(r"非法uid")
        #     return
        #
        # total_balance = qs[0][0]
        # self.logger.info("total balance: %s" % total_balance)
        #
        # self.write({"errcode": 0, "errmsg": "ok", "data": self.query_curday_balance(uid))
        # self.finish()
        #
        # self.logger.info("cost time: %s" %((datetime.now() - start_time)))
