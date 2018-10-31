'''
Created on Oct 24, 2018

@author: victord
'''
import unittest
from sct.instrument.mc33996 import Mc33996

class TestAds8638(unittest.TestCase):

    def setUp(self):
        self.mc33996 = Mc33996()

    def tearDown(self):
        pass
    
    def test_selectPort(self):
        for i in range(0, 16):
            relaySelect = 2**i
            self.mc33996.selectPort('power', relaySelect)
            self.assertTrue(self.mc33996.states.get('relay') == relaySelect)
            self.assertTrue(self.mc33996.states.get('ins').get(i).get('name') == 'OUT{}'.format(i))
        with self.assertRaises(TypeError):
            self.mc33996.selectPort('io', 0x1)
            self.mc33996.selectPort(0x1, '')
            self.mc33996.selectPort()
                        
    def test_validateBits(self):
        self.assertTrue(self.mc33996.validateBits(0x1))
        self.assertTrue(self.mc33996.validateBits(0x8000))
        self.assertFalse(self.mc33996.validateBits(0x0))
        self.assertFalse(self.mc33996.validateBits(0x7))
        self.assertFalse(self.mc33996.validateBits(0x10000))
        with self.assertRaises(TypeError):
            self.mc33996.validateBits('invalid')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
