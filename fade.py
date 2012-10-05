#!/usr/bin/python

from time import sleep
from LPD8806 import *

num = 36;
led = strand(num)
#led.setAutoUpdate()
led.setChannelOrder(ChannelOrder.BRG)
led.all_off()

for i in range(1, num + 1):
	led.fillOff()
	led.fillRGB(255, 255, 255, 0, i)
	led.update()
	sleep(0.05)

sleep(3.0)

r = 255.0
g = 0.0
b = 0.0
level = 0.0
while level <= 1.0:
	led.fillRGB(r * level, g * level, b * level)
	led.update()
	level += 0.01
	sleep(0.005)

r = 0.0
g = 255.0
b = 0.0
level = 0.0
while level <= 1.0:
	led.fillRGB(r * level, g * level, b * level)
	led.update()
	level += 0.01
	sleep(0.005)
	
r = 0.0
g = 0.0
b = 255.0
level = 0.0
while level <= 1.0:
	led.fillRGB(r * level, g * level, b * level)
	led.update()
	level += 0.01
	sleep(0.005)
	
r = 255.0
g = 255.0
b = 255.0
level = 0.0
while level <= 1.0:
	led.fillRGB(r * level, g * level, b * level)
	led.update()
	level += 0.01
	sleep(0.02)

led.all_off()


