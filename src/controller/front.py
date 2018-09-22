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
        self.results = None
        print('Front is initialized...')
        
    def monitor(self, cmdPath=None, logDir = None):
        while True:
            print("Polling for CMD file in %s%s%s" % (os.getcwd(), os.path.sep, cmdPath))
            if os.path.exists(cmdPath):
                print('Front is loading CMD file...')
                fh = FileHandler()
                self.processCmds(fh.loadCmd(cmdPath), logDir)
            time.sleep(10)
        
    def processCmds(self, cmds, logDir):
        for cmd in cmds:
            op = cmd.split()
            if op[0] == 'LOAD':
                self.load(op[1])
            elif op[0] == 'EXECUTE_ALL':
                self.executeAll()
            elif op[0] == 'LOG_ALL':
                self.logAll(logDir, op[1])
            else:
                pass
        
    def load(self, tpPath=None):
        print('Front is loading TP...')
        fh = FileHandler()
        self.tp = fh.loadTp(tpPath)
        print(etree.tostring(self.tp.programtree))
        
    def executeAll(self):
        flowrunner = FlowRunner(self.tp)
        self.results = flowrunner.executeAll()
#         print('All results...')
#         print(self.results)
        
    def logAll(self, logDir=None, logFile=None):
#         print('Logging all...')
#         print(self.results)
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        fh = FileHandler()
        fh.logResults(os.path.join(logDir,logFile), self.results)
        print('Front finished logging the results...')
        
