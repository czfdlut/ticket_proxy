# -*- coding: utf-8 -*
import json
import hashlib
from util import md5, request_query, add_headers

#################################################
def md5(url):
    m = hashlib.md5(url)
    return m.hexdigest()


#################################################
def test():
    data = {'sign' : 'abcdefg',
        'ver': "1.0",
        'command' : "203",
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
def create_sign(data, extra_code):
    dict_keys = data.keys()
    #print(dict_keys)
    keys = list(dict_keys)
    keys.sort()
    #print [key for key in keys]
    #print [data[key] for key in keys]
    message = ""
    for k in keys:
        value = data[k]
        if k != "sign":
            if k != "param":
                message = message + value
            else:
                tmp = json.dumps(value)
                message = message + tmp
        
    message = message + extra_code
    print("message=%s" %message)
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
    keys = data.keys()
    keys.sort()
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
    #print(tmp)
    body = body + tmp
    return header, body


#################################################
'''def get_access_token():
    access_token = ""
    return access_token
'''

#################################################
def get_access_token(data, extra_code):
    
    print("data=%s" %data)
    sign = create_sign(data, extra_code)
    data['sign'] = sign
    print("data=%s" %data)

    post_data = json.dumps(data)
    print("post_data=%s" %post_data)

    url = "https://test.maidaopiao.com/base/doAction";
    headers = {
	    "Content-type": "application/json;charset='utf-8'", 
	    "Accept" : "application/json", 
	    "Cache-Control" : "no-cache", 
	    "Pragma" : "no-cache" 
    }
    #request_query(url, headers, post_data, 1000)
    resp_headers, resp_data, status_code, err  = request_query(url, headers=headers, data=post_data, timeout=1000)
    print(resp_headers)
    print(resp_data)
    #$ret_array = json_decode($ret_data, true);
    #return $ret_array['data']['token'];


#################################################
if __name__ == "__main__":
    dt = test()
    print(dt)
    #ll = ['sign', 'ver', 'command', 'token', 'timestamp', 'openid', 'param']
    #ll.sort()
    #print(ll)
    '''
    sign = create_sign(dt, "abx23579436")
    dt['sign'] = sign
    print(dt)
    header, body = make_form_request_v2(dt)
    print(header)
    print(body)
    '''
    get_access_token(dt, "abx23579436")

