'''
Created on 9 Apr 2018

@author: BIKOYPOGI
'''
from model.tp import Tp
from lxml import etree


class FileHandler:
    '''
    This class handles all file processing.
    
    Attributes:
        filepath   Directory and filename in dirPath/fileName.ext format
    '''


    def __init__(self, fullpath = None):
        '''
        Constructor
        '''
        self.fullpath = fullpath
        self.tp = Tp()
        print('FileHandler is initialized...')

                
    def load(self):
        self.parse(self.fullpath)
        print(etree.tostring(self.tp.programtree))
        return self.tp
            
    def parse(self, fullpath):
        parsed = etree.parse(fullpath)
        print(parsed.getroot().tag)
        if (parsed.getroot().tag == 'Testprogram'):
            self.tp.programtree = parsed
            print(etree.tostring(parsed))
        
        