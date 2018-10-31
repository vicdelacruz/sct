'''
Created on Oct 16, 2018

@author: victord
'''
from sct.logger.sctLogger import SctLogger

class Max5322(object):
    '''
    Models the Max5322 voltage DAC in the SCT board
    '''
    logger = SctLogger().getLogger(__name__)
    
    voutStart = -5.0
    voutStop = 5.0
    dacSteps = 2**12
    dacRes = (voutStop - voutStart) / dacSteps
    pmuTypes = {
        #IO constants        
        'io': { 'start': -400e-6, 'stop': 400e-6, 'res': (400e-6 - -400e-6)/(dacSteps) },
        #power constants
        'power': { 'start': -100e-3, 'stop': 100e-3, 'res': (100e-3 - -100e-3)/(dacSteps) }
    }

    def __init__(self):
        '''
        Default settings
        '''
        #force -IFVM force currents
        #dac - Holds the intermediate, 12-bit binary input to DAC         
        #IO['out'] - OUTA <=> Channel A, IO chType, voltage analog out +/-5V bipolar
        #power['out'] - OUTB <=> Channel B, power chType, voltage analog out +/-5V bipolar
        self.states = {       
            'io': { 'dac': 0x0, 'force': 0.0, 'out': 0.0 },
            'power': { 'dac': 0x0, 'force': 0.0, 'out': 0.0 }
        }
        
        self.logger.debug("MAX5322 has been instantiated")
        
    def setIForce(self, chType, current):
        current = float(current)
        if self.validateRange(chType, current):
            (dac, force) = self.quantizeI(chType, current)
            out = self.voutStart + dac*self.dacRes
            self.states.get(chType)['dac'] = dac
            self.states.get(chType)['force'] = force
            self.states.get(chType)['out'] =  out
            self.logger.debug("MAX5322 settings updated force={:.4E}A, dac={:#05x}, out={:.4f}V".format(force, dac, out))
            return True
        else: 
            return False
        
    def validateRange(self, chType, current):
        valid = True
        cond = [
                current > self.pmuTypes.get(chType).get('stop'), #must not be greater than
                current < self.pmuTypes.get(chType).get('start'), #must not be less than
                chType not in self.pmuTypes.keys(), #invalid chType
                ]
        if any(cond): 
            self.logger.error("Invalid condition({}) with (\'{}\', {}) ".format(cond.index(True), chType, current))
            valid = False
        return valid
    
    def quantizeI(self, chType, current):
        qDac = int( (current - self.pmuTypes.get(chType).get('start'))/ self.pmuTypes.get(chType).get('res') )
        #Not a bug but per datasheet, max qout is self.dacSteps-1*dacRes
        if (qDac==self.dacSteps):
            self.logger.warning("Max count reached, scaling back by 0x1...")
            qDac = self.dacSteps -1
        qOut = qDac * self.pmuTypes.get(chType).get('res') + self.pmuTypes.get(chType).get('start')
        self.logger.debug("Quantized dac value = {:#05x}".format(qDac))
        self.logger.debug("Valid current = {:.4E} with {:.2E} resolution".format(qOut, self.pmuTypes.get(chType).get('res')))
        return (qDac, qOut)
        
        
