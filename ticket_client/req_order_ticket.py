import json
import hashlib

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

def md5(url):
    m = hashlib.md5(url)
    return m.hexdigest()

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

function make_form_request_v2($content, &$header, &$body)
{
    $boundary = "-----------------------------7d83e2d7a141e";
    $multipart_header_fmt = "multipart/form-data; boundary=%s";
    $multipart_fmt = "--%s\r\nContent-Disposition: form-data; name=\"%s\"\r\n\r\n%s\r\n";
    $multipart_end_fmt = "--%s--\r\n";
    $header = sprintf($multipart_header_fmt, $boundary);
    $body = "";
    foreach($content as $key => $value) 
    {
        if ($key != "param") 
        {
            $tmp = sprintf($multipart_fmt, $boundary, $key, $value);
            $body = $body.$tmp;
        }
        else
        {
            $new_value = json_encode($value);
            $tmp = sprintf($multipart_fmt, $boundary, $key, $new_value);
            $body = $body.$tmp;
        }
    }
    $tmp = sprintf($multipart_end_fmt, $boundary);
    $body = $body.$tmp;
}

if __name__ == "__main__":
    dt = test()
    print dt
    sign = create_sign(dt, "abx23579436")
    dt['sign'] = sign
    print dt
    make_form_request_v2(dt, header, body)

