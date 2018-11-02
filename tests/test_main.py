'''
Created on Oct 24, 2018

@author: victord
'''
import unittest
import os
from sct.resources import props
from sct.controller.front import FrontController
from logging import FileHandler
import logging

class TestMain(unittest.TestCase):

    def setUp(self):
        self.testLog = os.path.join(props.testDir, props.logFile)
        logging.basicConfig(level=logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s.%(msecs)03d [%(levelname)-8s][%(name)-22s] %(message)s",
            "%Y-%m-%d %H:%M:%S")
        logger = logging.getLogger()
        fhandler = FileHandler(filename=self.testLog, mode='w')
        fhandler.setFormatter(formatter)
        logger.addHandler(fhandler)
        self.app = FrontController()
        cmds = ("LOG_STATUS\n"
                "LOAD sct/repo/TestProgram.xml\n"
                "EXECUTE_ALL\n"
                "LOG_ALL Measurements.xml")
        cmdFile= open(props.cmdPath, 'w')
        cmdFile.write(cmds)
        cmdFile.close()
        self.app.monitor(props.cmdPath, props.logDir, True)

    def tearDown(self):
        self.app.stop()

    def test_Sct(self):
        with open(self.testLog, 'r') as f:
            self.assertTrue('ERROR' not in f.read())     

if __name__ == "__main__":
    unittest.main()
