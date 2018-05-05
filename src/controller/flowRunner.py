'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from lxml import etree
from instrument.pmu import Pmu
from instrument.tests import Tests

class FlowRunner():
    '''
    classdocs
    '''


    def __init__(self, tp):
        '''
        Constructor
        '''
        self.tp = tp
        print('FlowRunner is initialized with Tp:', tp)
        print(etree.tostring(self.tp.programtree))
        self.tests = {}
        self.pingroups = {}
        self.extractTests()

        
    def executeAll(self):
        print('executeAll: ', etree.tostring(self.tp.programtree))
        print('tests: ', self.tests)
        print('pingroups: ', self.pingroups)
        for test in self.tests.keys():
            testResult = self.executeSingle(test)
            print(etree.tostring(testResult))
#                 etree.SubElement(element.getparent(), element.tag, testResult.getroot())
#         return self.tp
    
    def extractTests(self):
        print('executeAll: ', etree.tostring(self.tp.programtree))
        for element in self.tp.programtree.iter():
            print(element.tag, ' : ', element.get('name'))
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
        print(etree.tostring(params))
        pinref = params.get('pinref')
        print(pinref)
        pins = self.pingroups.get(pinref).get('pins')
        print(pins)
        pmu = Pmu(singleTest, pins)
        singleResult = etree.ElementTree(pmu.get())
#         print(etree.tostring(singleResult))
        return singleResult