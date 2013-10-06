import math
from color import Color, ColorHSV, wheel_color


class Rainbow(object):
    """Generate rainbow."""

    def __init__(self, led):
        self._led = led
        self._step = 0

    def step(self, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex
        size = end - start + 1

        for i in range(size):
            color = (i + self._step) % 384
            self._led.set(start + i, wheel_color(color))

        self._step += 1
        if self._step > 384:
            self._step = 0

        self._led.update()


class RainbowCycle(object):
    """Generate rainbow wheel equally distributed over strip."""

    def __init__(self, led):
        self._led = led
        self._step = 0

    def step(self, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex
        size = end - start + 1

        for i in range(size):
            color = (i * (384 / size) + self._step) % 384
            self._led.set(start + i, wheel_color(color))

        self._step += 1
        if self._step > 384:
            self._step = 0

        self._led.update()


class ColorWipe(object):
    """Fill the dots progressively along the strip."""

    def __init__(self, led):
        self._led = led
        self._step = 0

    def step(self, color, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex

        if self._step == 0:
            self._led.fillOff()

        self._led.set(start + self._step, color)

        self._step += 1
        if start + self._step > end:
            self._step = 0

        self._led.update()


class ColorChase(object):
    """Chase one pixel down the strip."""

    def __init__(self, led):
        self._led = led
        self._step = 0

    def step(self, color, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex

        if self._step == 0:
            self._led.setOff(end)
        else:
            self._led.setOff(start + self._step - 1)

        self._led.set(start + self._step, color)

        self._step += 1
        if start + self._step > end:
            self._step = 0

        self._led.update()


class LarsonScanner(object):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.)."""

    def __init__(self, led):
        self._led = led
        self._step = 0
        self._direction = -1
        self._last = 0

    def step(self, color, tail=2, fade=0.75, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex
        size = end - start + 1

        tail += 1  # makes tail math later easier
        if tail >= size / 2:
            tail = (size / 2) - 1

        self._last = start + self._step
        self._led.set(self._last, color)

        tl = tail
        if self._last + tl > end:
            tl = end - self._last
        tr = tail
        if self._last - tr < start:
            tr = self._last - start

        for l in range(1, tl + 1):
            level = (float(tail - l) / float(tail)) * fade
            self._led.setRGB(self._last + l,
                             color.r * level,
                             color.g * level,
                             color.b * level)

        if self._last + tl + 1 <= end:
            self._led.setOff(self._last + tl + 1)

        for r in range(1, tr + 1):
            level = (float(tail - r) / float(tail)) * fade
            self._led.setRGB(self._last - r,
                             color.r * level,
                             color.g * level,
                             color.b * level)

        if self._last - tr - 1 >= start:
            self._led.setOff(self._last - tr - 1)

        if start + self._step == end:
            self._direction = -self._direction
        elif self._step == 0:
            self._direction = -self._direction

        self._step += self._direction

        self._led.update()


class LarsonRainbow(LarsonScanner):
    """Larson scanner (i.e. Cylon Eye or K.I.T.T.) but Rainbow."""

    def step(self, tail=2, fade=0.75, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex
        size = end - start + 1

        hue = (self._step * (360 / size))

        super(LarsonRainbow, self).step(
            ColorHSV(hue).get_color_rgb(), tail, fade, start, end)

        self._led.update()


class Wave(object):
    """Sine wave animation."""

    def __init__(self, led):
        self._led = led
        self._step = 0

    def step(self, color, cycles, start=0, end=0):
        if end == 0 or end > self._led.lastIndex:
            end = self._led.lastIndex
        size = end - start + 1

        for i in range(size):
            y = math.sin(
                math.pi * float(cycles) * float(self._step * i) / float(size))
            if y >= 0.0:
                # Peaks of sine wave are white
                y = 1.0 - y  # Translate Y to 0.0 (top) to 1.0 (center)
                c2 = Color(255 - float(255 - color.r) * y,
                           255 - float(255 - color.g) * y,
                           255 - float(255 - color.b) * y)
            else:
                # Troughs of sine wave are black
                y += 1.0  # Translate Y to 0.0 (bottom) to 1.0 (center)
                c2 = Color(float(color.r) * y,
                           float(color.g) * y,
                           float(color.b) * y)
            self._led.set(start + i, c2)

        self._step += 1
        self._led.update()
