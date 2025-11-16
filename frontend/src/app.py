from flask import Flask
import requests
from flask import request
import os
from datetime import datetime
from time import sleep
from random import randrange
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.DEBUG)

app = Flask(__name__)

helloHost      = os.environ.get('HELLO_HOST', "localhost")
worldHost      = os.environ.get('WORLD_HOST', "localhost")
worldHostRuby  = os.environ.get('WORLD_HOST_RUBY', "localhost")
worldPort      = os.environ.get('WPORT', "5002")
worldPortRuby  = os.environ.get('WPORT_RUBY', "5002")
shard          = os.environ.get('SHARD', "na")
rubyWorld      = os.environ.get('RUBY_WORLD', "50")
az_dns_suffix  = os.environ.get('CONTAINER_APP_ENV_DNS_SUFFIX')


def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.info(timeString + " - [frontend: " + shard + "] - " + message)
    
def generate_acct_num():
    r = randrange(10000)
    return str(r) 

def which_world_to_call():
    r = randrange(100)
    if r < int(rubyWorld):
        logit("world-ruby")
        return worldHostRuby, worldPortRuby
    else: 
        logit("world-python")
        return worldHost, worldPort

@app.route("/")
def front_end():
    httpStatus = 200
    req_url_hello = ""
    req_url_world = ""
    res = ''

    if az_dns_suffix:
        req_url_hello = "https://" + helloHost + ".internal." + az_dns_suffix
    else:
        req_url_hello = 'http://' + helloHost + ':5001' + "?account=" + generate_acct_num()
    try:
        print(f"Attempting to connect to hello host at {req_url_hello}")
        resH = requests.get(req_url_hello)
        httpStatus = resH.status_code
        res += "hello status: " + str(resH.status_code) + " - " + resH.text 
    except Exception as e:
        res += "hello status: " + repr(e)

    try: 
        if az_dns_suffix:
            req_url_world =  "https://" + worldHost + ".internal." + az_dns_suffix
        else: 
            lHost, lPort = which_world_to_call()
            logit(lHost + ":" + lPort)
            req_url_world = 'http://' + lHost + ':' + lPort
        print(f"Attempting to connect to world host at {req_url_world}")
        resW = requests.get(req_url_world)
        httpStatus = resW.status_code
        res += " | world status: " + str(resW.status_code) + " - " + resW.text 
    except Exception as e:
        httpStatus = 500
        res += " world status: " + repr(e)

    logit (res)
    return res,  httpStatus

