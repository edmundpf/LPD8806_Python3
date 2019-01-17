from bootstrap import *

anim = Rainbow(led)
while 1:
	anim.step()
	led.update()
