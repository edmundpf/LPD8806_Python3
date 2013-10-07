import math
import time
from color import Color, ColorHSV, wheel_color


class BaseAnimation(object):
    def __init__(self, led, start, end):
        self._led = led
        self._start = start

        self._end = end
        if self._end == 0 or self._end > self._led.lastIndex:
            self._end = self._led.lastIndex

        self._size = self._end - self._start + 1
        self._step = 0

    def step(self):
        raise RuntimeError("Base class step() called. This shouldn't happen")

    def run(self, sleep=None):
        while True:
            self.step()
            self._led.update()
            if sleep:
                time.sleep(sleep)


class Rainbow(BaseAnimation):
    """Generate rainbow."""

    def __init__(self, led, start=0, end=0):
        super(Rainbow, self).__init__(led, start, end)

    def step(self):
        for i in range(self._size):
            color = (i + self._step) % 384
            self._led.set(self._start + i, wheel_color(color))

        self._step += 1
        if self._step > 384:
            self._step = 0


class RainbowCycle(BaseAnimation):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led, start=0, end=0):
        super(RainbowCycle, self).__init__(led, start, end)

    def step(self):
        for i in range(self._size):
            color = (i * (384 / self._size) + self._step) % 384
            self._led.set(self._start + i, wheel_color(color))

        self._step += 1
        if self._step > 384:
            self._step = 0


class ColorWipe(BaseAnimation):
    """Fill the dots progressively along the strip."""

    def __init__(self, led, color, start=0, end=0):
        super(ColorWipe, self).__init__(led, start, end)
        self._color = color

    def step(self):
        if self._step == 0:
            self._led.fillOff()

        self._led.set(self._start + self._step, self._color)

        self._step += 1
        if self._start + self._step > self._end:
            self._step = 0


class ColorChase(BaseAnimation):
    """Chase one pixel down the strip."""

    def __init__(self, led, color, start=0, end=0):
        super(ColorChase, self).__init__(led, start, end)
        self._color = color

    def step(self):
        if self._step == 0:
            self._led.setOff(self._end)
        else:
            self._led.setOff(self._start + self._step - 1)

        self._led.set(self._start + self._step, self._color)

        self._step += 1
        if self._start + self._step > self._end:
            self._step = 0


class LarsonScanner(BaseAnimation):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, led, color, tail=2, fade=0.75, start=0, end=0):
        super(LarsonScanner, self).__init__(led, start, end)
        self._color = color
        self._tail = tail
        self._fade = fade
        self._direction = -1
        self._last = 0

    def step(self):
        self._tail += 1  # makes tail math later easier
        if self._tail >= self._size / 2:
            self._tail = (self._size / 2) - 1

        self._last = self._start + self._step
        self._led.set(self._last, self._color)

        tl = self._tail
        if self._last + tl > self._end:
            tl = self._end - self._last
        tr = self._tail
        if self._last - tr < self._start:
            tr = self._last - self._start

        for l in range(1, tl + 1):
            level = (float(self._tail - l) / float(self._tail)) * self._fade
            self._led.setRGB(self._last + l,
                             self._color.r * level,
                             self._color.g * level,
                             self._color.b * level)

        if self._last + tl + 1 <= self._end:
            self._led.setOff(self._last + tl + 1)

        for r in range(1, tr + 1):
            level = (float(self._tail - r) / float(self._tail)) * self._fade
            self._led.setRGB(self._last - r,
                             self._color.r * level,
                             self._color.g * level,
                             self._color.b * level)

        if self._last - tr - 1 >= self._start:
            self._led.setOff(self._last - tr - 1)

        if self._start + self._step == self._end:
            self._direction = -self._direction
        elif self._step == 0:
            self._direction = -self._direction

        self._step += self._direction


class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def __init__(self, led, tail=2, fade=0.75, start=0, end=0):
        super(LarsonRainbow, self).__init__(
            led, ColorHSV(0).get_color_rgb(), tail, fade, start, end)

    def step(self):
        self._color = ColorHSV(self._step * (360 / self._size)).get_color_rgb()

        super(LarsonRainbow, self).step()


class Wave(BaseAnimation):
    """Sine wave animation."""

    def __init__(self, led, color, cycles, start=0, end=0):
        super(Wave, self).__init__(led, start, end)
        self._color = color
        self._cycles = cycles

    def step(self):
        for i in range(self._size):
            y = math.sin(
                math.pi *
                float(self._cycles) *
                float(self._step * i) /
                float(self._size))

            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                c2 = Color(255 - float(255 - self._color.r) * y,
                           255 - float(255 - self._color.g) * y,
                           255 - float(255 - self._color.b) * y)
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                c2 = Color(float(self._color.r) * y,
                           float(self._color.g) * y,
                           float(self._color.b) * y)
            self._led.set(self._start + i, c2)

        self._step += 1
