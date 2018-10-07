'''
Created on 22 Sep 2018

@author: BIKOYPOGI
'''
import spidev
from spi import spiConfig
from logger.sctLogger import SctLogger

class Driver:
    '''
    Raw driver for SPI port in the Raspberry PI.
    
    Attributes:
        addr       The SCT address of the device to write to 
        data       The payload data
    '''
    logger = SctLogger(__name__).logger

    def __init__(self):
        '''
        Constructor
        '''
        self.addr = 0x0
        self.data = 0x0
        self.spi = spidev.SpiDev()
        self.initCfg(self.spi)

    def initCfg(self, spi):
        '''
        spi.bits_per_word = spiConfig.bitsPerWord
        spi.cshigh = spiConfig.csHigh
        spi.loop = spiConfig.loop
        spi.lsbfirst = spiConfig.lsbFirst
        spi.max_speed_hz = spiConfig.maxSpeedHz
        spi.mode = spiConfig.mode
        '''
        self.logger.info("spi bitsPerWord = %s" % spiConfig.bitsPerWord)
        self.logger.info("spi csHigh      = %s"      % spiConfig.csHigh)
        self.logger.info("spi loop        = %s"        % spiConfig.loop)
        self.logger.info("spi lsbFirst    = %s"    % spiConfig.lsbFirst)
        self.logger.info("spi maxSpeedHz  = %s"  % spiConfig.maxSpeedHz)
        self.logger.info("spi mode        = %s"        % spiConfig.mode)

    def setCfg(self, attr, value):
        if not hasattr(self, attr):
            raise AttributeError("config has no setting %s" % attr)
        else:
            setattr(self, attr, value)

    def open(self, addr):
        self.spi.open(0, addr)

    def close(self):
        self.spi.close()

    def xfer(self, addr, data):
        self.open(addr)
        self.spi.xfer(self.sanitize(data))
        self.close()
        self.logger.info("SPI has sent data 0x%x to address 0x%x" % (data, addr))

    def xfer2(self, addr, data):
        self.open(addr)
        self.spi.xfer2(self.sanitize(data))
        self.close()
        self.logger.info("SPI has sent data 0x%x to address 0x%x" % (data, addr))

    def sanitize(self, data):
        if isinstance(data, list):
            return data
        else:
            return([data])

