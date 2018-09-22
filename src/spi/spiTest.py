
'''
Created on 22 Sep 2018

@author: BIKOYPOGI
'''
from spiDriver import Driver

driver = Driver()
driver.xfer(0x0, 0b01011010)
driver.xfer2(0x0, 0b11110000)
