import RPi.GPIO as GPIO
from sct.logger.sctLogger import SctLogger


class GpioConfig:
    logger = SctLogger().getLogger(__name__)

    def __init__(self):
        self.ce_max5322     = [19]
        self.ce_ads8638     = [20]
        self.ce_mc33996     = [21]
        self.gpio_list      = self.ce_max5322 + self.ce_ads8638 + self.ce_mc33996
        self.mode           = GPIO.BCM
        self.warn           = False

    def printVals(self):
        self.logger.info("ce_max5322 = %s" % self.ce_max5322)
        self.logger.info("ce_ads8638 = %s" % self.ce_ads8638)
        self.logger.info("ce_mc33996 = %s" % self.ce_mc33996)
        self.logger.info("gpio_list  = %s" % self.gpio_list)
        self.logger.info("gpio_mode  = %s" % self.mode)
        self.logger.info("gpio_warn  = %s" % self.warn)
