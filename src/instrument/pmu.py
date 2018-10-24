'''
Created on 8 Apr 2018

@author: BIKOYPOGI
'''

from logger.sctLogger import SctLogger
from instrument.max7301 import Max7301
from instrument.max5322 import Max5322
from instrument.ads8638 import Ads8638
from instrument.mc33996 import Mc33996

class Pmu:
    '''
    Tester currently supports Pmu IFVM mode only.
    
    Attributes:
        testref    The name of the TestRef that needs the measurement
        result     Result of this Pmu measurement (in V)
    '''
    logger = SctLogger(__name__).getLogger()

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
            'IO': 0b_001_00000_00000 ,
            'power': 0b_0000_0000_0000_0001
        }

    def getMeas(self, testType, singleChannel, singleParam):
        intChannel = int(singleChannel)
        self.logger.debug("Pmu test type {} for channel {} at setpoint={}...".format(testType, singleChannel, singleParam))
        self.setMax5322(testType, singleParam)
        self.setMax7301(testType, intChannel, 0x401)
        self.setAds8638(0x7)
        self.setMc33996(testType, intChannel)
        result = self.ads8638.readAdc()
        self.states[testType] = singleChannel
        self.logger.debug("States: IO: {:#015b}, power: {:#018b}".format(self.states.get('IO'), self.states.get('power')))
        return result
    
    def setMax5322(self, testType, singleParam):
        try:
            self.max5322.setIForce(testType, singleParam)
        except ValueError as e:
            self.logger.exception("Set Max5322 unsuccessful: {}...", e.message)
    
    def setMax7301(self, testType, channelSelect, ctrl):
        try:
            self.max7301.setPorts(testType, channelSelect, ctrl)
        except ValueError as e:
            self.logger.exception("Set Max7301 unsuccessful: {}...", e.message)
                        
    def setAds8638(self, muxSel):
        try:
            self.ads8638.setMux(muxSel)
        except ValueError as e:
            self.logger.exception("Set ADS8638 unsuccessful: {}...", e.message)
            
    def setMc33996(self, testType, relaySel):
        try:
            self.mc33996.selectPort(testType, relaySel)
        except ValueError as e:
            self.logger.exception("Set MC33996 unsuccessful: {}...", e.message)
            
