from flask import Flask
import requests
from flask import request
import os
from datetime import datetime
from time import sleep
from random import randrange
import logging

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)

helloHost = os.environ.get('HELLO_HOST', "localhost")
worldHost = os.environ.get('WORLD_HOST', "localhost")
worldHostRuby = os.environ.get('WORLD_HOST_RUBY', "localhost")
worldPort = '5002'
# endpoint  = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', "localhost")
shard = os.environ.get('SHARD', "na")
print(" [frontend: " + shard + "] - " + " initialized]")

def which_world():
    global worldHost
    global worldHostRuby
    global worldPort
    r = randrange(100)
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(timeString + " - [frontend: " + shard + "] - " + " random=" + str(r))
    if r > 49:
        return worldHostRuby, '5003'
    else: 
        return worldHost, '5002'

@app.route("/")
def front_end():
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    # res = " - [frontend: " + shard + " ]- hello host: " + helloHost + " ]"
    res = " - [frontend: " + shard + "]"
    try:
        resH = requests.get('http://' + helloHost + ':5001')
        if resH.status_code >= 300:
            res += " hello status: " + str(resH.status_code) + " - " + resH.text 
        else:
            res += " hello status: " + str(resH.status_code) + " - " + resH.text 
    except Exception as e:
        res += " hello status: " + repr(e)

    try: 
        lHost, lPort = which_world()
        resW = requests.get('http://' + lHost + ':' + lPort)
        
        if resW.status_code >= 300:
            res += " | world status: " + str(resW.status_code) + " - " + resW.text + " - " + " | worldHost: " + worldHost
        else:
            res += " | world status: " + str(resW.status_code) + " - " + resW.text 
    except Exception as e:
        res += " world status:" + repr(e)

    print (timeString + res)
    return res