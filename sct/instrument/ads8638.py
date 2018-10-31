'''
Created on Oct 16, 2018

@author: victord
'''
import random
from sct.logger.sctLogger import SctLogger

class Ads8638(object):
    '''
    Models the ADS8638 voltage ADC in the SCT board
    '''
    logger = SctLogger().getLogger(__name__)
    rangeStart = -5.0
    rangeStop = 5.0
    rangeSteps = 2**12
    rangeResolution = (rangeStop - rangeStart)/rangeSteps

    def __init__(self):
        '''
        Default settings
        '''
        self.states = {
            #Holds the 12-bit ADC serial readout 
            'digOut': 0b_0000_0000_0000,
            #Represents the normalized Vmeas based on muxSel
            'anaOut': 0.0,
            #Input Select - integer var
            'muxSel': 0x0,
            #8 Analog inputs 
            'ins': {
                0x0: {'name': 'AIN0', 'analog': 0.0 },
                0x1: {'name': 'AIN1', 'analog': 0.0 },
                0x2: {'name': 'AIN2', 'analog': 0.0 },
                0x3: {'name': 'AIN3', 'analog': 0.0 },
                0x4: {'name': 'AIN4', 'analog': 0.0 },
                0x5: {'name': 'AIN5', 'analog': 0.0 },
                0x6: {'name': 'AIN6', 'analog': 0.0 },
                0x7: {'name': 'AIN7', 'analog': 0.0 },
            }
        }
        self.logger.debug("ADS8638 has been instantiated")
        
    def setMux(self, muxSel):
        if self.validateMux(muxSel):
            self.states['muxSel'] = muxSel
            aIn = random.uniform(self.rangeStart, self.rangeStop)
            self.states.get('ins').get(muxSel)['analog'] = aIn
            self.logger.debug("Random analog in = {:.4f}".format(aIn))
            self.logger.debug("ADS8638 settings updated muxSel={:#x} ({})".format(
                muxSel, self.states.get('ins').get(muxSel).get('name')) )
            return True
        else:
            return False
        
    def validateMux(self, muxVal):
        valid = True
        cond = [
                muxVal < 0x0, #0x0 to 0x7 only
                muxVal > 0x7, #up to 8 AI selections in ADS8638
                ]
        if any(cond): 
            valid = False
            self.logger.error("Invalid condition({}) with ({}) ".format(cond.index(True), muxVal))
        return valid
        
    def readAdc(self):
        muxSel = self.states.get('muxSel')
        analogIn = self.states.get('ins').get(muxSel).get('analog')
        digitalOut = int((analogIn - self.rangeStart)/self.rangeResolution)
        if (digitalOut==self.rangeSteps):
            self.logger.warning("Max count reached, scaling back by 0x1...")
            digitalOut = self.rangeSteps -1
        self.states['digOut'] = digitalOut
        self.logger.debug("ADC analog in = {:.4f} for {}".format(analogIn, self.states.get('ins').get(muxSel).get('name')))
        self.logger.debug("ADC digital out = {:#x} with {:.4f} resolution".format(digitalOut, self.rangeResolution))
        return digitalOut
    
    def getVmeas(self):
        analogOut = self.states.get('digOut') * self.rangeResolution + self.rangeStart
        self.states['anaOut'] = analogOut
        self.logger.debug("Calculated Vmeas out {:.4f} for {:#x}".format(analogOut, self.states.get('digOut')))
        return self.states['anaOut']

        