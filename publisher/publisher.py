
import logging
import sys
import time
from logging.handlers import TimedRotatingFileHandler
import paho.mqtt.client as mqtt_client
import random
import requests
import http.client
from hashlib import md5


FORMATTER_STRING = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
FORMATTER = logging.Formatter(FORMATTER_STRING)
LOG_FILE = "/tmp/my_app.log" # use fancy libs to make proper temp file

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)

    return logger
logger = get_logger("publisher_logger")
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
my_ip=md5(str(conn.getresponse().read().decode('utf-8')).encode('utf-8')).hexdigest()

broker="broker.emqx.io"

#client = mqtt_client.Client('isu10012300')
# FOR new version change ABOVE line to 
res = requests.get('http://158.160.58.203:8000/get_id')

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.fatal("Failed to connect, return code %d\n", rc)

client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION1, 
    res.json()["id"]
)
client.on_connect=on_connect
logger.info("Connecting to broker"+" "+str(broker))
logger.debug(str(client.connect(broker)))
client.loop_start()
logger.info("Publishing started")

for i in range(10):
    state = "onPech" if random.randint(0,1)==0 else "offPech"
    state=state+" - machine - "+res.json()["id"]
    logger.info("state is "+state+" - machine "+ res.json()['id']+" - host = "+my_ip)
    client.publish("lab/leds/state", state)
    time.sleep(2)
    
client.disconnect()
logger.info("Publishing is ended")
client.loop_stop()