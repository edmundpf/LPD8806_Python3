Raspberry Pi library for LPD8806 based RGB light strips
Initial code from: https://github.com/Sh4d/LPD8806

See a demo video here: http://www.youtube.com/watch?v=g5upsgqASiY

Download, extract, then run the help:
  >>> import LPD8806
  >>> help(LPD8806)

 - The LPD8806 chip does not seem to really specify in what order the color channels are, so there is a helper function in case yours happen to be different. The most common seems to be GRB order but I have found some strips that use BRG order as well. If yours (like the one's from Adafruit) use GRB order nothing needs to be done as this is the default. But if the channels are swapped call the method setChannelOrder() with the proper ChannelOrder value. Those are the only two I've ever encountered, but if anyone ever encounters another, please let me know so I can add it.
 
 - All of the animations are designed to allow you to do other things on the same thread in between frames. So, everytime you want to actually progress the animation, call it's method and then call update() to push the data to the the strip. You could do any other processing on the buffer before pushing the update if needed. Each animation has a step variable that can be manually reset or modified externally. See variables in the __init__ of LEDStrip
 
 - If any of the built in animations are not enough you can use any of the set or fill methods to manually manipulate the strip data.
 
 - These strips can get extremely bright