'''
Created on 19 Apr 2018

@author: BIKOYPOGI
'''

from lxml import etree

class Tp:
    '''
    Holds the whole testprogram
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.programtree = etree.ElementTree()
        self.resulttree = etree.ElementTree()
        print('Tp is initialized...')