'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
import logging
from logging.config import dictConfig

class SctLogger(object):
    '''
    classdocs
    '''
    logger = None
    logLevel = {
        0: logging.DEBUG,
        1: logging.INFO,
        2: logging.WARNING,
        3: logging.ERROR,
        4: logging.CRITICAL
    }

    def __new__(cls, name, level = 0):
        if not hasattr(cls, name):
            cls.name= super(SctLogger, cls).__new__(cls)
            cls.name.logger = cls.name.createInstance(name, level)
            print("New Sct Logger", cls.name)
        return cls.name

    def createInstance(self, name, level):
        '''
        Constructor
        '''
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(name)-20s %(levelname)-8s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(self.logLevel.get(level, "Invalid log level"))
        print("Created instance", logger)
        return logger
