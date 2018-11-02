'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from lxml import etree
from sct.controller.tests import Tests
from sct.logger.sctLogger import SctLogger

class FlowRunner():
    '''
    classdocs
    '''
    logger = SctLogger().getLogger(__name__)

    def __init__(self, tp):
        '''
        Constructor
        '''
        self.testController = Tests()
        self.tp = tp
        self.logger.info('FlowRunner is initialized with Tp: {}'.format(tp.programtree.getroot().get('name')))
        self.logger.debug(etree.tostring(self.tp.programtree))
        self.tests = {}
        self.pingroups = {'io': {}, 'power': {}}
        self.extractTests()
    
    def extractTests(self):
        self.logger.info('Extacting tests...')
        for element in self.tp.programtree.iter():
            self.logger.debug('{} : {}'.format(element.tag, element.attrib))
            if (element.tag == 'DataPoints'):
                self.tests[element.get('pingroup')] = []
            elif (element.tag == 'ForcedValue'):
                self.tests[element.getparent().get('pingroup')].append(element.get('set'))
            elif (element.tag == 'PinGroup'):
                self.pingroups[element.get("pintype")].update({element.get("name"): {} })
            elif (element.tag == 'Pin' and element.getparent().tag == 'PinGroup'):
                self.pingroups[element.getparent().get('pintype')].get(element.getparent().get('name')).update({element.get('channel'): element.get('name')})
        self.logger.debug('Parsed tests: {}'.format(self.tests))
        self.logger.debug('Parsed pingroups: {}'.format(self.pingroups))
        self.testController.pinMap = self.pingroups
        return self.tp
        
    def executeAll(self):
        self.logger.info('Executing all tests...')
        self.logger.debug('Execute tests: %s', self.tests)
        self.logger.debug('Execute pingroups: %s', self.pingroups)
        testResults = etree.Element('TestResults', name=self.tp.programtree.getroot().get('name'),
            pkg=self.tp.programtree.getroot().get('pkg'), opn=self.tp.programtree.getroot().get('opn'),
            ver=self.tp.programtree.getroot().get('ver'))
        for testType in self.pingroups:
            self.logger.debug('Test type: %s', testType)
            for testGroup in self.pingroups.get(testType):
                if testGroup not in self.tests.keys():
                    self.logger.error('Test: %s does not have setpoint(s)', testGroup)
                else:
                    self.logger.info('Running pin group: %s', testGroup)
                    pinGroup = self.pingroups.get(testType).get(testGroup)
                    testResult = self.executeGroup(testType, self.tests.get(testGroup), testGroup, pinGroup)
                    testResults.append(testResult)
            self.logger.debug('Test results: %s', etree.tostring(testResults))
        self.testSpi()
		return testResults
    
    def executeGroup(self, testType, testPoints, testGroup, pinGroup):
        testResults = etree.Element('Results', name=testGroup, pintype=testType)
        forcedValue = etree.SubElement(testResults, 'ForcedValue')
        forcedValue.text = '|'.join(testPoints)   
        pinResults = self.testController.getGroupResults(testType, 
            testPoints, testGroup, pinGroup)
        for pinResult in pinResults.getchildren():
            testResults.append(pinResult)
        self.logger.debug('Test groups result: %s', etree.tostring(testResults))
        return testResults
    
    def executeSingle(self, testType, singleTest):
        singleResult = etree.Element('Results', name=singleTest, pintype=testType)
        forcedValue = etree.SubElement(singleResult, 'ForcedValue')
        forcedValue.text = '|'.join(self.tests.get(singleTest))         
        for pin in self.pingroups.get(testType).get(singleTest):
            params = self.tests.get(singleTest)
            self.logger.debug('Testing pin %s for %s', pin, params)
            singleResult.append(self.testController.getPinResults(params, pin))
            self.logger.debug('Single result: %s', etree.tostring(singleResult))
        return singleResult

    def testSpi(self):
        driver = Driver()
        driver.xfer(0x0, 0b01011010)
        driver.xfer2(0x0, 0b11110000) 
