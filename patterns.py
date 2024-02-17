""" Responsible for changing the lights pixels, contains different patterns """

from digitalio import DigitalInOut, Direction, Pull
import board
import neopixel
from rainbowio import colorwheel
import time
import math
from robotstates import check_robot_changed, get_fps


# NeoPixel
PIXEL_PIN = board.D5
NUM_PIXELS = 20
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)

r, g, b = 0, 0, 0
r2, g2, b2 = 0, 0, 0
loop = 0


Colors = {
    "RED": (255, 0, 0),
    "ORANGE": (255, 100, 100),
    "GRAY": (100, 100, 100),
    "GREEN": (0,255,0),
    "BLUE":(0,0,255)
}


def set_primary_color(color: str):
    global r, g, b
    if color in Colors:
        (r, g, b) = Colors[color]
    else:
        print("color not in Colors")
    return

def set_secondary_color(color: str):
    global r2, g2, b2
    if color in Colors:
        (r2, g2, b2) = Colors[color]
    else:
        print("color not in Colors")
    return




""" PATTERNS """
def flash():
    fps = get_fps()
    # Dark -> Bright
    for frame in range(0, fps+1, 1):
        for pixel in range(NUM_PIXELS):
            pixels[pixel] = (r*frame/fps, g*frame/fps, b*frame/fps)
        pixels.show()
        check_robot_changed()
    # Bright -> Dark
    for frame in range(fps, 0, -1):
        for pixel in range(NUM_PIXELS):
            pixels[pixel] = (r*frame/fps, g*frame/fps, b*frame/fps)
        pixels.show()
        check_robot_changed()
    return

        
def static():
    for pixel in range(NUM_PIXELS):
        pixels[pixel] = (r, g, b)
    pixels.show()
    time.sleep(1/get_fps())
    return

#MOVING RAINBOW IS VERY BRIGHT

def moving_rainbow():
    global loop
    loop += 1
    for pixel in range(NUM_PIXELS):
        pixels[pixel] = colorwheel((255/20*(r+loop))%255)  
    pixels.show()
    check_robot_changed()
    return

# TESTING
# def alternating():
#     global loop
#     loop += 1
#     for pixel in range(NUM_PIXELS):
#         if loop % 2 == 0:
#             pixels[pixel] = colorwheel(r, g, b)

def wavy():
    # Initialize speed
    loop = 0
    # Loop for movement of the lights
    while True:
        # Update time for animation
        loop += 1

        # Calculate brightness for each pixel
        for pixel in range(NUM_PIXELS):
            multiplier = math.sin(pixel + loop)
            multiplier = max(0, multiplier)
            pixels[pixel] = (r*multiplier, g*multiplier, b*multiplier)

        pixels.show()  # Update the NeoPixels with the new colors
        time.sleep(0.05)
        check_robot_changed()  

    return
    
    
# def alternating(color 1, color 2, interval):
#     while True:
#         strip.fill (color1)
#         strip.show()
#         time.sleep(interval)
#         strip.fill(color2)
#         strip.show()
#         time.sleep(interval)
#     pixels.show()
#     return+
            
            