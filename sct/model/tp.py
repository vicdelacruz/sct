'''
Created on 19 Apr 2018

@author: BIKOYPOGI
'''

from lxml import etree
from sct.logger.sctLogger import SctLogger

class Tp:
    '''
    Holds the whole testprogram
    '''
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        '''
        Constructor
        '''
        self.programtree = etree.ElementTree()
        self.resulttree = etree.ElementTree()
        self.logger.debug('Tp is initialized...')
