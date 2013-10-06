#!/usr/bin/python

from time import sleep
from LPD8806 import *
from animation import *

num = 32;
led = LEDStrip(num)
#led.setChannelOrder(ChannelOrder.BRG) #Only use this if your strip does not use the GRB order
#led.setMasterBrightness(0.5) #use this to set the overall max brightness of the strip
led.all_off()

#setup colors to loop through for fade
colors = [
	(255.0,0.0,0.0),
	(0.0,255.0,0.0),
	(0.0,0.0,255.0),
	(255.0,255.0,255.0),
]

step = 0.01
for c in range(4):
	r, g, b = colors[c]
	level = 0.01
	dir = step
	while level >= 0.0:
		led.fill(Color(r, g, b, level))
		led.update()
		if(level >= 0.99):
			dir = -step
		level += dir
		sleep(0.005)
		
led.all_off()

#animations - each animation method moves the animation forward one step on each call
#after each step, call update() to push it to the LED strip
#sin wave animations
color = Color(255, 0, 0)
anim = Wave(led)
for i in range(led.lastIndex):
	anim.step(color, 4)
	sleep(0.15)
	
color = Color(0, 0, 100)
anim = Wave(led)
for i in range(led.lastIndex):
	anim.step(color, 2)
	sleep(0.15)


#rolling rainbow
anim = Rainbow(led)
for i in range(384):
	anim.step()

led.fillOff()
	
#evenly distributed rainbow
anim = RainbowCycle(led)
for i in range(384*2):
	anim.step()

led.fillOff()

#setup colors for wipe and chase
colors = [
	Color(255, 0, 0),
	Color(0, 255, 0),
	Color(0, 0, 255),
	Color(255, 255, 255),
]

anim = ColorWipe(led)
for c in range(4):
	for i in range(num):
		anim.step(colors[c])
		sleep(0.03)
	
led.fillOff()

anim = ColorChase(led)
for c in range(4):
	for i in range(num):
		anim.step(colors[c])
		sleep(0.03)
		
led.fillOff()

#scanner: single color and changing color
color = Color(255, 0, 0)
anim = LarsonScanner(led)
for i in range(led.lastIndex*4):
	anim.step(color)
	sleep(0.03)

led.fillOff()

anim = LarsonRainbow(led)
for i in range(led.lastIndex*4):
	anim.step(2, 0.5)
	sleep(0.03)

led.all_off()



