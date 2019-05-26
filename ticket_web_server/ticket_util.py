# -*- coding: utf-8 -*
import datetime
import time
import json
import hashlib
from util import md5, request_query, add_headers

#################################################
def test():
    data = {'sign' : 'abcdefg',
        'ver': "1.0",
        'command' : "1001",
        'token' : "1261109",
        'timestamp' : "12131231",
        'openid' : "test_id",
        'param' : {
            'appid' : '35385640507',
            'secret' : 'a14c4ab485a60833fe09064e27ae013e',
            'merchantCode' : 'meituan'}
       }

    #content = json.dumps(data)
    #print content
    #print data['param']
    #new_data = sorted(data.items(), key=lambda d:d[0])
    return data

#################################################
def get_time_stamp13():
    # 生成13时间戳   eg:1540281250399895
    datetime_now = datetime.datetime.now()

    # 10位，时间点相当于从1.1开始的当年时间编号
    date_stamp = str(int(time.mktime(datetime_now.timetuple())))

    # 3位，微秒
    data_microsecond = str("%06d"%datetime_now.microsecond)[0:3]

    date_stamp = date_stamp+data_microsecond
    return date_stamp

#################################################
def create_sign(data, extra_code):
    #print("-----------")
    #print(data)
    dict_keys = data.keys()
    #print(dict_keys)
    keys = list(dict_keys)
    keys.sort()
    #jjprint(keys)
    #print("-----------")
    #print [key for key in keys]
    #print [data[key] for key in keys]
    message = ""
    for k in keys:
        value = data[k]
        if k != "sign":
            if k != "param":
                message = message + value
            else:
                tmp = json.dumps(value,separators=(',',':'))
                message = message + tmp
        
    message = message + extra_code
    #print("message=%s" %message)
    sign = md5(message.encode("utf-8"))
    #print sign
    return sign


#################################################
def make_form_request_v2(data):
    boundary = "-----------------------------7d83e2d7a141e"
    multipart_header_fmt = "multipart/form-data; boundary=%s"
    multipart_fmt = "--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n"
    multipart_end_fmt = "--%s--\r\n"
    header = multipart_header_fmt % (boundary)
    #print(header)
    
    body = "";
    dict_keys = data.keys()
    keys = list(dict_keys)
    keys.sort()
    #print(keys)
    for k in keys:
        value = data[k]
        if k != "param":
            tmp = multipart_fmt % (boundary, k, value)
            #print(tmp)
            body = body + tmp
        else:
            new_value = json.dumps(value)
            tmp = multipart_fmt % (boundary, k, new_value)
            #print(tmp)
            body = body + tmp

    tmp = multipart_end_fmt % (boundary)
    body = body + tmp
    
    print("=================================")
    print(header)
    print(body)
    print("=================================")

    return header, body


#################################################
def get_access_token_v2(data, extra_code):
    access_token = "123456789101112"
    return str(access_token)

#################################################
def get_access_token(data, extra_code):
    sign = create_sign(data, extra_code)
    data['sign'] = sign

    post_data = json.dumps(data)
    post_data = post_data.encode(encoding='UTF8')
    #print("post_data=%s" %post_data)

    url = "http://test.maidaopiao.com/base/doAction";
    headers = {
	    "Content-type": "application/json;charset='utf-8'", 
	    "Accept" : "application/json", 
	    "Cache-Control" : "no-cache", 
	    "Pragma" : "no-cache",
        "ticket-uid": "proxy_test_uid" 
    }

    resp_headers, resp_data, status_code, err  = request_query(url, headers=headers, data=post_data, timeout=1000)
    if err is not None:
        print("request access_token", err)
        return None

    if status_code is None or status_code < 200 or status_code >= 400:
        return None

    try:
        token = json.loads(resp_data)["data"]["token"]
    except Exception as e:
        print("sign failed", e, resp_data)
        return None

    return token

#################################################
if __name__ == "__main__":
    dt = {
        "sign": "367dc4bea216b766ae5d0f44dc4d5169",
        "ver": "1.0",
        "command": "1001",
        "token": "",
        "param": {"appid" : "14324152292","secret" : "59a69169ff81415dfc30ac652353f69f"},
        "timestamp": "1558857864000",
        "openid": ""
    }

    #sign = create_sign(dt, "abx23579436")
    #dt['sign'] = sign
    dt['timestamp'] = get_time_stamp13()
    print("data: ", dt)
    #print(get_time_stamp13())
    access_token = get_access_token(dt, "abx23579436")
    header, body = make_form_request_v2(dt)
    #print("headers: ", header)
    #print("body: ", body)

