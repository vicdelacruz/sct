'''
Created on 9 Apr 2018

@author: BIKOYPOGI
'''
import os
from lxml import etree
from sct.model.tp import Tp
from sct.logger.sctLogger import SctLogger


class FileHandler:
    '''
    This class handles all file processing.
    
    Attributes:
        filepath   Directory and filename in dirPath/fileName.ext format
    '''
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        '''
        Constructor
        '''
        self.logger.debug('FileHandler is initialized...')
                
    def loadCmd(self, cmdPath=None):
        cmds = self.parseCmd(cmdPath)
        return cmds
    
    def loadTp(self, tpPath=None):
        tp = self.parseTp(tpPath)
        self.logger.debug(etree.tostring(tp.programtree))
        return tp
    
    def parseCmd(self, fullpath):
        cmds = []
        try:
            fh = open(fullpath)
            lines = fh.readlines()
            for i, cmd in enumerate(lines):
                cmds.append(cmd.strip())
            fh.close()
            os.remove(fullpath)
        except Exception as e:
            self.logger.error('Unable to parse %s: %s', fullpath, e)
        return cmds
    
    def logResults(self, logPath=None, results=None):
        try:
            with open(logPath, 'w') as f:
                f.write(etree.tostring(results, pretty_print=True, encoding='unicode'))
        except Exception as e:
            self.logger.error('Unable to log to file: %s', e)
            self.logger.error('%s%s', logPath, '...')
            self.logger.error('%s', etree.tostring(results, pretty_print=True, encoding='unicode'))
            
    def parseTp(self, fullpath):
        tp = Tp()
        parsed = etree.parse(fullpath)
        if (parsed.getroot().tag == 'TestProgram'):
            tp.programtree = parsed
            self.logger.info('TestProgram %s pkg=%s ver=%s found', parsed.getroot().get("name"),
                             parsed.getroot().get("pkg"), parsed.getroot().get("ver"))
        else:
            self.logger.error('Invalid testprogram format in %s', fullpath)
        return tp

    def logState(self, logPath=None, state=None):
        try:
            with open(logPath, 'w') as f:
                f.write(state)
        except Exception as e:
            self.logger.error('Unable to update state %s in %s: %s', state, logPath, e)
