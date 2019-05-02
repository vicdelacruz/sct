'''
Created on Oct 16, 2018

@author: victord
'''
import statistics, time
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
    RESETSEQ = 0b1 #Reset the channel sequence counter (1: true, 0: false)
    RANGESEL = 0b010 #Range Select
    TSENSESEL = 0b0 #Temp Sensor Select
    MANUALMODE = 0x04 #Manual mode
    AUTOMODE = 0x05 #Auto mode
    CHANNELMODE = 'AUTO' #Channel Selection Mode AUTO or MANUAL

    SAMPLE_DELAY = 0.020 #Delay before reading value
    SAMPLE_SIZE = 5 #Remove spurious ADC readouts
    SIGMA_LIMIT = 2 #Filter outside of this n-sigma
    TIGHT_ITER = 2 #Number of loops to remove min and max from data

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
            'unused0': {'muxSel': 0x0, 'autoSel': 0x80},
            'unused1': {'muxSel': 0x1, 'autoSel': 0x40},
            'power'  : {'muxSel': 0x2, 'autoSel': 0x20},
            'unused3': {'muxSel': 0x3, 'autoSel': 0x10},
            'unused4': {'muxSel': 0x4, 'autoSel': 0x08},
            'io'     : {'muxSel': 0x5, 'autoSel': 0x04},
            'unused6': {'muxSel': 0x6, 'autoSel': 0x02},
            'unused7': {'muxSel': 0x7, 'autoSel': 0x01}
        }
        self.driver = None
        self.logger.debug("ADS8638 has been instantiated")

    def initCfg(self, driver):
        self.driver = driver
        #Ads8638 ADC voltage measure
        self.sendBytes([0x01, 0x00]) #Reset disable
        self.sendBytes([0x06, 0x0C]) #AL_PD=1, IntVREF=1, TempSense=0
        self.sendBytes([0x0C, 0x00]) #Automode on Ch0 only
        self.sendBytes([0x10, 0x22]) #Range 010
        self.sendBytes([0x11, 0x22]) #Range 010
        self.sendBytes([0x12, 0x22]) #Range 010
        self.sendBytes([0x13, 0x22]) #Range 010
        
    def setMux(self, testType):
        muxSel = self.ins.get(testType).get('muxSel')
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
                (muxVal > 0x2 and muxVal < 0x5), #0x0 and 0x7 only
                muxVal > 0x7, #up to 8 AI selections in ADS8638
                ]
        if any(cond): 
            valid = False
            self.logger.error("Invalid condition({}) with ({}) ".format(cond.index(True), muxVal))
        return valid
        
    def readAdc(self, testType):
        #Set AIN
        self.setMux(testType)
        cmd = self.setupCommand('MANUAL',testType) 
        self.sendBytes(cmd)
        time.sleep(self.SAMPLE_DELAY)
        self.sendBytes() #16 SCKs for acquisition
        #Read DigitalOut
        digitalSamples = []
        for i in range(self.SAMPLE_SIZE):
        msb, lsb = self.getBytes()
        chByte = (0xF0 & msb) >> 4
        digitalOut = (0x0F & msb) << 8 | (lsb & 0xFF)
            digitalSamples.append(digitalOut)
        #self.logger.warning("Digital samples: {}".format(digitalSamples))
        finalDigitalOut = self.filterOutlier(digitalSamples)
        self.states['digOut'] = finalDigitalOut
        self.logger.debug("ADC digital out = {:#x} from port {:#x}".format(finalDigitalOut, chByte))
        #Calc Vmeas
        return (chByte, self.getVmeas())

    def setupCommand(self, mode='AUTO', testType=None):
        cmd = []
        if mode=='AUTO':
            self.sendBytes([0x0C, self.ins.get(testType).get('autoSel')]) #Automode channel
            lnib = (0x0F & (self.RESET_SEQ << 3))
            rnib = ((0x07 & self.RANGESEL) << 1) | (0x01 & self.TSENSESEL) 
            lsb = (lnib << 4) | rnib
            cmd = [self.AUTOMODE, lsb]
        elif mode=='MANUAL':
            #Set Manual Cfg
            lnib = (0x07 & self.states.get('muxSel'))
            rnib = ((0x07 & self.RANGESEL) << 1) | (0x01 & self.TSENSESEL) 
            lsb = (lnib << 4) | rnib
            cmd = [self.MANUALMODE, lsb]
        else:
            self.logger.error("Unsupported channel sequence mode: {}".format(mode))
        return cmd

    def sendBytes(self, dBytes=[0x00,0x00]):
        addr, data = dBytes 
        eff_addr = addr << 1
        self.driver.cfg_write(self.CHIPSEL, [eff_addr, data], self.FREQUENCY) 

    def getBytes(self, dBytes=[0x00,0x00]):
        time.sleep(self.SAMPLE_DELAY)
        addr, data = dBytes 
        eff_addr = addr << 1
        result = self.driver.cfg_read(self.CHIPSEL, [eff_addr, data], self.FREQUENCY) 
        return result
        
    def getVmeas(self):
        analogOut = self.states.get('digOut') * self.rangeResolution + self.rangeStart
        self.states['anaOut'] = analogOut
        self.logger.debug("Calculated Vmeas out {:.4f} for {:#x}".format(analogOut, self.states.get('digOut')))
        return self.states['anaOut']

    def filterOutlier(self, dataSamples=[]):
        #self.logger.warning("Median: {}".format(statistics.median(dataSamples)))
        return int(statistics.median(dataSamples))
