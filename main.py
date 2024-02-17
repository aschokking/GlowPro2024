# NUM_PIXELS = 20

# pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)

# steps = 30
# wait = 0.04

# movingRainbow = 0


# def moving_rainbow():    
#     global movingRainbow
#     current_mode = read_current_mode()
#     for r in range(NUM_PIXELS):
#         if read_current_mode() != current_mode:
#             return
#         pixels[r]=t((255/20*(r+movingRainbow))%255)  
#         pixels.show()
#     movingRainbow = movingRainbow+1

############################################################################################
from digitalio import DigitalInOut, Direction, Pull
import board
import neopixel
from rainbowio import colorwheel
from light import Light
import patterns
from robot_states import recorded_mode, get_mode, get_states, ModeChangedException, frame_time_per_interval
import threading
import time


# Stuff from 2023, might need to be updated

Colors = {
    "RED": (255, 0, 0),
    "ORANGE": (255, 100, 100),
    "GRAY": (100, 100, 100),
    "GREEN": (0,255,0),
    "BLUE":(0,0,255)}

robot_state: list[int]
mainloop_count = 0

"""
Sets color of all pixels, used primarily with static lights
"""


def light_main_loop(light: Light, loopcount: int):
    while mainloop_count == loopcount:
        if robot_state[light.key] == 1:
            light.primary = Colors["BLUE"]
            patterns.static(light)

        elif robot_state[light.key] == 2:
            light.primary = Colors["GREEN"]
            patterns.static(light)

        elif robot_state[light.key] == 3:
            light.primary = Colors["GRAY"]
            patterns.static(light)

        elif robot_state[light.key] == 4:
            light.primary = Colors["RED"]
            patterns.flashing(light)

        elif robot_state[light.key] == 5:
            light.primary = Colors["ORANGE"]
            patterns.static(light)


def main_loop(lights: list[Light]):
    # Assuming we are getting a state
    # Also, "action" or "rainbow" states should have higher priority than static
    global robot_state
    global recorded_mode
    global mainloop_count
    robot_state = get_states() # Placed here because we always want to update our states

    if recorded_mode == get_mode():
        time.sleep(frame_time_per_interval)
        return

    mainloop_count += 1
    recorded_mode = get_mode()

    if recorded_mode == 1:
        pass

    elif recorded_mode == 2:
        pass

    elif recorded_mode == 3:
        pass

    elif recorded_mode == 4:
        # Update light states in lights
        # While True, have the lights display their states
        for light in lights:
            light.state = robot_state[light.key]
            thread = threading.Thread(target=light_main_loop, args=(light, mainloop_count))
            thread.start()


def initialize():
    light1 = Light(board.D5, 20)
    lights = [light1]
    for key, light in enumerate(lights):
        light.key = key

    return lights

# Main Loop
if __name__ == "__main__":
    lights = initialize()
    while True:
        main_loop(lights)


# So apparently how this year (2024) lights will work is that we will get like a serial, a text constantly on
# probably what command is running and we can update our lights based off of it
# Keep everything above line 144 just for reference ;), that way we don't have to navigate through github

# Intaking - flashing orange (or any color)

# When holding note with arm - static green

# Shooter Rev - charge up based on desired rpm
    # Shooting - flash a quick white light

# Not holding note - Blue

# Signal amp button - rave

# In a horrible state - flashing red

# # ## # # # # LightDisplayState.Charging:
#         brightness += .5
#     if brightness >= 1
#         light_state == LightDisplayState.Charging:#below is a function for testing flashing
# def flashing_lights(color):
#     delay = 0.25 
#     flashes = 10
#     for _ in range(flashes):
#         set_color(color)
#         pixels.show()
#         time.sleep(delay)
#     pixels.show(False)


# #below is a function for testing shooter
# def shooting_lights(color):
#     global light_stateg
#     while True:
#         pass#below is a function for testing flashing
        
        

# def flashing_lights(color):
#     delay = 0.25 
#     flashes = 10
#     for _ in range(flashes):
#         set_color(color)
#         pixels.show()
#         time.sleep(delay)
#     pixels.show(False)
# def rainbow_rave()
