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
        self.cleanup()

        self.spi = SpiDev()
        self.spiCfg = SpiConfig()
        #use default spidev values for now
        self.spiCfg.refreshVals()

        self.gpioCfg = GpioConfig()
        self.initGpio()

    def initSpi(self, spiCfg):
        self.spi.bits_per_word = spiCfg.bitsPerWord
        self.spi.cshigh =        spiCfg.csHigh
        self.spi.loop =          spiCfg.loop
        self.spi.lsbfirst =      spiCfg.lsbFirst
        self.spi.max_speed_hz =  spiCfg.maxSpeedHz
        self.spi.mode =          spiCfg.mode
        self.spi.threewire =     spiCfg.threeWire

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
            self.logger.info("Opening SPI 0,0...")
            self.spi.open(0, 0)
            self.initSpi(self.spiCfg)
        elif (cs > 0 and cs < 4):
            self.logger.info("Opening SPI 0,1 with CE {}...".format(cs-1))
            self.setCE(self.gpioCfg.gpio_list[cs-1])
            self.spi.open(0, 1)
            self.initSpi(self.spiCfg)
        else:
            self.logger.error("CS #{} not valid...".format(cs))

    def close(self):
        self.logger.info("Closing SPI and resetting CE's...")
        self.spi.close()
        self.unsetCE()

    def cfg_write(self, cs, data, speed=125000000):
        hbyte, lbyte = self.sanitize(data)
        self.open(cs)
        self.spi.max_speed_hz = speed
        result = self.spi.xfer2([hbyte, lbyte])
        self.close()
        self.logger.info("SPI sent 0x%x 0x%x to dev 0x%x @ %.3E Hz" % (hbyte, lbyte, cs, speed))
        return result

    def cfg_read(self, cs, data, speed=125000000):
        hbyte, lbyte = self.sanitize(data)
        self.open(cs)
        self.spi.max_speed_hz = speed
        result = self.spi.xfer2([hbyte, lbyte])
        self.close()
        msb, lsb = result
        self.logger.info("SPI received 0x%x 0x%x from dev 0x%x @ %.3E Hz" % (msb, lsb, cs, speed))
        return result

    def adc_read(self, data, speed=125000000):
        cs = self.gpioCfg.gpio_list.index(self.gpioCfg.ce_ads8638[0]) + 1
        self.cfg_write(cs, data, speed)
        hbyte, lbyte = self.cfg_read(cs, [0x00, 0x00], speed)
        self.close()
        chbyte = (0xF0 & hbyte) >> 4
        adcout_msb = 0x0F & hbyte
        adcout = adcout_msb*256 + lbyte
        return [chbyte, adcout]

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
