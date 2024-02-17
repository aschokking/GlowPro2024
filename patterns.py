from rainbowio import colorwheel
from robot_states import frames
from light import Light
from math import sin

loopcount = 0


def static(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = light.primary
    light.neopixel.show()


def flashing(light: Light):
    multiplier = sin(loopcount) + 1
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = tuple(x * (multiplier/2) for x in light.primary)
    light.neopixel.show()
        

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


def railgun(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        if loopcount - light.pattern_starting_loop == pixel + light.PIXEL_COUNT or loopcount - light.pattern_starting_loop == pixel + light.PIXEL_COUNT + 1:
            light.neopixel[pixel] = light.secondary
        elif loopcount - light.pattern_starting_loop > pixel:
            light.neopixel[pixel] = light.primary
        else:
            light.neopixel[pixel] = (0, 0, 0)
    light.neopixel.show()