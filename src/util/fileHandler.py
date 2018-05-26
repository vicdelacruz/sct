'''
Created on 9 Apr 2018

@author: BIKOYPOGI
'''
from model.tp import Tp
from lxml import etree
import os

class FileHandler:
    '''
    This class handles all file processing.
    
    Attributes:
        filepath   Directory and filename in dirPath/fileName.ext format
    '''


    def __init__(self):
        '''
        Constructor
        '''
        print('FileHandler is initialized...')

                
    def loadCmd(self, cmdPath=None):
        cmds = self.parseCmd(cmdPath)
        return cmds

    
    def loadTp(self, tpPath=None):
        tp = self.parseTp(tpPath)
        print(etree.tostring(tp.programtree))
        return tp
    
    def parseCmd(self, fullpath):
        cmds = []
        try:
            lines = open(fullpath).readlines()
            for i, cmd in enumerate(lines):
                cmds.append(cmd.strip())
#             print(cmds)
            os.remove(fullpath)
        except:
            pass
        return cmds

            
    def parseTp(self, fullpath):
        tp = Tp()
        parsed = etree.parse(fullpath)
        print(parsed.getroot().tag)
        if (parsed.getroot().tag == 'Testprogram'):
            tp.programtree = parsed
            print(etree.tostring(parsed))
        return tp
        
        