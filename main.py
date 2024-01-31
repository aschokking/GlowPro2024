import time

from digitalio import DigitalInOut, Direction, Pull
import board
import neopixel
from rainbowio import colorwheel

PIXEL_PIN = board.D5
NUM_PIXELS = 20

pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)

steps=30
wait=0.04

movingRainbow = 0


'''
#############################################
######  color display functions
#############################################
'''
def enabled(current_mode):
    for countdown in range(steps, 1, -1):
        if read_current_mode() != current_mode:
            return
        for i in range(NUM_PIXELS):
            pixels[i]=(0, 255*countdown/steps, 0)
        pixels.show()
        wait_and_check(wait)

    for countup in range(1, steps, 1):
        if read_current_mode() != current_mode:
            return
        for i in range(NUM_PIXELS):
            pixels[i]=(0, 255*countup/steps, 0)
        pixels.show()
        wait_and_check(wait)

def no_code():
    for noCode in range(NUM_PIXELS):
        pixels[noCode]=(80, 80, 80)
    pixels.show()
    wait_and_check(0.3)
    for noCode in range(NUM_PIXELS):
        pixels[noCode]=(0, 0, 0)
    pixels.show()
    wait_and_check(0.3)

def disabled():
    for countdown in range(steps, 1, -1):
        for i in range(NUM_PIXELS):
            pixels[i]=(255*countdown/steps, 0, 0)
        pixels.show()
        wait_and_check(wait)

    for countup in range(1, steps, 1):
        for i in range(NUM_PIXELS):
            pixels[i]=(255*countup/steps, 0, 0)
        pixels.show()
        wait_and_check(wait)

def disabled_with_auto():
    for i in range(NUM_PIXELS):
        pixels[i]=(20, 50, 20)
    for countdown in range(steps, 1, -1):
        pixels.brightness = countdown/steps
        pixels.show()
        wait_and_check(wait)

    for countup in range(1, steps, 1):
        pixels.brightness = countup/steps
        pixels.show()
        wait_and_check(wait)

def moving_rainbow():    
    global movingRainbow
    current_mode = read_current_mode()
    for r in range(NUM_PIXELS):
        if read_current_mode() != current_mode:
            return
        pixels[r]=colorwheel((255/20*(r+movingRainbow))%255)  
        pixels.show()
    movingRainbow = movingRainbow+1

'''
#############################################
######  get current input from robot
#############################################
'''

def read_current_mode():
    # TODO: read from serial or input pins
    # for now just statically returning disabled
    return 31


class ModeChangedException(Exception):
    pass

def wait_and_check(durationS):
    if mode == read_current_mode():
        time.sleep(durationS)
    else:
        raise ModeChangedException("Mode changed")

#############################################
######  main loop
#############################################

def main():
    global mode
    # Read mode and alliance from pins
    mode = read_current_mode()

    try:    
        #Select display option
        if mode == 31:
            no_code()
        elif mode == 1:
            disabled()
        elif mode == 2:
            enabled(mode)
        elif mode == 3:
            moving_rainbow(False)
        elif mode == 4:
            disabled_with_auto()
        elif mode == 5: #arm in position
            moving_rainbow(True)
        else:
            no_code()
    except ModeChangedException:
        # Mode changed, restart loop
        pass

if __name__ == "__main__":
    while True:
        main()
