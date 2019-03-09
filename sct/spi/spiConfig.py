from sct.logger.sctLogger import SctLogger

class SpiConfig:
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        self.bitsPerWord    = 8 
        self.csHigh         = True
        self.loop           = False
        self.lsbFirst       = False
        self.maxSpeedHz     = 32000
        self.mode           = 0b01
        self.threeWire      = False
