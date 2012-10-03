#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 36*5;
led = strand(num)
led.setAutoUpdate()
led.setChannelOrder(ChannelOrder.BRG)
led.all_off()


