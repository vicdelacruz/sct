'''
Created on 5 May 2018

@author: BIKOYPOGI
'''
import os
import time
from lxml import etree
from sct.util.fileHandler import FileHandler
from sct.model.tp import Tp
from sct.controller.flowRunner import FlowRunner
from sct.logger.sctLogger import SctLogger
from sct.status.status import Status

class FrontController(object):
    '''
    classdocs
    '''
    logger = SctLogger().getLogger(__name__)

    def __init__(self, mainView = None):
        '''
        Constructor
        '''
        self.goState = True 
        self.tp = Tp()
        self.fh = FileHandler()
        self.mainView = mainView
        self.results = None
        self.status = Status()
        self.logger.debug('Front Controller is initialized...')

    def monitor(self, cmdPath=None, logDir = None, testMode = False):
        self.status.updateState('waiting')
        self.logState()
        if testMode:
            self.processCmds(self.fh.loadCmd(cmdPath), logDir)
        else:
            while self.goState:
                self.logger.debug("Polling for CMD file in %s", os.path.abspath(os.path.join(os.getcwd(), cmdPath)))
                self.status.updateState('waiting')
                time.sleep(10)
                if os.path.exists(cmdPath):
                    self.logger.info('Front is loading CMD file...')
                    self.processCmds(self.fh.loadCmd(cmdPath), logDir)

    def stop(self):
        self.logger.warning('SCT is shutting down...')
        self.status.updateState('shutdown')
        self.logState()
        self.goState = False

    def processCmds(self, cmds, logDir):
        for cmd in cmds:
            op = cmd.split()
            if op[0] == 'LOAD':
                self.load(op[1])
            elif op[0] == 'EXECUTE_ALL':
                self.executeAll()
            elif op[0] == 'LOG_ALL':
                self.logAll(logDir, op[1])
            elif op[0] == 'GET_STATUS':
                self.logState(logDir)
            elif op[0] == 'STOP':
                self.stop()
            else:
                pass
        
    def load(self, tpPath=None):
        self.logger.info('Front is loading TP...')
        self.status.updateState('loading')
        self.logState()
        self.tp = self.fh.loadTp(tpPath)
        self.logger.debug(etree.tostring(self.tp.programtree))
        self.status.updateState('waiting')
        self.logState()
        
    def executeAll(self):
        if self.tp is not None:
            flowrunner = FlowRunner(self.tp)
            self.status.updateState('testing')
            self.logState()
            self.results = flowrunner.executeAll()
            self.status.updateState('waiting')
            self.logState()
            self.logger.info('SCT finished running the tests...')   
        
    def logAll(self, logDir=None, logFile=None):
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        self.status.updateState('testing')
        self.logState()
        self.fh.logResults(os.path.join(logDir,logFile), self.results)
        self.status.updateState('waiting')
        self.logState()
        self.logger.info('SCT finished logging the results...')   
        
    def logState(self):
        if not os.path.exists(self.status.logDir):
            os.makedirs(self.status.logDir)
        self.logger.info('Asked to log SCT state of \'%s\'...', self.status.state)   
        self.fh.logState(os.path.join(self.status.logDir,self.status.logFile), self.status.state)
        self.logger.debug('SCT finished logging the state...')   
        