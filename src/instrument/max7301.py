'''
Created on Oct 16, 2018

@author: victord
'''

from logger.sctLogger import SctLogger

class Max7301(object):
    '''
    Models the Max7301 port states in the SCT board
    '''
    logger = SctLogger(__name__).getLogger()

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
        
    def setPorts(self, portVals):
        ls =    portVals & 0b_1_1111
        cs =    (portVals >> 5) & 0b_1_1111
        re =    (portVals >> 10) & 0b111
        ctrl =  (portVals >> 13) & 0b_111_1111_1111_1111
        if self.validateBits(ls, cs, re, ctrl):
            self.ls = ls
            self.cs = cs
            self.re = re
            self.ctrl = ctrl
            self.logger.debug("Settings updated ls={:05b}, cs={:05b}, re={:03b}, ctrl={:015b}".format(ls, cs, re, ctrl))
            return True
        else:
            return False
        
    def validateBits(self, ls, cs, re, ctrl):
        valid = True
        if any([
                ls > 0x1F, #only 5 bits
                cs > 0x1F, #only 5 bits
                re not in [0b_000, 0b_001, 0b_010, 0b_100], #only 1 or 0 enabled 
                ctrl > 0x7FFF, #only 15 bits
                ]): 
            valid = False
            self.logger.exception("Bit validation failed!!!")
            self.logger.debug("Line Select = {0:b} {1}".format(ls, str(ls > 0x1F)))
            self.logger.debug("Column Select = {0:b} {1}".format(cs, str(cs > 0x1F)))
            self.logger.debug("Row Enable = {0:b} {1}".format(re, str(re not in [0b_000, 0b_001, 0b_010, 0b_100])))
            self.logger.debug("Controls = {0:b} {1}".format(ctrl, str(ctrl > 0x7FFF)))
        return valid
        
        