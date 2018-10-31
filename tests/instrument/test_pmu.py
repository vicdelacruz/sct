'''
Created on Oct 24, 2018

@author: victord
'''
import unittest
from sct.instrument.pmu import Pmu

class TestPmu(unittest.TestCase):

    def setUp(self):
        self.pmu = Pmu()

    def tearDown(self):
        pass
    
    def test_setupGetMeas(self):
        #Mock Values
        testValues = {
            0x0: {'testType': 'io', 'chSel': 0b_001_00000_00000, 'param': -400e-6, 'digOut': 0x0, 'anaOut': -5.0 },
            0x1: {'testType': 'io', 'chSel': 0b_010_00000_00011, 'param': 400e-6, 'digOut': 0xFFF, 'anaOut': 5.0 - self.pmu.ads8638.rangeResolution }, #1 LSB off
            0x2: {'testType': 'io', 'chSel': 0b_100_11110_00111, 'param': 0.0, 'digOut': 0x800, 'anaOut': 0.0 }, #midpoint of the scale
            0x3: {'testType': 'io', 'chSel': 0b_100_11111_11111, 'param': -0.0, 'digOut': 0x7FF, 'anaOut': 0.0 - self.pmu.ads8638.rangeResolution },
            0x4: {'testType': 'power', 'chSel': 0b_0000_0000_0000_0001, 'param': -100e-3, 'digOut': 0x801, 'anaOut': 0.0 + self.pmu.ads8638.rangeResolution },
            0x5: {'testType': 'power', 'chSel': 0b_0000_0000_0100_0000, 'param': 100e-3, 'digOut': 0xFFF, 'anaOut': 5.0 - self.pmu.ads8638.rangeResolution }, #1 LSB off
            0x6: {'testType': 'power', 'chSel': 0b_0000_0000_1000_0000, 'param': 0.0, 'digOut': 0xFFE, 'anaOut': 5.0 - 2*self.pmu.ads8638.rangeResolution }, #1 LSB off
            0x7: {'testType': 'power', 'chSel': 0b_1000_0000_0000_0000, 'param': -0.0, 'digOut': 0x001, 'anaOut': -5.0 + self.pmu.ads8638.rangeResolution }
        } 
            
        for i in range(0, 8):
            testType = testValues.get(i).get('testType')
            chSel = testValues.get(i).get('chSel')
            param = testValues.get(i).get('param')
            self.pmu.setup(testType, chSel, param)
            self.assertTrue(self.pmu.states.get(testType).get('pinSelect') == chSel) #tests setup()
            self.pmu.ads8638.states['digOut'] = testValues.get(i).get('digOut') #mock ADC out
            self.assertTrue(self.pmu.getMeas() == testValues.get(i).get('anaOut')) #tests getMeas()
        with self.assertRaises(TypeError):
            self.pmu.setup('', 0x1, 0.0)
            self.pmu.setup('io', 0x1, 0.0)
            self.pmu.setup('power', 0x0, 0.0)
            self.pmu.setup('', 0x1)
            self.pmu.setup(0x1, 0.0)
                    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
