# -*- coding: utf-8 -*
from util import validate_date_str
import tornado.web
from datetime import datetime
import json

class UpdateBalanceHandler(tornado.web.RequestHandler):
    @property
    def logger(self):
        return self.application.logger

    @property
    def mysql_db(self):
        return self.application.mysql_db

    @property
    def redis_client(self):
        return self.application.redis_client

    def stats_curday_balance(self, uid, start_tme, end_time):
        data = {"order_balance": None, "cancel_balance": None}

        sql = "select sum(ticketPrices) from order_ticket where uid='%s' \
                        and status=1 and updateTime>='%s' and updateTime<'%s'" % (uid, start_tme, end_time)
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            return data, err

        self.logger.info("order balance: %s" % str(qs))
        if qs is None or len(qs) == 0:
            return data, None

        data["order_balance"] = qs[0][0]

        sql = "select sum(ticketPrices) from order_cancel where uid='%s' \
                    and cancelStatus=1 and updateTime>='%s' and updateTime<'%s'" % (uid, start_tme, end_time)
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            return data, err

        self.logger.info("cancel balance: %s" % str(qs))
        if qs is None or len(qs) == 0:
            return data, None

        data["cancel_balance"] = qs[0][0]

        return data, None

    def get(self):
        self.logger.info("%s%s?%s" % (self.request.host, self.request.path, self.request.query))

        uid = self.get_argument("uid", default=None, strip=True)
        start_time = self.get_argument("start_time", default=None, strip=True)
        end_time = self.get_argument("end_time", default=None, strip=True)

        self.set_header("Content-Type", "application/json;charset=UTF-8")
        if uid is None or start_time is None or end_time is None:
            self.write({"errcode": -1, "errmsg": r"参数错误", "data": {}})
            self.finish()
            return

        if validate_date_str(start_time, "%Y-%m-%d %H:%M:%S") == False or \
                        validate_date_str(end_time, "%Y-%m-%d %H:%M:%S") == False:
            self.write({"errcode": -1, "errmsg": r"参数错误", "data": {}})
            self.finish()
            return

        sql = "select totalBalance,updateTime from account_balance where uid='%s' order by updateTime desc limit 1" % uid
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.write({"errcode": -1, "errmsg": str(err), "data": {}})
            self.finish()
            return

        if qs is None or len(qs) == 0:
            self.write({"errcode": -1, "errmsg": r"非法uid", "data": {}})
            self.finish()
            return

        total_balance = qs[0][0]
        utime = qs[0][1].strftime("%Y-%m-%d %H:%M:%S").split(" ")[0]
        stime = start_time.split(" ")[0]
        etime = end_time.split(" ")[0]

        self.logger.info("total balance: %s stime:%s utime:%s etime:%s" % (total_balance, stime, utime, etime))
        if utime == stime or utime == etime:
            self.write({"errcode": 0, "errmsg": r"己经更新过余额", "data": {}})
            self.finish()
            return

        data, err = self.stats_curday_balance(uid, start_time, end_time)
        if err is not None:
            self.write({"errcode": -1, "errmsg": str(err), "data": {}})
            self.finish()
            return

        self.logger.info("query balance: %s" % json.dumps(data))

        if data["order_balance"] is None and data["cancel_balance"]  is None:
            self.write({"errcode": 0, "errmsg": "%s-%s无交易余额" % (start_tme, end_time), "data": {}})
            self.finish()
            return

        trans_balance = 0.0
        if data["order_balance"] is not None:
            trans_balance = float(data["order_balance"])

        if data["cancel_balance"]  is not None:
            trans_balance = trans_balance - float(data["cancel_balance"])

        balance = total_balance - trans_balance
        self.logger.info("total_balance: %f trans_balance: %f balance: %f" % (total_balance, trans_balance, balance))

        hdata = {
                "totalBalance": balance,
                "lastTransMoney": trans_balance,
                "uid": uid,
                "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

        self.logger.info("hdata: %s" % json.dumps(hdata))

        if self.redis_client.hset("ticket-uid", uid, balance) == False:
            self.write({"errcode": -1, "errmsg": r"更新交易余额失败", "data": hdata})
            self.finish()
            return

        if self.redis_client.set("ticket_balance_uid_%s" % uid, balance) is None:
            self.write({"errcode": -1, "errmsg": r"更新缓存余额失败", "data": hdata})
            self.finish()
            return

        if self.mysql_db.insert("account_balance", hdata) is not None:
            self.write({"errcode": -1, "errmsg": r"更新余额失败", "data": hdata})
            self.finish()
            return

        if balance < 0.0:
            self.logger.info("trans_balance < totalBalance")
            self.write({"errcode": 0, "errmsg": r"余额不足", "data": hdata})
        else:
            self.write({"errcode": 0, "errmsg": r"交易正常", "data": hdata})
        self.finish()

        self.logger.info("=====================end")
