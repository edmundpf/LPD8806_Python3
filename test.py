#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 36;
led = strand(num)
#led.setAutoUpdate()
led.setChannelOrder(ChannelOrder.BRG)
led.fillOff()

color = Color()
color.setHue(0.0)

for i in range(384):
	led.anim_rainbow()
	led.update()
	
led.fillOff()
sleep(0.5)
	
for i in range(384):
	led.anim_rainbow_cycle()
	led.update()
	
led.fillOff()

color.setRGB(127, 255, 0)
for i in range(num*4):
	led.anim_color_wipe(color)
	led.update()
	sleep(0.03)
	
led.fillOff()

color.setRGB(127, 127, 255)
for i in range(num*4):
	led.anim_color_chase(color)
	led.update()
	sleep(0.03)

led.fillOff()

color.setRGB(255, 0, 0)
for i in range(num*4):
	led.anim_larson_scanner(color)
	led.update()
	sleep(0.03)

led.fillOff()

for i in range(num*4):
	led.anim_larson_rainbow(2, 0.5)
	led.update()
	sleep(0.05)

led.fillOff()
led.update()



