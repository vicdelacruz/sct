'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from lxml import etree
from instrument.pmu import Pmu
from instrument.lookup import Lookup
from logger.sctLogger import SctLogger

class Tests():
    '''
    classdocs
    '''
    logger = SctLogger(__name__).getLogger()
    meas = None
    pinMap = {}
    formatting = {
        'power': '{:02d}',     
        'IO': '{:04d}',
    }

    def __init__(self):
        '''
        Constructor
        '''
        self.pmu = Pmu() #PMU instantiation
        self.lookup = Lookup() #Import the lookup table
        self.logger.debug('Tests Controller is initialized...')
        
    def getGroupResults(self, testType, tests, pins):
        self.logger.debug('PinMap: {}'.format(self.pinMap))
        self.logger.debug('{} {} {}'.format(testType, tests, pins))
        groupName = next(iter(pins))
        testResults = etree.Element('Results')
        self.logger.debug('Group name is {}'.format(groupName))
        self.logger.debug('Keys =  {}'.format(pins.get(groupName).keys()))
        for ch in self.lookup.channelMap.get(testType).keys():
            if ch in pins.get(groupName).keys():
                mappedChannel = self.lookup.decode(testType, ch)
                pinName = pins.get(groupName).get(ch)
                self.logger.debug('Getting result for pin {} on channel {:s}...'.format(pinName, ch))
                pinMeas = etree.Element('Pin', name=pinName)
                pinMeas.text = ''
                for i, param in enumerate(tests):
                    pinMeas.text += self.pmu.getMeas(testType, mappedChannel, param)
                    if i<len(tests)-1:
                        pinMeas.text += '|'
                testResults.append(pinMeas)
        self.logger.debug(etree.tostring(testResults))
        return testResults    
    
    def getPinResults(self, tests, pin):
        self.meas = etree.Element('Pin', name=pin)
        self.meas.text = ''
        for i, param in enumerate(tests):
            self.meas.text += self.pmu.getMeas(pin, param)
            if i<len(tests)-1:
                self.meas.text += '|'
        self.logger.debug(etree.tostring(self.meas))
        return self.meas        