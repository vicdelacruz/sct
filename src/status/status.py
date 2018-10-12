'''
Created on Oct 12, 2018

@author: victord
'''

from logger.sctLogger import SctLogger
from resources import props

class Singleton:
    status = {}

    def __init__(self):
        self.__dict__ = self.status   
        
class Status(Singleton):
    '''
    This is a simple class that reflects the current SCT status
    '''
    logger = SctLogger(__name__).getLogger()
    logFile = props.statusFile
    logDir = props.logDir
    stat = {
        'invalid': 'INVALID',
        'waiting': 'WAITING',
        'loading': 'LOADING',
        'testing': 'TESTING'
    }

    def __init__(self):
        '''
        Constructor
        '''
        Singleton.__init__(self)
        self.status['state'] = self.updateState('invalid')
        
    def getState(self):
        return self.status['state']

    def updateState(self, newState):
        if self.status.get('state') != self.stat.get(newState):
            self.status['state'] = self.stat.get(newState, "Invalid_state")
            self.logger.debug('SCT state updated to %s ...', self.getState())
        return self.getState()
    