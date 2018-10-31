'''
Created on Oct 24, 2018

@author: victord
'''
import unittest
from sct.instrument.ads8638 import Ads8638

class TestAds8638(unittest.TestCase):

    def setUp(self):
        self.ads8638 = Ads8638()

    def tearDown(self):
        pass
    
    def test_setMuxReadAdcGetVmeas(self):
        #Mock Values
        testValues = {
            0x0: {'analog': -5.0, 'digOut': 0x0, 'anaOut': -5.0 },
            0x1: {'analog': 5.0, 'digOut': 0xFFF, 'anaOut': 5.0 - self.ads8638.rangeResolution }, #1 LSB off
            0x2: {'analog': 0.0, 'digOut': 0x800, 'anaOut': 0.0 }, #midpoint of the scale
            0x3: {'analog': 0.0 - self.ads8638.rangeResolution, 'digOut': 0x7FF, 'anaOut': 0.0 - self.ads8638.rangeResolution },
            0x4: {'analog': 0.0 + self.ads8638.rangeResolution, 'digOut': 0x801, 'anaOut': 0.0 + self.ads8638.rangeResolution },
            0x5: {'analog': 5.0 - self.ads8638.rangeResolution, 'digOut': 0xFFF, 'anaOut': 5.0 - self.ads8638.rangeResolution }, #1 LSB off
            0x6: {'analog': 5.0 - 2*self.ads8638.rangeResolution, 'digOut': 0xFFE, 'anaOut': 5.0 - 2*self.ads8638.rangeResolution }, #1 LSB off
            0x7: {'analog': -5.0 + self.ads8638.rangeResolution, 'digOut': 0x001, 'anaOut': -5.0 + self.ads8638.rangeResolution }
        } 
        for i in range(0, 8):
            self.ads8638.setMux(i)
            self.ads8638.states.get('ins').get(i)['analog'] = testValues.get(i).get('analog')
            self.assertTrue(self.ads8638.states.get('ins').get(i).get('analog') == testValues.get(i).get('analog'))
            self.assertTrue(self.ads8638.readAdc() == testValues.get(i).get('digOut'))
            self.assertTrue(self.ads8638.getVmeas() == testValues.get(i).get('anaOut'))
            
    def test_validateMux(self):
        self.assertTrue(self.ads8638.validateMux(0x0))
        self.assertTrue(self.ads8638.validateMux(0x7))
        self.assertFalse(self.ads8638.validateMux(0x8))
        with self.assertRaises(TypeError):
            self.ads8638.validateMux('invalid')

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()