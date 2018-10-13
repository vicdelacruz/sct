'''
Created on 6 Apr 2018

@author: BIKOYPOGI
'''
import signal
import sys
from controller.front import FrontController
from resources import props

app = FrontController()

def sigHandler(sig, frame):
     app.stop()
     sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigHandler)
    app.monitor(props.cmdPath, props.logDir)
