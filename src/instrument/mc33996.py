'''
Created on Oct 16, 2018

@author: victord
'''
import os
import signal
from logger.sctLogger import SctLogger

class Mc33996(object):
    '''
    Models the Mc33996 port states in the SCT board
    '''
    logger = SctLogger(__name__).getLogger()
    validTypes = ['power']

    def __init__(self):
        '''
        Default settings
        '''        
        #Controls - 16 bits, independent, one-hot encoding, output only
        #VDD0: OUT0 <=> bit0
        #VDD1: OUT1 <=> bit1
        #VDD2: OUT2 <=> bit2
        #VDD3: OUT3 <=> bit3
        #VDD4: OUT4 <=> bit4
        #VDD5: OUT5 <=> bit5
        #VDD6: OUT6 <=> bit6
        #VDD7: OUT7 <=> bit7
        #VDD8: OUT8 <=> bit8
        #VDD9: OUT9 <=> bit9
        #VDD10: OUT10 <=> bit10
        #VDD11: OUT11 <=> bit11
        #VDD12: OUT12 <=> bit12
        #VDD13: OUT13 <=> bit13
        #VDD14: OUT14 <=> bit14
        #VDD15: OUT15 <=> bit15
        self.relay = 0b_0000_0000_0000_0000
        self.logger.debug("MC33996 has been instantiated")
        
    def selectPort(self, chType, portSel):
        if chType in self.validTypes: 
            if self.validateBits(portSel):
                self.relay = portSel & 0b_1111_1111_1111_1111 
                self.logger.debug("MC33996 settings updated relay={:#018b} or {:#06x} or bit #{:02d}".format(self.relay, self.relay, portSel))
                return True
            else:
                os.kill(os.getpid(), signal.SIGINT) 
                return False
        else:
            self.logger.debug("Type {} is not in {}, skipping...".format(chType, self.validTypes))
            return True
            
        
    def validateBits(self, portSel):
        valid = True
        if any([
                (portSel & (portSel - 1)) != 0, #more than 1 selected
                portSel > 0b_1000_0000_0000_0000, #only 16 selections
                ]): 
            valid = False
            self.logger.debug("Relay Select = {:#x}".format(portSel))
            self.logger.exception("Bit validation failed, shutting down...")
        return valid
        
        