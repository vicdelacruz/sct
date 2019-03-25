'''
Created on Oct 16, 2018

@author: victord
'''
import os
import signal
from sct.logger.sctLogger import SctLogger
from sct.spi.spiDriver import Driver

class Mc33996(object):
    '''
    Models the Mc33996 port states in the SCT board
    '''
    logger = SctLogger().getLogger(__name__)
    validTypes = ['power']

    CHIPSEL = 0x3 #Device #3
    FREQUENCY = 1000000 # 1MHz baud rate 
    MODE = 0b01 #CPOL=0 (PositiveEdge Clk)
                #CPHA=1 (DataLatch on ClkFall)

    def __init__(self):
        '''
        Default settings
        '''
        self.states = {
            #Controls - 16 bits, independent, one-hot encoding, output only
            'relay': 0b_0000_0000_0000_0000
        }
        self.ins = {
            0x0: 'OUT1',  #VDD1
            0x1: 'OUT2',  #VDD2
            0x2: 'OUT3',  #VDD3
            0x3: 'OUT4',  #VDD4
            0x4: 'OUT5',  #VDD5
            0x5: 'OUT6',  #VDD6
            0x6: 'OUT7',  #VDD7
            0x7: 'OUT8',  #VDD8
            0x8: 'OUT9',  #VDD9
            0x9: 'OUT10', #VDD10
            0xA: 'OUT11', #VDD11
            0xB: 'OUT12', #VDD12
            0xC: 'OUT13', #VDD13
            0xD: 'OUT14', #VDD14
            0xE: 'OUT15', #VDD15
            0xF: 'OUT16', #VDD16
        }
        self.driver = None
        self.logger.debug("MC33996 has been instantiated")

    def initCfg(self, driver):
        self.driver = driver
        #MC33996 power relay mux
        self.sendBytes([0x00, 0x00, 0x00]) #All out OFF

    def selectPort(self, chType, portSel):
        if chType in self.validTypes: 
            if self.validateBits(portSel):
                relaySel = portSel & 0b_1111_1111_1111_1111
                self.states['relay'] = relaySel
                i = "{:016b}".format(relaySel)[::-1].index('1')
                self.logger.debug("MC33996 settings updated relay={:#x} or {}".format(
                    relaySel, self.ins.get(i)))
                msb = (relaySel & 0xFF00) >> 8
                lsb = relaySel & 0xFF
                self.sendBytes([0x00, msb, lsb])
                return True
            else:
                self.logger.exception("Bit validation failed, shutting down...")
                os.kill(os.getpid(), signal.SIGINT) 
                return False
        else:
            self.logger.debug("Type {} is not in {}, skipping...".format(chType, self.validTypes))
            return True

    def sendBytes(self, data):
        self.driver.cfg_write(self.CHIPSEL, data, self.FREQUENCY, self.MODE) 

    def validateBits(self, portSel):
        valid = True
        cond = [
                portSel < 0b_0000_0000_0000_0001, #None selected
                (portSel & (portSel - 1)) != 0, #more than 1 selected
                portSel > 0b_1000_0000_0000_0000, #only 16 selections
                ]
        if any(cond): 
            valid = False
            self.logger.error("Invalid condition({}) with ({:#x}) ".format(cond.index(True), portSel))
        return valid
