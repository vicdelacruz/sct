'''
Created on Oct 16, 2018

@author: victord
'''
import random
from sct.logger.sctLogger import SctLogger
from sct.spi.spiDriver import Driver

class Ads8638:
    '''
    Models the ADS8638 voltage ADC in the SCT board
    '''
    logger = SctLogger().getLogger(__name__)
    rangeStart = -5.0
    rangeStop = 5.0
    rangeSteps = 2**12
    rangeResolution = (rangeStop - rangeStart)/rangeSteps

    CHIPSEL = 0x2 #Device #2
    FREQUENCY = 1000000 # 1MHz baud rate 
    RANGESEL = 0b010 #Range Select
    TSENSESEL = 0b0 #Temp Sensor Select
    MANUALMODE = 0x40 #Manual mode
    AUTOMODE = 0x50 #Auto mode

    def __init__(self):
        '''
        Default settings
        '''
        self.states = {
            #Holds the 12-bit ADC serial readout 
            'digOut': 0b_1011_1010_1101, #BAD
            #Input Select - integer var
            'muxSel': 0x1,
        }
        #8 Analog inputs 
        self.ins = {
            'power'  : 0x0,
            'unused1': 0x1,
            'unused2': 0x2,
            'unused3': 0x3,
            'unused4': 0x4,
            'unused5': 0x5,
            'unused6': 0x6,
            'io'     : 0x7
        }
        self.driver = None
        self.logger.debug("ADS8638 has been instantiated")

    def initCfg(self, driver):
        self.driver = driver
        #Ads8638 ADC voltage measure
        self.sendBytes([0x01, 0x00]) #Reset disable
        self.sendBytes([0x06, 0x0C]) #AL_PD=1, IntVREF=1, TempSense=0
        self.sendBytes([0x0C, 0x81]) #Automode on Ch0 and Ch7 only
        self.sendBytes([0x10, 0x22]) #Range 010
        self.sendBytes([0x11, 0x22]) #Range 010
        self.sendBytes([0x12, 0x22]) #Range 010
        self.sendBytes([0x13, 0x22]) #Range 010
        
    def setMux(self, testType):
        muxSel = self.ins.get(testType)
        if self.validateMux(muxSel):
            self.states['muxSel'] = muxSel
            self.logger.debug("ADS8638 updating muxSel={:#x} ({})".format(
                muxSel, testType))
            return True
        else:
            return False
        
    def validateMux(self, muxVal):
        valid = True
        cond = [
                muxVal < 0x0, #0x0 to 0x7 only
                (muxVal > 0x0 and muxVal < 0x7), #0x0 and 0x7 only
                muxVal > 0x7, #up to 8 AI selections in ADS8638
                ]
        if any(cond): 
            valid = False
            self.logger.error("Invalid condition({}) with ({}) ".format(cond.index(True), muxVal))
        return valid
        
    def readAdc(self, testType):
        #Set AIN
        self.setMux(testType)
        #Set Manual Cfg
        lnib = (0x07 & self.states.get('muxSel'))
        rnib = ((0x07 & self.RANGESEL) << 1) | (0x01 & self.TSENSESEL) 
        lsb = (lnib << 4) | rnib
        self.sendBytes([self.MANUALMODE, lsb])
        #Read DigitalOut
        msb, lsb = self.getBytes()
        chByte = (0xF0 & msb) >> 4
        digitalOut = (0x0F & msb) << 8 | (lsb & 0xFF)
        self.states['digOut'] = digitalOut
        self.logger.debug("ADC digital out = {:#x} from port {:#x}".format(digitalOut, chByte))
        #Calc Vmeas
        return (chByte, self.getVmeas())

    def sendBytes(self, dBytes=[]):
        addr, data = dBytes 
        eff_addr = addr << 1
        self.driver.cfg_write(self.CHIPSEL, [eff_addr, data], self.FREQUENCY) 

    def getBytes(self):
        result = self.driver.cfg_read(self.CHIPSEL, [0x00, 0x00], self.FREQUENCY) 
        return result
        
    def getVmeas(self):
        analogOut = self.states.get('digOut') * self.rangeResolution + self.rangeStart
        self.states['anaOut'] = analogOut
        self.logger.debug("Calculated Vmeas out {:.4f} for {:#x}".format(analogOut, self.states.get('digOut')))
        return self.states['anaOut']
