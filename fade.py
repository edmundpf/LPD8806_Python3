#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 36;
led = strand(num)
led.setAutoUpdate()
led.setChannelOrder(ChannelOrder.BRG)
led.all_off()

led.fillRGB(255, 255, 255)
sleep(2)

hue = 0.0
color = Color()
color.setHSV(hue, 1.0, 0.5)

while hue <= 1.0:
	led.fill(color)
	hue += 0.01
	color.setHue(hue)
	sleep(0.03)

value = 0.0	
color.setHSV(0.0, 1.0, value)
while value <= 1.0:
	led.fill(color)
	value += 0.01
	color.setValue(value)
	sleep(0.02)
	
value = 0.0	
color.setHSV(120.0 / 360.0, 1.0, value)
while value <= 1.0:
	led.fill(color)
	value += 0.01
	color.setValue(value)
	sleep(0.02)
	
value = 0.0	
color.setHSV(240.0 / 360.0, 1.0, value)
while value <= 1.0:
	led.fill(color)
	value += 0.01
	color.setValue(value)
	sleep(0.02)

led.all_off()


