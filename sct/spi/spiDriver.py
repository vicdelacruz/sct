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
from pprint import pprint

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
        #self.spiCfg = SpiConfig()
        self.gpioCfg = GpioConfig()
        self.initGpio()

    def initSpi(self):
        # SpiConfig
        self.logger.info("Before ...")
        self.logger.info("spi bitsPerWord = %s" % self.spi.bits_per_word)
        self.logger.info("spi csHigh      = %s"      % self.spi.cshigh)
        self.logger.info("spi loop        = %s"        % self.spi.loop)
        self.logger.info("spi lsbFirst    = %s"    % self.spi.lsbfirst)
        self.logger.info("spi maxSpeedHz  = %s"  % self.spi.max_speed_hz)
        self.logger.info("spi mode        = %s"        % self.spi.mode)
        self.spi.bits_per_word = self.spiCfg.bitsPerWord
        self.spi.cshigh =        self.spiCfg.csHigh
        self.spi.loop =          self.spiCfg.loop
        self.spi.lsbfirst =      self.spiCfg.lsbFirst
        self.spi.max_speed_hz =  self.spiCfg.maxSpeedHz
        self.spi.mode =          self.spiCfg.mode
        self.logger.info("After...")
        self.logger.info("spi bitsPerWord = %s" % self.spi.bits_per_word)
        self.logger.info("spi csHigh      = %s"      % self.spi.cshigh)
        self.logger.info("spi loop        = %s"        % self.spi.loop)
        self.logger.info("spi lsbFirst    = %s"    % self.spi.lsbfirst)
        self.logger.info("spi maxSpeedHz  = %s"  % self.spi.max_speed_hz)
        self.logger.info("spi mode        = %s"        % self.spi.mode)

    def initGpio(self):
        GPIO.setwarnings(self.gpioCfg.warn)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioCfg.gpio_list, GPIO.OUT)
        GPIO.output(self.gpioCfg.gpio_list, GPIO.HIGH)

    def setCE(self, port):
        newPort = self.sanitize(port)
        if port in self.gpioCfg.gpio_list:
            GPIO.output(newPort, GPIO.LOW)
        else:
            self.logger.error("GPIO port {} not found in GpioList {}...".format(newPort, self.gpioCfg.gpio_list))

    def unsetCE(self):
        GPIO.output(self.gpioCfg.gpio_list, GPIO.HIGH)

    def open(self, cs):
        if cs == 0:
            self.spi.open(0, 0)
            #self.initSpi()
        elif (cs >= 1 and cs < 4):
            self.setCE(self.gpioCfg.gpio_list[cs-1])
            self.spi.open(0, 1)
            #self.initSpi()
        else:
            self.logger.error("CS #{} not valid...".format(cs))

    def close(self):
        self.spi.close()
        self.unsetCE()

    def xfer(self, cs, data):
        hbyte, lbyte = self.sanitize(data)
        self.open(cs)
        xfer_speed = self.spi.max_speed_hz
        self.spi.xfer([hbyte, lbyte])
        self.close()
        self.logger.info("SPI sent 0x%x 0x%x to dev 0x%x @ %.3E Hz" % (hbyte, lbyte, cs, xfer_speed))

    def xfer2(self, cs, data):
        hbyte, lbyte = self.sanitize(data)
        self.open(cs)
        xfer_speed = self.spi.max_speed_hz
        self.spi.xfer([hbyte, lbyte])
        self.close()
        self.logger.info("SPI sent 0x%x 0x%x to dev 0x%x @ %.3E Hz" % (hbyte, lbyte, cs, xfer_speed))

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
