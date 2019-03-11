'''
Created on 22 Sep 2018

@author: BIKOYPOGI
'''
import sys, signal
from spidev import SpiDev
import RPi.GPIO as GPIO
from sct.spi.spiConfig import SpiConfig
from sct.spi.gpioConfig import GpioConfig
from sct.logger.sctLogger import SctLogger

class Driver:
    '''
    Raw driver for SPI port in the Raspberry PI.
    
    Attributes:
        addr       The SCT address of the device to write to 
        data       The payload data
    '''
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        '''
        Constructor
        '''
        self.addr = 0x0
        self.data = 0x0
        self.cleanup()
        self.spi = SpiDev()
        self.spiCfg = SpiConfig()
        #self.initSpi()
        self.gpioCfg = GpioConfig()
        self.initGpio()

    def initSpi(self):
        # SpiConfig
        #self.spi.bits_per_word = self.spiCfg.bitsPerWord
        #self.spi.cshigh        = self.spiCfg.csHigh
        #self.spi.loop          = self.spiCfg.loop
        #self.spi.lsbfirst      = self.spiCfg.lsbFirst
        self.spi.max_speed_hz  = self.spiCfg.maxSpeedHz
        #self.spi.mode          = self.spiCfg.mode

    def initGpio(self):
        GPIO.setwarnings(self.gpioCfg.warn)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioCfg.gpio_list, GPIO.OUT)
        GPIO.output(self.gpioCfg.gpio_list, GPIO.HIGH)

    def setCE(self, port):
        newPort = self.sanitize(port)
        if newPort in self.gpioCfg.gpio_list:
            GPIO.output(newPort, GPIO.LOW)
        else:
            self.logger.error("GPIO port {} not found in GpioList...".format(newPort))

    def unsetCE(self):
        GPIO.output(self.gpioCfg.gpio_list, GPIO.HIGH)

    def open(self, cs):
        if cs == 0:
            self.spi.open(0, 0)
        elif (cs >= 1 and cs < 4):
            self.setCE(self.gpioCfg.gpio_list[cs-1])
            self.spi.open(0, 1)
        else:
            self.logger.error("CS #{} not valid...".format(cs))

    def close(self):
        self.spi.close()
        self.unsetCE()

    def xfer(self, cs, data):
        hbyte, lbyte = self.sanitize(data)
        self.open(cs)
        self.spi.xfer([hbyte, lbyte])
        self.close()
        self.logger.info("SPI has sent data 0x%x 0x%x to dev 0x%x" % (hbyte, lbyte, cs))

    def xfer2(self, cs, data):
        hbyte, lbyte = self.sanitize(data)
        self.open(cs)
        self.spi.xfer([hbyte, lbyte])
        self.close()
        self.logger.info("SPI has sent data 0x%x 0x%x to dev 0x%x" % (hbyte, lbyte, cs))

    def sanitize(self, data):
        if isinstance(data, list):
            return data
        else:
            return([data])

    def setCfg(self, attr, value):
        if not hasattr(self, attr):
            raise AttributeError("config has no setting %s" % attr)
        else:
            setattr(self, attr, value)

    def cleanup(self):
        try:
            self.spi.close()
            GPIO.cleanup()
        except:
            self.logger.info("Nothing to cleanup...")
