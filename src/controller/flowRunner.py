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
        self.logger.debug(etree.tostring(self.tp.programtree))
        self.tests = {}
        self.pingroups = {}
        self.extractTests()

        
    def executeAll(self):
        self.logger.info('executeAll: %s', etree.tostring(self.tp.programtree))
        self.logger.info('tests: %s', self.tests)
        self.logger.info('pingroups: %s', self.pingroups)
        testResults = etree.Element('TestResults', name=self.tp.programtree.getroot().get('name'),
            pkg=self.tp.programtree.getroot().get('pkg'), opn=self.tp.programtree.getroot().get('opn'))
        for testType in self.pingroups:
            self.logger.debug('Test type: %s', testType)
            for test in self.pingroups.get(testType):
                if test not in self.tests.keys():
                    self.logger.error('Test: %s does not have setpoint(s)', test)
                else:
                    self.logger.debug('Running test: %s with setpoints %s', test, self.tests.get(test))
                    testResult = self.executeSingle(testType, test)
                    testResults.append(testResult)
            self.logger.debug('Test results: %s', etree.tostring(testResults))
        self.testSpi()
        return testResults
    
    def extractTests(self):
        self.logger.info('executeAll: %s', etree.tostring(self.tp.programtree))
        for element in self.tp.programtree.iter():
            self.logger.debug('%s : %s',element.tag, element.attrib )
            if (element.tag == 'DataPoints'):
                self.tests[element.get("pingroup")] = []
                self.logger.debug(self.tests)
            elif (element.tag == 'ForcedValue'):
                self.tests[element.getparent().get('pingroup')].append(element.get('set'))
            elif (element.tag == 'PinGroup'):
                self.pingroups[element.get("pintype")] = {element.get("name"): [] }
                self.logger.debug(self.pingroups)
            elif (element.tag == 'Pin' and element.getparent().tag == 'PinGroup'):
                self.pingroups[element.getparent().get('pintype')].get(element.getparent().get('name')).append(element.get('name'))
        self.logger.debug(self.tp)
        return self.tp
        
    def executeSingle(self, testType, singleTest):
        singleResult = etree.Element('Results', name=singleTest, pintype=testType)
        forcedValue = etree.SubElement(singleResult, 'ForcedValue')
        forcedValue.text = '|'.join(self.tests.get(singleTest))         
        for pin in self.pingroups.get(testType).get(singleTest):
            params = self.tests.get(singleTest)
            self.logger.debug('Testing pin %s for %s', pin, params)
            pmu = Pmu(params, pin)
            singleResult.append(pmu.get())
            self.logger.debug('Single result: %s', etree.tostring(singleResult))
        return singleResult

    def testSpi(self):
        driver = Driver()
        driver.xfer(0x0, 0b01011010)
        driver.xfer2(0x0, 0b11110000)