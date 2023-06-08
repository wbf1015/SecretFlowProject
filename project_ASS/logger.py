import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.DEBUG)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

memory_logger = []

def make_StartInfo_Logger(mylog):
    logger.info(mylog)
    memory_logger.append('StartInfo')
    memory_logger.append(mylog)
    
def make_WebInfo_Logger(mylog):
    logger.info(mylog)
    memory_logger.append('WebInfo')
    memory_logger.append(mylog)

def make_ABY3_Logger(mylog):
    logger.info(mylog)
    memory_logger.append('ABY3Info')
    memory_logger.append(mylog)

def make_ASS_Logger(mylog):
    logger.info(mylog)
    memory_logger.append('ASSInfo')
    memory_logger.append(mylog)

'''
How to make your own message record: 
logger.debug
logger.info
logger.warning
logger.error
logger.critical
'''

def getLogger():
    return logger