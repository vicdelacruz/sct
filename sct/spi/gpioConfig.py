import RPi.GPIO as GPIO
from sct.logger.sctLogger import SctLogger


class GpioConfig:
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        self.ce_max5322     = [19]
        self.ce_ads8638     = [20]
        self.ce_max7301     = [21]
        self.gpio_list      = self.ce_max5322 + self.ce_ads8638 + self.ce_max7301
        self.mode           = GPIO.BCM
        self.warn           = False

