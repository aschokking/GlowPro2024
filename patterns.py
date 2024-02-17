from rainbowio import colorwheel
from light import Light
from math import sin

frames = 25
frame_interval = 1
frame_time_per_interval = frame_interval / frames
loopcount = 0


def static(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = light.primary
    light.neopixel.show()


def flashing(light: Light):
    multiplier = sin(loopcount / 5) + 1
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = tuple(x * (multiplier/2) for x in light.primary)
    light.neopixel.show()
        

# ALTERNATING DOESN'T LOOK GOOD
def alternating(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        if (pixel + loopcount) % 2 == 0:
            light.neopixel[pixel] = light.primary
        else:
            light.neopixel[pixel] = light.secondary
    light.neopixel.show()
    

def wavy(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        multiplier = max(0, min(sin(pixel + loopcount), 1))
        light.neopixel[pixel] = tuple(x * multiplier for x in light.primary)
    light.neopixel.show()
    

def rainbow(light: Light):    
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = colorwheel(((255 / frames) * loopcount) % 255)
    light.neopixel.show()