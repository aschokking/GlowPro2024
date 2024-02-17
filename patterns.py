from rainbowio import colorwheel
from robot_states import frames, check_robot
from light import Light
from math import sin

loopcount = 0


def static(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = light.primary
    light.neopixel.show()
    if not check_robot(light):
        return


def flashing(light: Light):
    # Dark -> Bright
    for frame in range(frames):
        for pixel in range(light.PIXEL_COUNT):
            light.neopixel[pixel] = tuple(x * frame / (frames-1) for x in light.primary)
        light.neopixel.show()
        if not check_robot(light):
            return

    # Bright -> Dark
    for frame in range(frames, 0, -1):
        for pixel in range(light.PIXEL_COUNT):
            light.neopixel[pixel] = tuple(x * (frame-1) / (frames-1) for x in light.primary)
        light.neopixel.show()
        if not check_robot(light):
            return
        

def alternating(light: Light):
    global loopcount
    loopcount += 1
    for pixel in range(light.PIXEL_COUNT):
        if (pixel + loopcount) % 2 == 0:
            light.neopixel[pixel] = light.primary
        else:
            light.neopixel[pixel] = light.secondary
    light.neopixel.show()
    if not check_robot(light):
        return
    

def wavy(light: Light):
    for pixel in range(light.PIXEL_COUNT):
        multiplier = max(0, min(sin(pixel), 1))
        light.neopixel[pixel] = tuple(x * multiplier for x in light.primary)
    light.neopixel.show()
    if not check_robot(light):
        return
    

def rainbow(light: Light):    
    global loopcount
    loopcount += 1
    for pixel in range(light.PIXEL_COUNT):
        light.neopixel[pixel] = colorwheel(((255 / frames) * loopcount) % 255)
    light.neopixel.show()
    if not check_robot(light):
        return