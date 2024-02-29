import neopixel
from patterns import static

class LightStrip:

    def __init__(self, pixel_pin, pixel_count) -> None:

        # Create a neopixel for each lightstrip
        self.neopixel = neopixel.NeoPixel(pixel_pin, pixel_count, brightness=1, auto_write=False)
        self.PIXEL_COUNT = pixel_count

        # Colors for different patterns
        self.primary: tuple[int, int, int] = (0, 0, 0)
        self.secondary = (0, 0, 0)

        # Pattern function to call on every update
        self.pattern = static

        # Which loopcount the pattern started on, used for patterns that require
        # Multiple loops to show its effect (railgun, rainbow)
        self.pattern_starting_loop = 0