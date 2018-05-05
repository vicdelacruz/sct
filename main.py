'''
Created on 6 Apr 2018

@author: BIKOYPOGI
'''
from controller.front import FrontController

if __name__ == '__main__':
    app = FrontController()
    app.load()
    app.executeAll()