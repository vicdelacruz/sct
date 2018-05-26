'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
from util.fileHandler import FileHandler
from model.tp import Tp
from controller.flowRunner import FlowRunner
from lxml import etree
import os
import time

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
        
    def monitor(self, cmdPath=None):
        while True:
            if os.path.exists(cmdPath):
                print('Front is loading CMD file...')
                fh = FileHandler()
                self.processCmds(fh.loadCmd(cmdPath))
            time.sleep(10)
        
    def processCmds(self, cmds):
        for cmd in cmds:
            op = cmd.split()
            if op[0] == 'LOAD':
                self.load(op[1])
            elif op[0] == 'EXECUTE_ALL':
                self.executeAll()
            else:
                pass
        
    def load(self, tpPath=None):
        print('Front is loading TP...')
        fh = FileHandler()
        self.tp = fh.loadTp(tpPath)
        print(etree.tostring(self.tp.programtree))
        
    def executeAll(self):
        flowrunner = FlowRunner(self.tp)
        flowrunner.executeAll()
#         raw = flowrunner.executeAll()
#         print(etree.tostring(raw))
        