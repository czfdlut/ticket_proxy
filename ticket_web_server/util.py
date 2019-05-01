# -*- coding: UTF-8 -*-
import logging.config
import os
import yaml
import hashlib
from datetime import datetime
import json
from collections import OrderedDict
import time
import urllib.request
import http.client
import socket

def add_headers(self, headers, k, v):
    is_exist_kv = False
    for k ,v in headers.items():
        if k.lower() == k.lower():
            is_exist_kv = True

    if is_exist_kv:
        headers[k] = v

def sha256(url):
    m = hashlib.sha256()
    m.update(url)
    return m.hexdigest()

def validate_date_str(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except:
        return False

def logger_handler(keyword, logpath="log", debug=0):
    path = os.path.split(os.path.realpath(__file__))[0]
    os.chdir(path)
    os.chdir("./")

    with open('./conf/logging.yaml', 'r') as f:
        yaml_config = yaml.load(f)

    config  = json.dumps(yaml_config)
    config = config.replace("XXXXX", keyword)
    jconfig = json.loads(config)

    rkeyword = u"app_%s" % keyword
    jconfig["handlers"][rkeyword]["filename"] = os.path.join(logpath, keyword + ".log")
    if debug == 1:
        jconfig["loggers"][keyword]["handlers"].append("console")

    logging.config.dictConfig(jconfig)

    return logging.getLogger(keyword)

def get_notify_token(secret_key, _id):
    timestampe = int(time.time())
    params = OrderedDict({"_id":_id, "limit": "inster_conf", "time": timestampe})
    lst = sorted(params.items(), key=lambda item: item[0])
    reqest_param = OrderedDict(lst)

    md5_data = ""
    for key in reqest_param.keys():
        md5_data = md5_data + str(reqest_param[key])
    sign = md5(md5_data + secret_key)
    return sign, timestampe

def md5(url):
    m = hashlib.md5(url)
    return m.hexdigest()

def request_query(url, headers={}, data=None, timeout=30):
    try:
        req = urllib.request.Request(url)
        for k, v in headers.items():
            req.add_header(k, v)
        resp = urllib.request.urlopen(req, data=data, timeout=timeout)
        return resp.info(), resp.read(), resp.getcode(), None
    except (urllib.request.HTTPError, http.client.HTTPException) as err:
        return None, None, None, err.read()
    except (socket.error, socket.timeout) as err:
        return None, None, None, str(err)
    except Exception as err:
        return None, None, None, str(err)
