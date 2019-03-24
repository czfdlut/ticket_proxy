# -*- coding: utf-8 -*
from mysql_client import MySqlClient
from util import request_query
from util import logger_handler
import tornado.ioloop
import time
from datetime import timedelta, datetime
import urllib.parse
import configparser
import json

####http://39.107.85.196:8080/admin/update/balance?uid=for_test&start_time=2019-03-09%2000:00:00&end_time=2019-03-10%2000:00:00
class CrontabBalance():
    def __init__(self):
        log_name = "crontab_update"
        config_path = "./conf/config.conf"

        try:
            self.config = configparser.ConfigParser()
            self.config.read(config_path)
            log_path = self.config.get("LOG", "path")
        except Exception as e:
            raise Exception(e)

        self.logger = logger_handler(log_name, logpath=log_path, debug=1)
        self.mysql_db = MySqlClient(config_path, "MYSQL", self.logger)
        self.admin_url = "http://127.0.0.1:8080/admin/update/balance"

    def crontab_update(self, uid):
        end_time = datetime.now()
        start_time = end_time + timedelta(days=-1)

        stime = start_time.strftime("%Y-%m-%d 00:00:00")
        utime = end_time.strftime("%Y-%m-%d 00:00:00")

        param = {"start_time": stime, "end_time": utime, "uid": uid}
        url = self.admin_url + "?" + urllib.parse.urlencode(param)

        self.logger.info("url: %s" % url)

        resp_headers, resp_data, status_code, err = request_query(url)
        if err is not None:
            self.logger.error(err)
            return err

        self.logger.info("status_code: %d" % status_code)
        if status_code < 200 or status_code > 400:
            self.logger.error(resp_data)
            return "reqest failed"

        self.logger.info("resp_data: %s" % resp_data)

        try:
            hdata = json.loads(resp_data)
        except Exception as err:
            self.logger.error(err)
            return err

        if hdata["errcode"] < 0:
            self.logger.error(hdata["errmsg"])
            return hdata["errmsg"], None
        else:
            self.logger.info(hdata["errmsg"])

        self.logger.info("update uid:%s blance sucess" % uid)
        return None

    def crontab_uids(self):
        if self.mysql_db.connect() is not None:
            return

        sql = "select uid from account_balance group by uid"
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.logger.error(err)
            return

        cuids = [{"uid": q[0], "status":-1} for q in qs]
        self.logger.info("uids: %s" % cuids)

        while True:
            htime = datetime.now().strftime("%H")
            self.logger.info("cur time: %s" % datetime.now())
            if int(htime) < 1 or int(htime) > 3:
                time.sleep(30)
                break

            for cuid in cuids:
                if cuid["status"] == 0:
                    continue

                if self.crontab_update(cuid["uid"]) is None:
                    cuid["status"] = 0
            time.sleep(30)


if __name__ == "__main__":
    obj = CrontabBalance()
    #obj.crontab_uids()

    io_loop = tornado.ioloop.IOLoop.current()
    tornado.ioloop.PeriodicCallback(obj.crontab_uids, 30000).start()
    io_loop.start()
