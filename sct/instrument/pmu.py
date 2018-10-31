'''
Created on 8 Apr 2018

@author: BIKOYPOGI
'''

from sct.logger.sctLogger import SctLogger
from sct.instrument.max7301 import Max7301
from sct.instrument.max5322 import Max5322
from sct.instrument.ads8638 import Ads8638
from sct.instrument.mc33996 import Mc33996

class Pmu:
    '''
    Tester currently supports Pmu IFVM mode only.
    
    Attributes:
        testref    The name of the TestRef that needs the measurement
        result     Result of this Pmu measurement (in V)
    '''
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        '''
        Constructor
        '''
        self.max7301 = Max7301() #IO channel mux select
        self.max5322 = Max5322() #Force DAC
        self.ads8638 = Ads8638() #Measurement ADC
        self.mc33996 = Mc33996() #Power relay select
        self.meas = None
        self.states = {    
            'io': { 'pinSelect': 0b_001_00000_00000, 'adcChannel': 0x0 },
            'power': { 'pinSelect': 0b_0000_0000_0000_0001, 'adcChannel': 0x7 },
        }

    def setup(self, testType, singleChannel, singleParam):
        self.states.get(testType)['pinSelect'] = singleChannel
        self.setMax5322(testType, singleParam)
        self.setMax7301(testType, singleChannel, 0x401)
        self.setMc33996(testType, singleChannel)
        self.setAds8638(self.states.get(testType).get('adcChannel'))
        self.ads8638.readAdc()
        self.logger.debug("Pmu tests type {} for channel {} at setpoint={}...".format(
            testType, singleChannel, singleParam))
    
    def getMeas(self):
        result = self.ads8638.getVmeas()
        self.logger.debug("States: io: {:#015b}, power: {:#018b}".format(
            self.states.get('io').get('pinSelect'), self.states.get('power').get('pinSelect')))
        return result
    
    def setMax5322(self, testType, singleParam):
        try:
            self.max5322.setIForce(testType, singleParam)
        except ValueError as e:
            self.logger.exception("Set Max5322 unsuccessful: {}...", e)
    
    def setMax7301(self, testType, channelSelect, ctrl):
        try:
            self.max7301.setPorts(testType, channelSelect, ctrl)
        except ValueError as e:
            self.logger.exception("Set Max7301 unsuccessful: {}...", e)
                        
    def setAds8638(self, muxSel):
        try:
            self.ads8638.setMux(muxSel)
        except ValueError as e:
            self.logger.exception("Set ADS8638 unsuccessful: {}...", e)
            
    def setMc33996(self, testType, relaySel):
        try:
            self.mc33996.selectPort(testType, relaySel)
        except ValueError as e:
            self.logger.exception("Set MC33996 unsuccessful: {}...", e)
            
