from sct.logger.sctLogger import SctLogger

class SpiConfig:
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        self.bitsPerWord    = 8 
        self.csHigh         = True
        self.loop           = False
        self.lsbFirst       = False
        self.maxSpeedHz     = 1000000
        self.mode           = 0b01
        self.threeWire      = False
        self.logger.info("spi bitsPerWord = %s" % self.bitsPerWord)
        self.logger.info("spi csHigh      = %s"      % self.csHigh)
        self.logger.info("spi loop        = %s"        % self.loop)
        self.logger.info("spi lsbFirst    = %s"    % self.lsbFirst)
        self.logger.info("spi maxSpeedHz  = %s"  % self.maxSpeedHz)
        self.logger.info("spi mode        = %s"        % self.mode)
