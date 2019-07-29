# -*- coding: utf-8 -*
from util import validate_date_str, logger_handler
from mysql_client import MySqlClient
from redis_client import RedisClient
from datetime import datetime, timedelta
import json
import time
import configparser
import argparse

class CrontabStats():
    def __init__(self, publish):
        config_path = "./conf/config_test.conf"
        if publish == 1:
            config_path = "./conf/config.conf"
            
        try:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
            log_path = self.config.get("LOG", "path")
        except Exception as e:
            raise Exception(e)

        self.logger = logger_handler("crontab_stats", logpath=log_path, debug=1)

        self.mysql_db = MySqlClient(config_path, "MYSQL", self.logger)
        self.redis_client = RedisClient(config_path, "REDIS", self.logger)

        self.redis_client.connect()
        self.mysql_db.connect()

    def stats_curday_balance(self, uid, start_time, end_time):
        data = {"order_balance": None, "cancel_balance": None, "updateTime": None}

        sql = "select sum(ticketPrices),updateTime from order_ticket where uid='%s' and status=1 and updateTime>='%s' and updateTime<'%s'" % (uid, start_time, end_time)
        self.logger.info(sql)

        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            return data, err
        
        self.logger.info("order balance: %s" % str(qs))
        if tuple(qs[0]) == (None, None):
            return data, None
       
        data["order_balance"] = qs[0][0]
        data["updateTime"]  = qs[0][1].strftime("%Y-%m-%d %H:%M:%S")

        sql = "select sum(ticketPrices),updateTime from order_cancel where uid='%s' and cancelStatus=1 and updateTime>='%s' and updateTime<'%s'" % (uid, start_time, end_time)
        self.logger.info(sql)
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            return data, err

        self.logger.info("cancel balance: %s" % str(qs))
        if tuple(qs[0]) == (None, None):
            return data, None

        data["cancel_balance"] = qs[0][0]
        data["updateTime"]  = qs[0][1].strftime("%Y-%m-%d %H:%M:%S")

        return data, None

    def cmp_update_time(self, update_time, start_time, end_time):
        s_time =  datetime.strptime(update_time.strftime("%Y-%m-%d"), "%Y-%m-%d")
        stime = datetime.strptime(start_time.split(" ")[0], "%Y-%m-%d")
        etime = datetime.strptime(end_time.split(" ")[0], "%Y-%m-%d")

        self.logger.info("s_time:%s stime: %s etime:%s" % (s_time, stime, etime))
        if s_time >= stime or s_time >= etime:
            return True
        return False

    def valid_reqeust_time(self, start_time, end_time):
        if validate_date_str(start_time, "%Y-%m-%d %H:%M:%S") == False or \
                        validate_date_str(end_time, "%Y-%m-%d %H:%M:%S") == False:
            return True

        c1 = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        c2 = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        self.logger.info("c1:%s c2:%s" % (c1, c2))
        if c1 + timedelta(days=1) < c2 or c1 > c2:
            return True
        return False

    def stats_blanace(self, uid):
        now_time = datetime.now()
        start_time = (now_time + timedelta(days=-1)).strftime("%Y-%m-%d 00:00:00")
        end_time = now_time.strftime("%Y-%m-%d 00:00:00")
        
        if self.valid_reqeust_time(start_time, end_time):
            self.logger.error(r"时间参数越界")
            return

        sql = "select totalBalance,updateTime from account_balance where uid='%s' order by updateTime desc limit 1" % uid
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.logger.error(err)
            return

        if tuple(qs[0]) == (None, None):
            self.logger.error(r"非法uid")
            return

        total_balance = qs[0][0]
        update_time = qs[0][1]

        self.logger.info("total balance: %s update_time:%s" % (total_balance, update_time))
        if self.cmp_update_time(update_time, start_time ,end_time) == True:
            self.logger.info(r"己经更新过余额")
            return

        data, err = self.stats_curday_balance(uid, start_time, end_time)
        if err is not None:
            self.logger.info(err)
            return

        self.logger.info("query balance: %s" % json.dumps(data))
        if data["order_balance"] is None and data["cancel_balance"]  is None:
            self.logger.info("%s-%s无交易余额" % (start_time, end_time))
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
                "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "statsTime": data["updateTime"],
                "operator": 1
                }

        self.logger.info("hdata: %s" % json.dumps(hdata))

        if self.redis_client.hset("ticket-uid", uid, balance) == False:
            self.logger.info(r"更新交易余额失败")
            return

        if self.redis_client.set("ticket_balance_uid_%s" % uid, balance) is None:
            self.logger.info(r"更新缓存余额失败")
            return

        if self.mysql_db.insert("account_balance", hdata) is not None:
            self.logger.info(r"更新余额失败")
            return

        if balance < 0.0:
            self.logger.info(r"余额不足:%s" % hdata)
        else:
            self.logger.info(r"交易正常: "% hdata)
        self.logger.info("=====================end")
        
    def crontab_uids(self):
        sql = "select uid from account_balance group by uid"
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.logger.error(err)
            return
        
        cuids = [{"uid": q[0], "status":-1} for q in qs]

        while True:
            htime = datetime.now().strftime("%H")
            if int(htime) < 1 or int(htime) > 3:
                time.sleep(300)
                break

            self.logger.info("crontab time: %s" % datetime.now())
            for cuid in cuids:
                if cuid["status"] == 0:
                    continue

                if self.stats_blanace(cuid["uid"]) is None:
                    cuid["status"] = 0
            time.sleep(300)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--publish", help="0:test | 1:online", type=int, default=0)
    args = parser.parse_args()
    
    obj = CrontabStats(args.publish)
    obj.crontab_uids()
