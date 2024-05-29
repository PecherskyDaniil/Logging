from fastapi import FastAPI
from hashlib import md5
from datetime import datetime
import logging
import sys
import time
from logging.handlers import TimedRotatingFileHandler
app = FastAPI()

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

logger = get_logger("serverid_logger")
logger.debug("Server is started!")
@app.get("/get_id")
async def get_id():
    newid="Pech"+str(md5(str(datetime.now()).encode("utf8")).hexdigest())
    logger.info("getting id '"+newid+"'")
    return {"id": newid}