'''
Created on Oct 16, 2018

@author: victord
'''
import random
from logger.sctLogger import SctLogger

class Ads8638(object):
    '''
    Models the ADS8638 voltage ADC in the SCT board
    '''
    logger = SctLogger(__name__).getLogger()
    rangeStart = -5.0
    rangeStop = 5.0
    rangeStep = 2**12
    rangeResolution = (rangeStop - rangeStart)/rangeStep

    def __init__(self):
        '''
        Default settings
        '''
        #Holds the 12-bit ADC serial readout 
        self.out = 0b_0000_0000_0000
        
        #Input Select - integer var
        self.ins = {
            0x0: 'AIN0',
            0x1: 'AIN1',
            0x2: 'AIN2',
            0x3: 'AIN3',
            0x4: 'AIN4',
            0x5: 'AIN5',
            0x6: 'AIN6',
            0x7: 'AIN7'
            }
        self.muxSel = 0x0
        
        self.logger.debug("ADS8638 has been instantiated")
        
    def setMux(self, muxSel):
        if self.validateMux(muxSel):
            self.muxSel = muxSel
            self.logger.debug("ADS8638 settings updated muxSel={:#x} ({})".format(muxSel, self.ins.get(muxSel)))
            return True
        else:
            return False
        
    def validateMux(self, muxVal):
        valid = True
        if any([
                muxVal < 0x0, #0x0 to 0x7 only
                muxVal > 0x7, #up to 8 AI selections in ADS8638
                ]): 
            valid = False
            self.logger.exception("Mux select validation failed!!!")
            self.logger.debug("Mux Select = {:#x} {}".format(muxVal, str(muxVal > 0x7 or muxVal < 0x0)))
        return valid
        
    def readAdc(self):
        adcOut = random.randrange(0, self.rangeStep)
        result = self.rangeStart + self.rangeResolution * adcOut
        strResult = "{:.2f}".format(result)
        self.logger.debug("ADC out = {:#x}".format(adcOut))
        self.logger.debug("Voltage out = {} with {:.4f} resolution".format(strResult, self.rangeResolution))
        return strResult

        