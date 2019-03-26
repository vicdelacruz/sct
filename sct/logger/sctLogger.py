'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from sct.resources import props

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

    def __init__(self):
        '''
        Constructor
        '''
        Singleton.__init__(self)
        self.logger['sctLogger'] = self.createInstance()
        
    def getLogger(self, name):
        return self.logger['sctLogger'].getChild(name)

    def createInstance(self):
        logger = logging.getLogger()
        while(logger.handlers):
            handler = logger.handlers.pop()
            handler.close()
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d [%(levelname)-8s][%(name)-25s] %(message)s",
            "%Y-%m-%d %H:%M:%S")
        if (props.logToConsole):
            stdHandler = logging.StreamHandler(sys.stdout)
            stdHandler.setLevel(logging.DEBUG)
            stdHandler.addFilter(lambda record: record.levelno <= logging.INFO)
            stdHandler.setFormatter(formatter)
            logger.addHandler(stdHandler)
        errHandler = logging.StreamHandler()
        errHandler.setLevel(logging.WARNING)
        errHandler.setFormatter(formatter)
        logger.addHandler(errHandler)
        if (props.logToFile):
            fhandler = RotatingFileHandler(
                filename=os.path.join(props.logDir, props.logFile),
                maxBytes=10000000, backupCount=5)
            fhandler.setFormatter(formatter)
            logger.addHandler(fhandler)
        logger.setLevel(self.logLevel.get(props.logLevel, "Invalid log level"))
        return logger
    
