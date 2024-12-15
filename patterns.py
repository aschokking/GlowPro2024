from rainbowio import colorwheel
from math import sin

frames_per_second = 12
loopcount = 0
alternating_loopcount = 0


# Constant color
def static(light: LightStrip):
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = light.primary
    light.neopixel.show()


# Gradient flashing
def flashing(light: LightStrip):
    multiplier = sin(loopcount / 5) + 1
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = tuple(x * (multiplier/2) for x in light.primary)
    light.neopixel.show()
        

# Alternates between two color of lights, Ex.
# Loop 1: All green
# Loop 2: All red
def alternating(light: LightStrip):
    global alternating_loopcount
    for pixel in range(light.PIXEL_COUNT):
        # Alternate appproximately 2 times a second
        if loopcount % (frames_per_second // 2) != light.pattern_starting_loop % (frames_per_second // 2):
            continue

        alternating_loopcount += 1
        if alternating_loopcount % 2 == 0:
            light.neopixel[pixel] = light.primary
        else:
            light.neopixel[pixel] = light.secondary
    light.neopixel.show()
    

# Think of this pattern as if you are static and cars in front of you
# Are constantly driving by (one direction)
def wavy(light: LightStrip):
    for pixel in range(light.PIXEL_COUNT):
        multiplier = max(0, min(sin(pixel + loopcount), 1))
        light.neopixel[pixel] = tuple(x * multiplier for x in light.primary)
    light.neopixel.show()
    

# Disco party baby!
def rainbow(light: LightStrip):    
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = colorwheel(((255 / frames_per_second) * loopcount) % 255)
    light.neopixel.show()

# Alternates between two color of lights, Ex.
# Loop 1: All green
# Loop 2: All red
def alternating(light):
    global alternating_loopcount
    for pixel in range(light.PIXEL_COUNT):
        # Alternate appproximately 2 times a second
        if loopcount % (frames_per_second // 2) != light.pattern_starting_loop % (frames_per_second // 2):
            continue

        alternating_loopcount += 1
        if alternating_loopcount % 2 == 0:
            light.neopixel[pixel] = light.primary
        else:
            light.neopixel[pixel] = light.secondary
    light.neopixel.show()

# Charge up
def railgun(light: LightStrip):
    for pixel in range(light.PIXEL_COUNT):
        if loopcount - light.pattern_starting_loop > pixel:
            light.neopixel[pixel] = light.primary
        else:
            light.neopixel[pixel] = (0, 0, 0)
    light.neopixel.show()