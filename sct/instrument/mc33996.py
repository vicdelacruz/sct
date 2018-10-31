'''
Created on Oct 16, 2018

@author: victord
'''
import os
import signal
from sct.logger.sctLogger import SctLogger

class Mc33996(object):
    '''
    Models the Mc33996 port states in the SCT board
    '''
    logger = SctLogger().getLogger(__name__)
    validTypes = ['power']

    def __init__(self):
        '''
        Default settings
        '''
        self.states = {
            'ins': {
                0x0: {'name': 'OUT0' },  #VDD0
                0x1: {'name': 'OUT1' },  #VDD1
                0x2: {'name': 'OUT2' },  #VDD2
                0x3: {'name': 'OUT3' },  #VDD3
                0x4: {'name': 'OUT4' },  #VDD4
                0x5: {'name': 'OUT5' },  #VDD5
                0x6: {'name': 'OUT6' },  #VDD6
                0x7: {'name': 'OUT7' },  #VDD7
                0x8: {'name': 'OUT8' },  #VDD8
                0x9: {'name': 'OUT9' },  #VDD9
                0xA: {'name': 'OUT10' }, #VDD10
                0xB: {'name': 'OUT11' }, #VDD11
                0xC: {'name': 'OUT12' }, #VDD12
                0xD: {'name': 'OUT13' }, #VDD13
                0xE: {'name': 'OUT14' }, #VDD14
                0xF: {'name': 'OUT15' }, #VDD15
            },
            #Controls - 16 bits, independent, one-hot encoding, output only
            'relay': 0b_0000_0000_0000_0000
        }
        self.logger.debug("MC33996 has been instantiated")
        
    def selectPort(self, chType, portSel):
        if chType in self.validTypes: 
            if self.validateBits(portSel):
                relaySel = portSel & 0b_1111_1111_1111_1111
                self.states['relay'] = relaySel
                i = '{:016b}'.format(relaySel)[::-1].index('1')
                self.logger.debug("MC33996 settings updated relay={:#x} or {}".format(
                    relaySel, self.states.get('ins').get(i).get('name')))
                return True
            else:
                self.logger.exception("Bit validation failed, shutting down...")
                os.kill(os.getpid(), signal.SIGINT) 
                return False
        else:
            self.logger.debug("Type {} is not in {}, skipping...".format(chType, self.validTypes))
            return True
            
        
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
        
        