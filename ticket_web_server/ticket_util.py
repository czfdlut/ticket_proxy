# -*- coding: utf-8 -*
from util import md5, request_query, add_headers

def get_access_token():
    access_token = ""
    return access_token

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

def create_sign(data, extra_code):
    keys = data.keys()
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
    sign = md5(message)
    print message
    #print sign
    return sign


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

if __name__ == "__main__":
    dt = test()
    print dt
    sign = create_sign(dt, "abx23579436")
    dt['sign'] = sign
    print dt
    header, body = make_form_request_v2(dt)
    print header
    print body

