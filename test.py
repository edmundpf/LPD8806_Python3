#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 36;
led = strand(num)
led.setAutoUpdate()
led.setChannelOrder(ChannelOrder.BRG)
led.all_off()

#for i in range(384*2):
#	led.anim_rainbow()


color = Color()
color.setHSV(0.8, 1.0, 1.0)
for i in range(num*8):
	led.anim_larson_scanner(color, 3)
	sleep(0.01)

	
led.all_off()

#for i in range(384):
#	led.anim_rainbow_cycle()








led.all_off()


