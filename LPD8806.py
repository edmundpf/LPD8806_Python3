#!/usr/bin/env python
import colorsys

"""
LPD8806.py: Raspberry Pi library for LPD8806 based RGB light strips
Initial code from: https://github.com/Sh4d/LPD8806

Provides the ability to drive a LPD8806 based strand of RGB leds from the
Raspberry Pi

Colors are provided as RGB and converted internally to the strand's 7 bit
values.


Wiring:
	Pi MOSI -> Strand DI
	Pi SCLK -> Strand CI

Make sure to use an external power supply to power the strand

Example:
	>> import LPD8806
	>> led = LPD8806.strand()
	>> led.fill(255, 0, 0)
"""

#Not all LPD8806 strands are created equal.
#Some, like Adafruit's use GRB order and the other common order is GRB
#Library defaults to GRB but you can call strand.setChannelOrder(ChannelOrder) 
#to set the order your strands use
class ChannelOrder:
	RGB = [0,1,2] #Probably not used, here for clarity
	GRB = [1,0,2] #Strands from Adafruit and some others (default)
	BRG = [1,2,0] #Strands from many other manufacturers
	
class Color:
	
	def __init__(self):
		self.R = 0.0
		self.G = 0.0
		self.B = 0.0
		self.H = 0.0
		self.S = 1.0
		self.V = 1.0
		
	def setRGB(self, r, g, b):
		if(r > 255.0 or r < 0.0 or g > 255.0 or g < 0.0 or b > 255.0 or b < 0.0):
			raise ValueError('RGB values must be between 0 and 255')
		self.R = float(r)
		self.G = float(g)
		self.B = float(b)
		h, s, v = colorsys.rgb_to_hsv((float(r)/255.0), (float(g)/255.0), (float(b)/255.0))
		self.H = h
		self.S = s
		self.V = v
		
	def setHSV(self, h, s, v):
		if(h > 360.0 or h < 0.0):
			raise ValueError('Hue value must be between 0.0 and 360.0')
		if(s > 1.0 or s < 0.0):
			raise ValueError('Saturation must be between 0.0 and 1.0')
		if(v > 1.0 or v < 0.0):
			raise ValueError('Value must be between 0.0 and 1.0')
		r, g, b = colorsys.hsv_to_rgb(h / 360.0, s, v)
		self.R = r * 255.0
		self.G = g * 255.0
		self.B = b * 255.0
		self.H = h
		self.S = s
		self.V = v
		
	def setHue(self, hue):
		self.setHSV(hue, self.S, self.V)		
		

