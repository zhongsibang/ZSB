import logging
from logging.handlers import RotatingFileHandler

def getlogger(mod_name:str, filename:str, level=logging.INFO, propagate=False,
              maxBytes=10*1024*1024, backcount=5):
    logger = logging.getLogger(mod_name)
    logger.setLevel(level)
    logger.propagate = propagate

    handler = RotatingFileHandler(filename, maxBytes=maxBytes, backupCount=backcount, encoding='utf-8')
    handler.setLevel(level)
    formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s %(funcName)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger





