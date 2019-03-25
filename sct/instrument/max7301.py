'''
Created on Oct 16, 2018

@author: victord
'''
import os
import signal
from sct.logger.sctLogger import SctLogger
from sct.spi.spiDriver import Driver

class Max7301:
    '''
    Models the Max7301 port states in the SCT board
    '''
    logger = SctLogger().getLogger(__name__)
    validTypes = ['io']

    CHIPSEL = 0x0 #Device #0
    FREQUENCY = 1000000 # 1MHz baud rate 

    def __init__(self):
        '''
        Default settings
        '''
        self.states = {
            #Line Select - 5 bits, binary encoded, output only
            #P04 <=> bit0 
            #P05 <=> bit1 
            #P06 <=> bit2 
            #P07 <=> bit3 
            #P08 <=> bit4 
            'ls': 0b_0_0000,
            
            #Column Select - 5 bits, binary encoded, output only
            #P09 <=> bit0 
            #P10 <=> bit1 
            #P11 <=> bit2 
            #P12 <=> bit3 
            #P13 <=> bit4 
            'cs': 0b_0_0000,
            
            #Row Enable - 3 bits, 1-hot encoded, output only
            #P14 <=> bit0 
            #P15 <=> bit1 
            #P16 <=> bit2 
            're': 0b_000,
            
            #Controls - 15 bits, independent, output only
            #P17 <=> ctrl_0 
            #P18 <=> ctrl_1 
            #P19 <=> ctrl_2 
            #P20 <=> ctrl_3 
            #P21 <=> ctrl_4 
            #P22 <=> ctrl_5 
            #P23 <=> ctrl_6 
            #P24 <=> ctrl_7 
            #P25 <=> ctrl_8 
            #P26 <=> ctrl_9 
            #P27 <=> ctrl_10 
            #P28 <=> ctrl_11 
            #P29 <=> ctrl_12 
            #P30 <=> ctrl_13 
            #P31 <=> ctrl_14 
            'ctrl': 0b_000_0000_0000_0000
        }
        self.regs = {
            'ls': [0x24, 0x25, 0x26, 0x27, 0x28],
            'cs': [0x29, 0x2A, 0x2B, 0x2C, 0x2D],
            're': [0x2E, 0x2F, 0x30]
        }
        self.driver = None
        self.logger.debug("MAX7301 has been instantiated")

    def setCfg(self, driver, data=[]):
        self.driver = driver
        self.sendBytes(data) 

    def setPorts(self, chType, channelMap, controls):
        ctrl =  controls & 0b111111111111111
        if chType in self.validTypes:
            channel = int(channelMap)
            ls =    channel & 0b11111
            cs =    channel>>5 & 0b11111
            re =    channel>>10 & 0b111
            if self.validateBits(ls, cs, re, ctrl):
                self.states['ls'] = ls
                self.setMux('ls', ls)
                self.states['cs'] = cs
                self.setMux('cs', cs)
                self.states['re'] = re
                self.setMux('re', re, False)
                self.states['ctrl'] = ctrl
                self.logger.debug("MAX7301 settings updated ls={:#02x}, cs={:#02x}, re={:#01x}, ctrl={:#06x}".format(ls, cs, re, ctrl))
                return True
            else:
                self.logger.exception("Bit validation failed, SCT is shutting down...")
                os.kill(os.getpid(), signal.SIGINT) 
                return False
        else:
            self.logger.debug("Type {} is not in {}, skipping channel selection...".format(chType, self.validTypes))
            return True

    def setMux(self, muxGroup, data, act_high=True):
        self.logger.debug("MuxGroup: [{}], data {:X}".format(muxGroup, data))
        for i in range(len(self.regs.get(muxGroup))):
            tmp = data
            if act_high:
                lsb = (tmp >> i) & 0b1
            else:
                lsb = ((tmp >> i) ^ 0b1) & 0b1
            self.sendBytes([self.regs.get(muxGroup)[i], lsb])

    def sendBytes(self, data):
        self.driver.cfg_write(self.CHIPSEL, data, self.FREQUENCY) 
                    
    def validateBits(self, ls, cs, re, ctrl):
        valid = True
        cond = [
                ls > 0x1F, #only 5 bits
                cs > 0x1F, #only 5 bits
                (re & (re - 1)) != 0, #only 1 enabled 
                re == 0, #RE must be initialized 
                ctrl > 0x7FFF, #only 15 bits
                ]
        if any(cond): 
            valid = False
            self.logger.error("Invalid condition({}) with ({:#x}, {:#x}, {:#x}, {:#x}) ".format(cond.index(True), ls, cs, re, ctrl))
        return valid
        
        
