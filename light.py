import neopixel

class Light:

    def __init__(self, pixel_pin, pixel_count) -> None:
        self.neopixel = neopixel.NeoPixel(pixel_pin, pixel_count, brightness=1, auto_write=False)
        self.primary = (0, 0, 0)
        self.secondary = (0, 0, 0)
        self.state = 0
        self.key = 0
        self.PIXEL_COUNT = pixel_count