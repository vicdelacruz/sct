'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from util.fileHandler import FileHandler
from model.tp import Tp
from resources import props
from controller.flowRunner import FlowRunner
from lxml import etree

class FrontController(object):
    '''
    classdocs
    '''
    

    def __init__(self, mainView = None):
        '''
        Constructor
        '''
        self.tp = Tp()
        self.mainView = mainView
        self.result = None
        print('Front is initialized...')
        
    def load(self, tpPath=None):
        print('Front is loading...')
        fh = FileHandler(props.tpPath)
        self.tp = fh.load()
        print(etree.tostring(self.tp.programtree))
        
    def executeAll(self):
        flowrunner = FlowRunner(self.tp)
        raw = flowrunner.executeAll()
#         print(etree.tostring(raw))
        