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

helloHost     = os.environ.get('HELLO_HOST', "localhost")
worldHost     = os.environ.get('WORLD_HOST', "localhost")
worldHostRuby = os.environ.get('WORLD_HOST_RUBY', "localhost")
worldPort     = os.environ.get('WPORT', "5002")
worldPortRuby = os.environ.get('WPORT_RUBY', "5002")
shard = os.environ.get('SHARD', "na")

def logit(message):
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    print(timeString + " - [frontend: " + shard + "] - " + message)

logit("worldHost: " + worldHost )
logit("worldPort: " + worldPort)
logit("worldHostRuby: " + worldHostRuby )
logit("worldPortRuby: " + worldPortRuby)
logit( "initialized")


def which_world():
    r = randrange(100)
    logit("random = " + str(r))
    if r > 49:
        return worldHostRuby, worldPortRuby
    else: 
        return worldHost, worldPort

@app.route("/")
def front_end():
    # logit("handling /")
    res = ""
    try:
        resH = requests.get('http://' + helloHost + ':5001')
        if resH.status_code >= 300:
            res += "hello status: " + str(resH.status_code) + " - " + resH.text 
        else:
            res += "hello status: " + str(resH.status_code) + " - " + resH.text 
    except Exception as e:
        res += "hello status: " + repr(e)

    try: 
        lHost, lPort = which_world()
        logit(lHost + ":" + lPort)
        resW = requests.get('http://' + lHost + ':' + lPort)
        if resW.status_code >= 300:
            res += " | world status: " + str(resW.status_code) + " - " + resW.text + " - " + " | worldHost: " + worldHost
        else:
            res += " | world status: " + str(resW.status_code) + " - " + resW.text 
    except Exception as e:
        res += " world status:" + repr(e)

    logit (res)
    return res