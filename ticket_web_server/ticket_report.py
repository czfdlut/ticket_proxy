# -*- coding: utf-8 -*
import tornado.web
from datetime import datetime
import json

##################################################
## method: get 
## param:  
##    table: account_balance, order_cancel, order_ticket, ticket
##    start: 0
##    pagesize: 10
#   curl http://test.maidaopiao.com:8080/Ticket/report.json?table=account_balance&start=0&pagesize=10
#         http://test.maidaopiao.com:8080/Ticket/report.json?table=order_cancel&start=0&pagesize=10
#         http://test.maidaopiao.com:8080/Ticket/report.json?table=order_ticket&start=0&pagesize=10
#         http://test.maidaopiao.com:8080/Ticket/report.json?table=ticket&start=0&pagesize=10
##################################################

class TicketReportHandler(tornado.web.RequestHandler):
    @property
    def ticket_token(self):
        return self.application.ticket_token
    
    @property
    def logger(self):
        return self.application.logger
    
    @property
    def mysql_db(self):
        return self.application.mysql_db

    def finish_err_msg(self, msg):
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.write({"errcode": -1, "errmsg": msg, "data": {}})
        self.finish()
        self.logger.error(str(msg))
       
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        start_time = datetime.now()
        table = self.get_argument("table", default="", strip=True)
        start = self.get_argument("start", default=0, strip=True)
        pagesize = self.get_argument("pagesize", default=10, strip=True)
        
        start = int(start)
        pagesize = int(pagesize)

        if pagesize <= 0 or pagesize > 10:
            pagesize = 10
        
        sql = "select count(id) from `%s`" % table
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.finish_err_msg(str(err))
            return     
            
        total = int(qs[0][0])  
        pos = start * total/pagesize
                
        if table == "account_balance":
            fields = {
                      "updateTime": r"操作时间",
                      "uid": "商户id",
                      "totalBalance": r"当前帐号余额",
                      "lastTransMoney": r"上笔结算金额",
                      "statsTime": "统计时间",
                      "operator": r"1:统计,2:加钱,3扣钱"
                    }
        elif table == "order_cancel":
            fields = {
                        "updateTime": r"更新时间",
                        "uid": r"商户id",
                        "merchantCode": r"商户系统编号",
                        "merchantName": r"商户名称",
                        "bizNo": r"业务流水编号",
                        "bizName": r"业务名称",
                        "bizType": r"业务类型",
                        "orderId": r"订单号",
                        "requestID": r"请求流水号",
                        "orderTicketFlow": r"操作流水号",
                        "cancelStatus": r"状态(成功(0),失败1)",
                        "ticketPrices": r"票价",
                        "errmsg": r"西铁返回信息"
                    }
        elif table == "order_ticket":
            fields = {
                        "updateTime": r"更新时间",
                        "uid": r"商户id",
                        "merchantCode": r"商户系统编号",
                        "merchantName": r"商户名称",
                        "bizNo": r"业务流水编号",
                        "bizName": r"业务名称",
                        "bizBrief": r"业务摘要",
                        "bizTime": r"业务日期",
                        "orderDate": r"订票日期",
                        "orderNo": r"对应订单流水号",
                        "ticketPrices": r"总票价",
                        "payType": r"支付类型:0,云闪付:1:支付宝,2:微信,3:其他",
                        "mobile": r"手机号",
                        "requestID": r"请求流水号",
                        "orderTicketFlow": r"操作流水号",
                        "status": r"执行状态码",
                        "errmsg": r"返回信息"
                     }
        elif table == "ticket":
            fields = {
                        "updateTime" : r"更新时间",
                        "train_id": r"车次编号",
                        "train_name": r"车次名称",
                        "start_station_id": r"始发车站编号",
                        "start_station_name": r"始发车站名称",
                        "arrival_station_id": r"到达车站编号",
                        "arrival_station_name": r"到达车站名称",
                        "via_station": r"途经站信息",
                        "start_datetime": r"始发时间",
                        "arrival_datetime": r"到达时间",
                        "seat_type": r"座位席别",
                        "ticket_price": r"票价",
                        "ticket_count": r"余票数量",
                        "status": r"售票状态"  
                     }
        
        keys = fields.keys()
        marks = fields.values()        
        sql = "SELECT %s FROM %s ORDER BY `updateTime` LIMIT %d, %d " % (",".join(keys), table, pos, pagesize)            
        qs, err = self.mysql_db.execute_query_sql(sql)
        if err is not None:
            self.finish_err_msg(str(err))
            return              
        
        rs = []
        for q in qs:
            temp = []
            for t in q:
                if isinstance(t, datetime):
                    temp.append(t.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    if isinstance(t, str) and len(t) > 100:
                        temp.append(t[0:100])
                    else:
                        temp.append(str(t))
            rs.append(temp)
        
        resp_data = {"marks": list(marks), "values": rs, "total": total, "start": start, "pagesize": pagesize}        
        self.set_header("Content-Type", "application/json;charset=UTF-8") 
        self.write(resp_data)
        self.finish()

        self.logger.info("cost time: %s" %((datetime.now() - start_time)))
 
