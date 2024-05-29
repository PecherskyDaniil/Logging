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
LOG_FILE = "/tmp/my_app.log"

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

logger = get_logger("subscriber_logger")

broker="broker.emqx.io"
res=requests.get('http://158.160.58.203:8000/get_id')
conn = http.client.HTTPConnection("ifconfig.me")
conn.request("GET", "/ip")
my_ip=md5(str(conn.getresponse().read().decode('utf-8')).encode('utf8')).hexdigest()

def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker!")
        else:
            logger.fatal("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, message):
    last_timestamp = time.time()
    time.sleep(1)
    data = str(message.payload.decode("utf-8"))
    logger.info("received message ="+" '"+ data+"' - machine -"+res.json()["id"] + " - host = "+my_ip)

#client = mqtt_client.Client('isu112230')
# FOR new version change ABOVE line to 
client = mqtt_client.Client(
    mqtt_client.CallbackAPIVersion.VERSION1, 
    res.json()["id"]
)

client.on_message=on_message
client.on_connect = on_connect

logger.debug("Connecting to broker"+" "+broker)
client.connect(broker) 
client.loop_start() 
logger.info("Subcribing is started")
client.subscribe("lab/leds/state")
last_timestamp=time.time()
for i in range(45):
    cur_time=time.time()
    if cur_time-last_timestamp>30:
        logger.warning("No messages!")
        last_timestamp=time.time()
    time.sleep(2)
client.disconnect()
logger.info("Subscribing is ended")
client.loop_stop()
