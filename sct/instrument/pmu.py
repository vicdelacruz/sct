'''
Created on 8 Apr 2018

@author: BIKOYPOGI
'''

from sct.logger.sctLogger import SctLogger
from sct.instrument.max7301 import Max7301
from sct.instrument.max5322 import Max5322
from sct.instrument.ads8638 import Ads8638
from sct.instrument.mc33996 import Mc33996
from sct.spi.spiDriver import Driver

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
        self.driver = Driver()
        self.initDevices()

    def initDevices(self):
        self.driver.spiCfg.printVals()
        self.driver.gpioCfg.printVals()
        self.initConfig(self.max7301) #Max7301 port controllers
        self.initConfig(self.max5322) #Max5322 DAC voltage driver
        self.initConfig(self.ads8638) #Ads8638 ADC voltage measure
        self.initConfig(self.mc33996) #MC33996 power relay mux

    def setup(self, testType, singleChannel, singleParam):
        if self.states.get(testType).get('pinSelect') != singleChannel:
            self.states.get(testType)['pinSelect'] = singleChannel
            self.setMax7301(testType, singleChannel, 0x401)
            self.setMc33996(testType, singleChannel)
        self.setMax5322(testType, singleParam)
        self.logger.debug("Pmu tests type {} for channel {} at setpoint={}...".format(
            testType, singleChannel, singleParam))

    def getMeas(self, testType):
        muxSel = self.states.get(testType).get('adcChannel')
        (chByte, result) = self.getAds8638(muxSel)
        self.resetMax5322() #Prevent hot-switching
        self.logger.debug("ChByte: {} ADCOut: {} for Mux Sel: {}...".format(chByte, result, muxSel))
        return result

    def initConfig(self, component):
        try:
            component.initCfg(self.driver)
        except ValueError as e:
            self.logger.exception("Unable to init {} ...", component)

    def setMax5322(self, testType, singleParam):
        try:
            self.max5322.setIForce(testType, singleParam)
        except ValueError as e:
            self.logger.exception("Set Max5322 unsuccessful: {}...", e)

    def resetMax5322(self):
        try:
            self.max5322.resetIForce()
        except ValueError as e:
            self.logger.exception("Reset Max5322 unsuccessful: {}...", e)

    def setMax7301(self, testType, channelSelect, ctrl):
        try:
            self.max7301.setPorts(testType, channelSelect, ctrl)
        except ValueError as e:
            self.logger.exception("Set Max7301 unsuccessful: {}...", e)
                        
    def getAds8638(self, muxVal):
        try:
            result = self.ads8638.readAdc(muxVal)
            return result
        except ValueError as e:
            self.logger.exception("Get ADS8638 unsuccessful: {}...", e)
            
    def setMc33996(self, testType, relaySel):
        try:
            self.mc33996.selectPort(testType, relaySel)
        except ValueError as e:
            self.logger.exception("Set MC33996 unsuccessful: {}...", e)
            
