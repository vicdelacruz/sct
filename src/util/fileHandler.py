'''
Created on 9 Apr 2018

@author: BIKOYPOGI
'''
from model.tp import Tp
from logger.sctLogger import SctLogger
from lxml import etree
import os

class FileHandler:
    '''
    This class handles all file processing.
    
    Attributes:
        filepath   Directory and filename in dirPath/fileName.ext format
    '''
    logger = SctLogger(__name__).logger

    def __init__(self):
        '''
        Constructor
        '''
        self.logger.info('FileHandler is initialized...')

                
    def loadCmd(self, cmdPath=None):
        cmds = self.parseCmd(cmdPath)
        return cmds

    
    def loadTp(self, tpPath=None):
        tp = self.parseTp(tpPath)
        self.logger.info(etree.tostring(tp.programtree))
        return tp
    
    def parseCmd(self, fullpath):
        cmds = []
        try:
            lines = open(fullpath).readlines()
            for i, cmd in enumerate(lines):
                cmds.append(cmd.strip())
#             self.logger.info(cmds)
            os.remove(fullpath)
        except:
            pass
        return cmds
    
    def logResults(self, logPath=None, results=None):
        try:
            with open(logPath, 'w') as f:
                f.writelines('{}:{}\n'.format(k,v) for k, v in results.items())
            for k, v in results.items():
                self.logger.info('{}:{}\n'.format(k,v))
        except:
            self.logger.info('Unable to log to file...')
            self.logger.info('...', logPath, '...')
            self.logger.info('...', results, '...')
            
    def parseTp(self, fullpath):
        tp = Tp()
        parsed = etree.parse(fullpath)
        self.logger.info(parsed.getroot().tag)
        if (parsed.getroot().tag == 'Testprogram'):
            tp.programtree = parsed
            self.logger.info(etree.tostring(parsed))
        return tp
        
        
