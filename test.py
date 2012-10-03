#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 36;
led = strand(num)
led.setAutoUpdate()
led.setChannelOrder(ChannelOrder.BRG)
led.all_off()

color = Color()

for i in range(384):
	led.anim_rainbow()
	
led.all_off()
sleep(0.5)
	
for i in range(384):
	led.anim_rainbow_cycle()
	
led.all_off()

color.setHSV(0.8, 1.0, 1.0)
for i in range(num*4):
	led.anim_color_wipe(color)
	sleep(0.03)
	
led.all_off()

color.setHSV(0.2, 1.0, 1.0)
for i in range(num*4):
	led.anim_color_chase(color)
	sleep(0.03)

led.all_off()

for i in range(num*8):
	led.anim_larson_scanner(color, 3)
	sleep(0.03)

led.all_off()

for i in range(num*8):
	led.anim_larson_scanner(color, 3, 9, 18)
	sleep(0.03)

led.all_off()

#for i in range(384):
#	led.anim_rainbow_cycle()








led.all_off()


