'''
Created on 19 Apr 2018

@author: BIKOYPOGI
'''

from lxml import etree
from logger.sctLogger import SctLogger

class Tp:
    '''
    Holds the whole testprogram
    '''
    logger = SctLogger(__name__).getLogger()

    def __init__(self):
        '''
        Constructor
        '''
        self.programtree = etree.ElementTree()
        self.resulttree = etree.ElementTree()
        self.logger.info('Tp is initialized...')
