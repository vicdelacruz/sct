'''
Created on 22 Sep 2018

@author: BIKOYPOGI
'''
import sys, signal
from unittest.mock import MagicMock
try:
    from spidev import SpiDev
    import RPi.GPIO as GPIO
except ImportError:
    SpiDev = MagicMock()
    GPIO = MagicMock()
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
        if port in self.gpioCfg.gpio_list:
            GPIO.output(port, GPIO.LOW)
        else:
            self.logger.error("GPIO port {} not found in GpioList {}...".format(port, self.gpioCfg.gpio_list))

    def unsetCE(self):
        GPIO.output(self.gpioCfg.gpio_list, GPIO.HIGH)

    def open(self, cs):
        if cs == 0:
            #self.logger.debug("Opening SPI 0,0...")
            self.spi.open(0, 0)
            self.initSpi(self.spiCfg)
        elif (cs > 0 and cs < 4):
            #self.logger.debug("Opening SPI 0,1 with CE {}...".format(cs-1))
            self.setCE(self.gpioCfg.gpio_list[cs-1])
            self.spi.open(0, 1)
            self.initSpi(self.spiCfg)
        else:
            self.logger.error("CS #{} not valid...".format(cs))

    def close(self):
        #self.logger.debug("Closing SPI and resetting CE's...")
        self.spi.close()
        self.unsetCE()

    def cfg_write(self, cs, data, speed=125000000, mode=0b00):
        self.open(cs)
        self.spi.max_speed_hz = speed
        self.spi.mode = mode 
        self.logger.debug("SPI sending [{}] to dev 0x{} @ {:.2E}Hz".format(', '.join(hex(x) for x in data), cs, speed))
        result = self.spi.xfer2(data)
        self.close()
        return result

    def cfg_read(self, cs, data, speed=125000000):
        hbyte, lbyte = data
        self.open(cs)
        self.spi.max_speed_hz = speed
        result = self.spi.xfer2([hbyte, lbyte])
        if isinstance(SpiDev, MagicMock):
            result = [0x00, 0x00]
        msb, lsb = result
        self.logger.debug("SPI received [0x{:02x}, 0x{:02x}] from dev 0x{:x} @ {:.3E} Hz".format(msb, lsb, cs, speed))
        self.close()
        return result

    def sanitize(self, data):
        if isinstance(data, list):
            return data
        else:
            return([data])

    def cleanup(self):
        try:
            self.spi.close()
            GPIO.cleanup()
        except:
            self.logger.info("Nothing to cleanup...")
