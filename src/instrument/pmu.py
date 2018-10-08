'''
Created on 8 Apr 2018

@author: BIKOYPOGI
'''
from time import sleep
from lxml import etree
from logger.sctLogger import SctLogger

class Pmu:
    '''
    Tester currently supports Pmu IFVM mode only.
    
    Attributes:
        testref    The name of the TestRef that needs the measurement
        result     Result of this Pmu measurement (in V)
    '''
    logger = SctLogger(__name__).getLogger()

    def __init__(self, test, pins):
        '''
        Constructor
        '''
        self.test = test #Element type
        self.pins = pins
        self.meas = etree.Element('Result')
        
    def get(self):
        for pin in self.pins:
            self.logger.info(pin)
            sleep(1)
            self.getMeas(pin)
        return self.meas
    

    def getMeas(self, singlePin):
        etree.SubElement(self.meas, 'Measurement', Pin=singlePin, Meas='0.75') #Mock
        
