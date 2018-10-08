'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from lxml import etree
from instrument.pmu import Pmu
from spi.spiDriver import Driver
from logger.sctLogger import SctLogger

class FlowRunner():
    '''
    classdocs
    '''
    logger = SctLogger(__name__).getLogger()

    def __init__(self, tp):
        '''
        Constructor
        '''
        self.tp = tp
        self.logger.info('FlowRunner is initialized with Tp: %s', tp.programtree.getroot().get('name'))
        self.logger.info(etree.tostring(self.tp.programtree))
        self.tests = {}
        self.pingroups = {}
        self.extractTests()

        
    def executeAll(self):
        self.logger.info('executeAll: %s', etree.tostring(self.tp.programtree))
        self.logger.info('tests: %s', self.tests)
        self.logger.info('pingroups: %s', self.pingroups)
        testResults = {}
        for test in self.tests.keys():
            testResult = self.executeSingle(test)
            testResults[test] = etree.tostring(testResult)
#             self.logger.info(etree.tostring(testResult))
#                 etree.SubElement(element.getparent(), element.tag, testResult.getroot())
        self.testSpi()
        return testResults
    
    def extractTests(self):
        self.logger.info('executeAll: %s', etree.tostring(self.tp.programtree))
        for element in self.tp.programtree.iter():
            self.logger.info('%s : %s',element.tag, element.get('name'))
            if (element.tag == 'Test'):
#                 testResult = self.executeSingle(element)
#                 etree.SubElement(element.getparent(), element.tag, testResult.getroot())
                self.tests[element.get('name')] = {'params': element, 
                                                   'pinref': element.get('pinref')}
            elif (element.tag == 'PinGroup'):
                self.pingroups[element.get("name")] = {'pins': [] }
            elif (element.tag == 'Pin' and element.getparent().tag == 'PinGroup'):
                self.pingroups[element.getparent().get('name')].get('pins').append(element.get('name'))
        return self.tp
        
    def executeSingle(self, singleTest):
        params = self.tests.get(singleTest).get('params')
        self.logger.info(etree.tostring(params))
        pinref = params.get('pinref')
        self.logger.info(pinref)
        pins = self.pingroups.get(pinref).get('pins')
        self.logger.info(pins)
        pmu = Pmu(singleTest, pins)
        singleResult = etree.ElementTree(pmu.get())
#         self.logger.info(etree.tostring(singleResult))
        return singleResult

    def testSpi(self):
        driver = Driver()
        driver.xfer(0x0, 0b01011010)
        driver.xfer2(0x0, 0b11110000)
