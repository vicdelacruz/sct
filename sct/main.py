'''
Created on 6 Apr 2018

@author: BIKOYPOGI
'''
import signal
import sys
from sct.controller.front import FrontController
from sct.resources import props

def sigHandler(sig, frame):
    app.stop()
    sys.exit(0)

if __name__ == '__main__':
    app = FrontController()
    signal.signal(signal.SIGINT, sigHandler)
    app.monitor(props.tpPath, props.cmdPath, props.logDir)
