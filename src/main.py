'''
Created on 6 Apr 2018

@author: BIKOYPOGI
'''
from controller.front import FrontController
from resources import props

if __name__ == '__main__':
    app = FrontController()
#     app.load(props.tpPath)
#     app.executeAll()
    app.monitor(props.cmdPath, props.logDir)