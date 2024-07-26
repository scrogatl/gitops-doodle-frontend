from flask import Flask
import requests
from flask import request
import os
from datetime import datetime
from time import sleep
import os

app = Flask(__name__)

helloHost = os.environ.get('HELLO_HOST', "localhost")
worldHost = os.environ.get('WORLD_HOST', "localhost")
endpoint  = os.environ.get('OTEL_EXPORTER_OTLP_ENDPOINT', "localhost")
shard = os.environ.get('SHARD', "na")
print(" [frontend: " + shard + "] - " + " initialized]")



@app.route("/")
def front_end():
    timeString = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    resLocal = timeString 
    res = " - [frontend: " + shard + " - hello host: " + helloHost + " ]"
    try:
        resH = requests.get('http://' + helloHost + ':5001')
        if resH.status_code >= 300:
            res += " hello status: " + str(resH.status_code) + " - " + resH.text 
        else:
            res += " hello status: " + str(resH.status_code) + " - " + resH.text 
    except Exception as e:
        res += " hello status: " + repr(e)

    try: 
        resW = requests.get('http://' + worldHost + ':5002')
        if resW.status_code >= 300:
            res += " | world status: " + str(resW.status_code) + " - " + resW.text + " - " + " | worldHost: " + worldHost
        else:
            res += " | world status: " + str(resW.status_code) + " - " + resW.text 
    except Exception as e:
        res += " world status:" + repr(e)


    print (resLocal + res)
    return res