'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from lxml import etree
from sct.instrument.pmu import Pmu
from sct.instrument.lookup import Lookup
from sct.logger.sctLogger import SctLogger
import time

class Tests():
    '''
    classdocs
    '''
    logger = SctLogger().getLogger(__name__)
    meas = None
    formatting = {
        'power': '{:02d}',     
        'io': '{:04d}',
    }

    def __init__(self):
        '''
        Constructor
        '''
        self.pmu = Pmu() #PMU instantiation
        self.lookup = Lookup() #Import the lookup table
        self.logger.debug('Tests Controller is initialized...')
        
    def getGroupResults(self, testType, tests, groupName, pins):
        self.logger.info('Group {}({}): {}'.format(groupName, testType, list(pins.values())))
        testResults = etree.Element('Results')
        self.logger.debug('Keys =  {}'.format(pins.keys()))
        for ch in self.lookup.channelMap.get(testType).keys():
            if ch in pins.keys():
                mappedChannel = self.lookup.decode(testType, ch)
                pinName = pins.get(ch)
                self.logger.debug('Getting result for pin {} on channel {:s}...'.format(pinName, ch))
                pinMeas = etree.Element('Pin', name=pinName)
                pinMeas.text = ''
                for i, param in enumerate(tests):
                    self.pmu.setup(testType, mappedChannel, param)
                    pinMeas.text += '{:.02f}'.format(self.pmu.getMeas())
                    if i<len(tests)-1:
                        pinMeas.text += '|'
                testResults.append(pinMeas)
        self.logger.debug(etree.tostring(testResults))
        return testResults    
    
    def getPinResults(self, tests, pin):
        self.meas = etree.Element('Pin', name=pin)
        self.meas.text = ''
        for i, param in enumerate(tests):
            time.sleep(0.0005)
            self.meas.text += self.pmu.getMeas(pin, param)
            if i<len(tests)-1:
                self.meas.text += '|'
        self.logger.debug(etree.tostring(self.meas))
        return self.meas        
