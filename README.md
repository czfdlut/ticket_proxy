# ticket_proxy
ticket proxy
1代码
https://github.com/czfdlut/ticket_proxy

 
2 服务部署
都在阿里云机器上：39.107.85.196
(1)	Nginx部署
部署目录：/home/work/nginx/
配置详见：/home/work/nginx/conf/nginx.conf
启动方式：
方式1：/home/work/start_nginx.sh
方式2：
source /etc/profile
 /home/work/nginx/sbin/nginx -c /home/work/nginx/conf/nginx.conf -s reload

权限：work
当前设置了两个对外端口：8080用于web-server，供内部工具使用；
8081用于proxy-server，用于转发美团的请求给西铁。
(2)	Proxy-server部署
部署目录：/home/work/ticket_proxy/ticket_server
启动方式：
/usr/bin/supervisord -c /home/work/supervisord/supervisord.conf
/usr/bin/supervisorctl -c /home/work/supervisord/supervisord.conf start/stop proxy_server
权限：work
端口：9002
(3)	Web-server部署
部署目录：/home/work/ticket_proxy/ticket_web_server
启动方式：
/usr/bin/supervisord -c /home/work/supervisord/supervisord.conf
/usr/bin/supervisorctl -c /home/work/supervisord/supervisord.conf start/stop ticket_web_server
权限：work
端口：9001
(4)	其他依赖模块
MySQL，用于实现用户数据、订单数据的存储和统计
Redis，用于实现分布式锁，以及用户数据存储
Python3，proxy-server和web-server依赖
PHP7，ticket-client依赖
(5)	Client测试用例
用于对西铁服务的测试，以及Proxy-server的测试。
部署目录：/home/work/ticket_proxy/ticket_client
(6)	测试环境
配置：/home/work/nginx/conf/test/nginx.conf
   服务端口： 7081
   web页面端口: 7080
   web访问页面： http://test.maidaopiao.com:7080/ticket/admin/report.html?n=order_ticket
(7)	线上环境
配置：/home/work/nginx/conf/online/nginx.conf 
   服务端口： 8081
   web页面端口: 8080
   web访问页面： http://test.maidaopiao.com:8080/ticket/admin/report.html?n=order_ticket
3 服务架构与流程
 
4 内部工具简介
页面地址：http://test.maidaopiao.com:8080/ticket/admin/index.html
订单查询
 
下单
 
退单
 

5备注
后续工作
前端页面上传证件
与美团联调
QA团队测试

