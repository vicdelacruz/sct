'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
import logging
import os
from resources import props
from logging.handlers import RotatingFileHandler

class Singleton:
    logger = {}
    
    def __init__(self):
        self.__dict__ = self.logger
    
class SctLogger(Singleton):
    '''
    This is the custom logger for the SCT app
    '''
    logLevel = {
        0: logging.DEBUG,
        1: logging.INFO,
        2: logging.WARNING,
        3: logging.ERROR,
        4: logging.CRITICAL
    }

    def __init__(self, name):
        '''
        Constructor
        '''
        Singleton.__init__(self)
        self.logger['sctLogger'] = self.createInstance(name)
        
    def getLogger(self):
        return self.logger['sctLogger']

    def createInstance(self, name):
        logger = logging.getLogger(name)
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d %(levelname)-8s %(name)-22s %(message)s",
            "%Y-%m-%d %H:%M:%S")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if (props.logToFile):
            fhandler = RotatingFileHandler(
                filename=os.path.join(props.logDir, props.logFile),
                maxBytes=100000, backupCount=5)
            fhandler.setFormatter(formatter)
            logger.addHandler(fhandler)
        logger.setLevel(self.logLevel.get(props.logLevel, "Invalid log level"))
        return logger
    
