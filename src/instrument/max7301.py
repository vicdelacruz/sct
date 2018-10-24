'''
Created on Oct 16, 2018

@author: victord
'''
import os
import signal
from logger.sctLogger import SctLogger

class Max7301(object):
    '''
    Models the Max7301 port states in the SCT board
    '''
    logger = SctLogger(__name__).getLogger()
    validTypes = ['IO']


    def __init__(self):
        '''
        Default settings
        '''
        #Line Select - 5 bits, binary encoded, output only
        #P04 <=> bit0 
        #P05 <=> bit1 
        #P06 <=> bit2 
        #P07 <=> bit3 
        #P08 <=> bit4 
        self.ls = 0b_0_0000
        
        #Column Select - 5 bits, binary encoded, output only
        #P09 <=> bit0 
        #P10 <=> bit1 
        #P11 <=> bit2 
        #P12 <=> bit3 
        #P13 <=> bit4 
        self.cs = 0b_0_0000
        
        #Row Enable - 3 bits, 1-hot encoded, output only
        #P14 <=> bit0 
        #P15 <=> bit1 
        #P16 <=> bit2 
        self.re = 0b_000
        
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
        self.ctrl = 0b_000_0000_0000_0000
        self.logger.debug("MAX7301 has been instantiated")
        
    def setPorts(self, chType, channelMap, controls):
        ctrl =  controls & 0b_111_1111_1111_1111
        if chType in self.validTypes:
            channel = int(channelMap)
            ls =    channel & 0b_1_1111
            cs =    channel>>5 & 0b_1_1111
            re =    channel>>10 & 0b111
            if self.validateBits(ls, cs, re, ctrl):
                self.ls = ls
                self.cs = cs
                self.re = re
                self.ctrl = ctrl
                self.logger.debug("MAX7301 settings updated ls={:02d}, cs={:02d}, re={:#05b}, ctrl={:#06x}".format(ls, cs, re, ctrl))
                return True
            else:
                os.kill(os.getpid(), signal.SIGINT) 
                return False
        else:
            self.logger.debug("Type {} is not in {}, skipping...".format(chType, self.validTypes))
            return True
                    
    def validateBits(self, ls, cs, re, ctrl):
        valid = True
        if any([
                ls > 0x1F, #only 5 bits
                cs > 0x1F, #only 5 bits
                re not in [0b_000, 0b_001, 0b_010, 0b_100], #only 1 or 0 enabled 
                ctrl > 0x7FFF, #only 15 bits
                ]): 
            valid = False
            self.logger.debug("Line Select = {:#b} {}".format(ls, str(ls > 0x1F)))
            self.logger.debug("Column Select = {:#b} {}".format(cs, str(cs > 0x1F)))
            self.logger.debug("Row Enable = {:#b} {}".format(re, str(re not in [0b_000, 0b_001, 0b_010, 0b_100])))
            self.logger.debug("Controls = {:#b} {}".format(ctrl, str(ctrl > 0x7FFF)))
            self.logger.exception("Bit validation failed, shutting down...")
        return valid
        
        