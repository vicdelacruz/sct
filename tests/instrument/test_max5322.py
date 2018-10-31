'''
Created on Oct 24, 2018

@author: victord
'''
import unittest
from sct.instrument.max5322 import Max5322

class TestMax5322(unittest.TestCase):

    def setUp(self):
        self.max5322 = Max5322()

    def tearDown(self):
        pass
    
    def test_setIForceWithQuantize(self):
        self.max5322.setIForce('io', -400e-6)
        self.assertTrue(self.max5322.states.get('io').get('dac') == 0x000)
        self.assertTrue(round(self.max5322.states.get('io').get('force'), 4) == -400e-6)
        self.assertTrue(round(self.max5322.states.get('io').get('out'), 4) == -5.0)
        self.max5322.setIForce('io', 400e-6)
        self.assertTrue(self.max5322.states.get('io').get('dac') == 0xfff)
        self.assertTrue(round(self.max5322.states.get('io').get('force'), 4) ==
            round(self.max5322.pmuTypes.get('io').get('stop') - self.max5322.pmuTypes.get('io').get('res'), 4)) #one step less
        self.assertTrue(round(self.max5322.states.get('io').get('out'), 4) == 4.9976) #one step less
        self.max5322.setIForce('power', -100e-3)
        self.assertTrue(self.max5322.states.get('power').get('dac') == 0x000)
        self.assertTrue(round(self.max5322.states.get('power').get('force'), 4) == -100e-3)
        self.assertTrue(round(self.max5322.states.get('power').get('out'), 4) == -5.0)
        self.max5322.setIForce('power', 100e-3)
        self.assertTrue(self.max5322.states.get('power').get('dac') == 0xfff)
        self.assertTrue(round(self.max5322.states.get('power').get('force'), 4) ==
            round(self.max5322.pmuTypes.get('power').get('stop') - self.max5322.pmuTypes.get('power').get('res'), 4)) #one step less
        self.assertTrue(round(self.max5322.states.get('power').get('out'), 4) == 4.9976) #one step less
        with self.assertRaises(AttributeError):
            self.max5322.setIForce('', 0)
            self.max5322.setIForce('')
            self.max5322.setIForce(0, 'invalid')
            
    def test_validateRange(self):
        self.assertTrue(self.max5322.validateRange('io', 0))
        self.assertTrue(self.max5322.validateRange('io', -400e-6))
        self.assertTrue(self.max5322.validateRange('io', 400e-6))
        self.assertFalse(self.max5322.validateRange('io', -400.1e-6))
        self.assertFalse(self.max5322.validateRange('io', 400.1e-6))
        self.assertTrue(self.max5322.validateRange('power', 0))
        self.assertTrue(self.max5322.validateRange('power', -100e-3))
        self.assertTrue(self.max5322.validateRange('power', 100e-3))
        self.assertFalse(self.max5322.validateRange('power', -101e-3))
        self.assertFalse(self.max5322.validateRange('power', 101e-3))
        with self.assertRaises(AttributeError):
            self.max5322.validateRange('', 0)
            self.max5322.validateRange('')
            self.max5322.validateRange('invalid', 0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
