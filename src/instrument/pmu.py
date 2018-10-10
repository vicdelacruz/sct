'''
Created on 8 Apr 2018

@author: BIKOYPOGI
'''
from time import sleep
from lxml import etree
import random
from logger.sctLogger import SctLogger

class Pmu:
    '''
    Tester currently supports Pmu IFVM mode only.
    
    Attributes:
        testref    The name of the TestRef that needs the measurement
        result     Result of this Pmu measurement (in V)
    '''
    logger = SctLogger(__name__).getLogger()

    def __init__(self, tests, pin):
        '''
        Constructor
        '''
        self.tests = tests #params
        self.pin = pin
        self.meas = etree.Element('Pin', name=pin)
        
    def get(self):
        self.logger.debug('Pmu test for %s...', self.pin)
        self.meas.text = ''
        for i, param in enumerate(self.tests):
#             sleep(1)
            self.meas.text += self.getMeas(self.pin, param)
            if i<len(self.tests)-1:
                self.meas.text += '|'
        self.logger.debug(etree.tostring(self.meas))
        return self.meas

    def getMeas(self, singlePin, singleParam):
        self.logger.debug('Pmu test for %s at setpoint=%s...', singlePin, singleParam)
        result = random.random()*3
        return "{:.2f}".format(result)