class strand:

	def __init__(self, leds, dev="/dev/spidev0.0"):
		#Variables:
		#	leds -- strand size
		#	dev -- spi device
		
		self.auto_update = False
		self.c_order = ChannelOrder.GRB
		self.dev = dev
		self.spi = file(self.dev, "wb")
		self.leds = leds
		self.lastIndex = self.leds - 1
		self.gamma = bytearray(256)
		self.buffer = [0 for x in range(self.leds + 1)]
		
		#anim step vars
		self.wheelStep = 0
		self.rainbowStep = 0
		self.rainbowCycleStep = 0
		self.wipeStep = 0
		self.chaseStep = 0
		self.larsonStep = 0
		self.larsonDir = 0
		self.larsonLast = 0
		
		for led in range(self.leds):
			self.buffer[led] = bytearray(3)
		for i in range(256):
			# Color calculations from
			# http://learn.adafruit.com/light-painting-with-raspberry-pi
			self.gamma[i] = 0x80 | int(
				pow(float(i) / 255.0, 2.5) * 127.0 + 0.5
			)

	#Allows for easily using LED strands with different channel orders
	def setChannelOrder(self, order):
		self.c_order = order
	
	#When true state change methods will not wait for update() to push the changes
	def setAutoUpdate(self, state=True):
		self.auto_update = state
		
	#Push new data to strand
	#Not needed if Auto Update is enaabled
	def update(self):
		for x in range(self.leds):
			self.spi.write(self.buffer[x])
			self.spi.flush()
		self.spi.write(bytearray(b'\x00'))
		self.spi.flush()
		
	#update if autoUpdate is True
	def __auto_update(self):
		if self.auto_update == True:
			self.update()
			
	#Fill the strand (or a subset) with a single color using a Color object
	def fill(self, color, start=0, end=0):
		if start < 0:
			start = 0
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
		for led in range(start, end + 1): #since 0-index include end in range
			self.__set_internal(led, color)

		self.__auto_update()

	#Fill the strand (or a subset) with a single color using RGB values
	def fillRGB(self, r, g, b, start=0, end=0):
		color = Color()
		color.setRGB(r, g, b)
		self.fill(color, start, end)
		
	#Fill the strand (or a subset) with a single color using HSV values
	def fillHSV(self, h, s, v, start=0, end=0):
		color = Color()
		color.setHSV(h, s, v)
		self.fill(color, start, end)

	#Fill the strand (or a subset) with a single color using a Hue value. 
	#Saturation and Value components of HSV are set to max.
	def fillHue(self, hue, start=0, end=0):
		color = Color()
		color.setHSV(hue, 1.0, 1.0)
		self.fill(color, start, end)
		
	def fillOff(self, start=0, end=0):
		self.fillRGB(0, 0, 0, start, end)

	#internal use only. sets pixel color
	def __set_internal(self, pixel, color):
		self.buffer[pixel][self.c_order[0]] = self.gamma[int(color.R)]
		self.buffer[pixel][self.c_order[1]] = self.gamma[int(color.G)]
		self.buffer[pixel][self.c_order[2]] = self.gamma[int(color.B)]
		
	#Set single pixel to Color value
	def set(self, pixel, color):
		self.__set_internal(pixel, color)

		self.__auto_update()

	#Set single pixel to RGB value
	def setRGB(self, pixel, r, g, b):
		color = Color()
		color.setRGB(r, g, b)
		self.set(pixel, color)
		
	#Set single pixel to HSV value
	def setHSV(self, pixel, h, s, v):
		color = Color()
		color.setHSV(h, s, v)
		self.set(pixel, color)

	#Set single pixel to Hue value.
	#Saturation and Value components of HSV are set to max.
	def setHue(self, pixel, hue):
		color = Color()
		color.setHSV(hue, 1.0, 1.0)
		self.set(pixel, color)
		
	#turns off the desired pixel
	def setOff(self, pixel):
		self.setRGB(pixel, 0, 0, 0)

	#Turn all LEDs off.
	def all_off(self):
		auto = self.auto_update
		self.setAutoUpdate(True)
		self.fillRGB(0,0,0)
		self.fillRGB(0,0,0)
		self.setAutoUpdate(auto)
		
	#Get color from wheel value (0 - 384)
	def wheel_color(self, wheelpos):
		if wheelpos < 0:
			wheelpos = 0
		if wheelpos > 384:
			wheelpos = 384
			
		if wheelpos < 128:
			r = 127 - wheelpos % 128
			g = wheelpos % 128
			b = 0
		elif wheelpos < 256:
			g = 127 - wheelpos % 128
			b = wheelpos % 128
			r = 0
		else:
			b = 127 - wheelpos % 128
			r = wheelpos % 128
			g = 0
			
		color = Color()
		color.setRGB(r, g, b)
		return color

	#generate rainbow
	def anim_rainbow(self, start=0, end=0):
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
		size = end - start + 1
		
		auto = self.auto_update
		self.setAutoUpdate(False)
		for i in range(size):
			color = (i + self.rainbowStep) % 384
			c = self.wheel_color(color)
			self.set(start + i, c)
		self.setAutoUpdate(auto)
		
		self.__auto_update()
		self.rainbowStep += 1
		if self.rainbowStep > 384:
			self.rainbowStep = 0
		
	#Generate rainbow wheel equally distributed over strip
	def anim_rainbow_cycle(self, start=0, end=0):
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
		size = end - start + 1
		
		auto = self.auto_update
		self.setAutoUpdate(False)
		for i in range(size):
			color = (i * (384 / size) + self.rainbowCycleStep) % 384
			c = self.wheel_color(color)
			self.set(start + i, c)
		self.setAutoUpdate(auto)
		
		self.__auto_update()
		self.rainbowCycleStep += 1
		if self.rainbowCycleStep > 384:
			self.rainbowCycleStep = 0
		
	#fill the dots progressively along the strip
	def anim_color_wipe(self, color, start=0, end=0):
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
			
		auto = self.auto_update
		self.setAutoUpdate(False)
		if(self.wipeStep == 0):
			self.fillOff()
		
		self.set(start + self.wipeStep, color)
		self.setAutoUpdate(auto)
		
		self.__auto_update()
		self.wipeStep += 1
		if start + self.wipeStep > end:
			self.wipeStep = 0
		
	#chase one pixel down the strip
	def anim_color_chase(self, color, start=0, end=0):
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
			
		auto = self.auto_update
		self.setAutoUpdate(False)
		#self.fillOff()
		if(self.chaseStep == 0):
			self.setOff(end)
		else:
			self.setOff(start + self.chaseStep - 1)
			
		self.set(start + self.chaseStep, color)
		self.setAutoUpdate(auto)
		
		self.__auto_update()
		self.chaseStep += 1
		if start + self.chaseStep > end:
			self.chaseStep = 0
		
	#larson scanner (i.e. Cylon Eye or K.I.T.T.)
	def anim_larson_scanner(self, color, tail=2, fade=0.75, start=0, end=0):
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
		size = end - start
		
		tail += 1 #makes tail math later easier
		if tail >= size / 2:
			tail = (size / 2) - 1
		
		auto = self.auto_update
		self.setAutoUpdate(False)
		
		self.larsonLast = start + self.larsonStep;
		self.set(self.larsonLast, color)
		
		tl = tail
		if(self.larsonLast + tl > end):
			tl = end - self.larsonLast
		tr = tail
		if(self.larsonLast - tr < start):
			tr = self.larsonLast - start
			
		for l in range(1, tl + 1):
			level = (float(tail - l) / float(tail)) * fade
			self.setRGB(self.larsonLast + l, color.R * level, color.G * level, color.B * level)

		if(self.larsonLast + tl + 1 <= end):
			self.setOff(self.larsonLast + tl + 1)
			
		for r in range(1, tr + 1):
			level = (float(tail - r) / float(tail)) * fade
			self.setRGB(self.larsonLast - r, color.R * level, color.G * level, color.B * level)

			
		if(self.larsonLast - tr - 1 >= start):
			self.setOff(self.larsonLast - tr - 1)
		
		self.setAutoUpdate(auto)
		self.__auto_update()
		
		if start + self.larsonStep == end:
			self.larsonDir = 1
		elif self.larsonStep == 0:
			self.larsonDir = 0
			
		if self.larsonDir == 0:
			self.larsonStep += 1
		else:
			self.larsonStep -= 1
		
	#larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow
	def anim_larson_rainbow(self, tail=2, fade=0.75, start=0, end=0):
		if end == 0 or end > self.lastIndex:
			end = self.lastIndex
		size = end - start
		
		hue = (self.larsonStep * (360 / size))
		color = Color()
		color.setHue(hue)
		
		self.anim_larson_scanner(color, tail, fade, start, end)
		

