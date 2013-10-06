import colorsys


class Color:
    """Main color object used by all methods."""

    def __init__(self, r=0.0, g=0.0, b=0.0, bright=1.0):
        """Initialize Color object with optional RGB and brightness values."""

        if r > 255.0 or r < 0.0 or g > 255.0 or g < 0.0 or b > 255.0 or b < 0.0:
            raise ValueError('RGB values must be between 0 and 255')
        if bright > 1.0 or bright < 0.0:
            raise ValueError('Brightness must be between 0.0 and 1.0')

        self.r = r * bright
        self.g = g * bright
        self.b = b * bright

    def get_color_hsv(self):
        h, s, v = colorsys.rgb_to_hsv(self.r / 255.0, self.g / 255.0, self.b / 255.0)
        return ColorHSV(h * 360, s, v)

    def __str__(self):
        return "%d,%d,%d" % (self.r, self.g, self.b)


class ColorHSV:
    """Useful for natural color transitions.

    Increment hue to sweep through the colors.  Must call getColorRGB()
    before passing to any of the methods.
    """

    def __init__(self, h=360.0, s=1.0, v=1.0):
        if h > 360.0 or h < 0.0:
            raise ValueError('Hue value must be between 0.0 and 360.0')
        if s > 1.0 or s < 0.0:
            raise ValueError('Saturation must be between 0.0 and 1.0')
        if v > 1.0 or v < 0.0:
            raise ValueError('Value must be between 0.0 and 1.0')

        self.h = h
        self.s = s
        self.v = v

    def get_color_rgb(self):
        r, g, b = colorsys.hsv_to_rgb(self.h / 360.0, self.s, self.v)
        return Color(r * 255.0, g * 255.0, b * 255.0)

    def __str__(self):
        return "%0.2f,%0.2f,%0.2f" % (self.h, self.s, self.v)


def wheel_color(position):
    """Get color from wheel value (0 - 384)."""
    if position < 0:
        position = 0
    if position > 384:
        position = 384

    if position < 128:
        r = 127 - position % 128
        g = position % 128
        b = 0
    elif position < 256:
        g = 127 - position % 128
        b = position % 128
        r = 0
    else:
        b = 127 - position % 128
        r = position % 128
        g = 0

    return Color(r, g, b)
