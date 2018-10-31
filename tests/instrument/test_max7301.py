'''
Created on Oct 24, 2018

@author: victord
'''
import unittest
from sct.instrument.max7301 import Max7301

class TestMax7301(unittest.TestCase):

    def setUp(self):
        self.max7301 = Max7301()

    def tearDown(self):
        pass
    
    def test_setPorts(self):
        self.max7301.setPorts('io', 0b_100_11111_11111, 0b_111_1111_1111_1111)
        self.assertTrue(self.max7301.states.get('ls') == 0x1F)
        self.assertTrue(self.max7301.states.get('cs') == 0x1F)
        self.assertTrue(self.max7301.states.get('re') == 0b100)
        self.assertTrue(self.max7301.states.get('ctrl') == 0x7FFF)
        self.max7301.setPorts('io', 0b_001_00000_00000, 0b_000_0000_0000_0000)
        self.assertTrue(self.max7301.states.get('ls') == 0x0)
        self.assertTrue(self.max7301.states.get('cs') == 0x0)
        self.assertTrue(self.max7301.states.get('re') == 0b001)
        self.assertTrue(self.max7301.states.get('ctrl') == 0x0)
        with self.assertRaises(TypeError):
            self.max7301.validateBits('power', 0x0, 0b001, 0x0)
            self.max7301.validateBits(0x0, '', 0b001, 0x0)
            self.max7301.validateBits(0x0, 0x0, '', 0x0)
            self.max7301.validateBits(0x0, 0x0, 0b001, '')
            self.max7301.validateBits(0x0, 0x0, 0b001)
            self.max7301.validateBits(0x0, 0x0, 0b001, 0x0, 0x0)
            
    def test_validateBits(self):
        self.assertTrue(self.max7301.validateBits(0x0, 0x0, 0b001, 0x0))
        self.assertFalse(self.max7301.validateBits(0x0, 0x0, 0x0, 0x0)) #Uninitialized RE?
        self.assertTrue(self.max7301.validateBits(0x1F, 0x1F, 0b100, 0x7FFF))
        self.assertFalse(self.max7301.validateBits(0x20, 0x1F, 0b100, 0x7FFF))
        self.assertFalse(self.max7301.validateBits(0x1F, 0x20, 0b100, 0x7FFF))
        self.assertFalse(self.max7301.validateBits(0x1F, 0x1F, 0b101, 0x7FFF))
        self.assertFalse(self.max7301.validateBits(0x1F, 0x1F, 0b100, 0x8000))
        with self.assertRaises(TypeError):
            self.max7301.validateBits('', 0x0, 0b001, 0x0)
            self.max7301.validateBits(0x0, '', 0b001, 0x0)
            self.max7301.validateBits(0x0, 0x0, '', 0x0)
            self.max7301.validateBits(0x0, 0x0, 0b001, '')
            self.max7301.validateBits(0x0, 0x0, 0b001)
            self.max7301.validateBits(0x0, 0x0, 0b001, 0x0, 0x0)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
