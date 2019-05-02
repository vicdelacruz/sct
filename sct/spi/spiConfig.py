from sct.logger.sctLogger import SctLogger
try:
    from spidev import SpiDev
except ImportError:
    from unittest.mock import MagicMock
    SpiDev = MagicMock()

class SpiConfig:
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        self.bitsPerWord    = 8 
        self.csHigh         = True
        self.loop           = False
        self.lsbFirst       = False
        self.maxSpeedHz     = 125000000
        self.mode           = 0b01
        self.threeWire      = False

    def printVals(self):
        self.logger.debug("spi bitsPerWord = %s" % self.bitsPerWord)
        self.logger.debug("spi csHigh      = %s"      % self.csHigh)
        self.logger.debug("spi loop        = %s"        % self.loop)
        self.logger.debug("spi lsbFirst    = %s"    % self.lsbFirst)
        self.logger.debug("spi maxSpeedHz  = %s"  % self.maxSpeedHz)
        self.logger.debug("spi mode        = %s"        % self.mode)
        self.logger.debug("spi threeWire   = %s"   % self.threeWire)

    def refreshVals(self):
        spi = SpiDev()
        spi.open(0,0)
        self.bitsPerWord    = spi.bits_per_word
        self.csHigh         = spi.cshigh
        self.loop           = spi.loop
        self.lsbFirst       = spi.lsbfirst
        self.maxSpeedHz     = spi.max_speed_hz
        self.mode           = spi.mode
        self.threeWire      = spi.threewire
        spi.close()
