
# PIXEL_PIN = board.D5
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
import sys
print(sys.version)
import time
from digitalio import DigitalInOut, Direction, Pull
import board
import neopixel
from rainbowio import colorwheel


# Stuff from 2023, might need to be updated
# connect the pin to D5
PIXEL_PIN = board.D5
NUM_PIXELS = 20
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)

class StateChangedException(Exception):
    pass


RobotModes = {
    "NOCODE": 1,
    "DISABLEDNOAUTO": 2,
    "DISABLEDWITHAUTO": 3,
    "ENABLED": 4
}

RobotStates = {
    "NOTHOLDINGSTATE": 1,
    "HOLDINGNOTE": 2,
    "SHOOTING" : 3,
    "INTAKING" : 4,
    "SIGNIALINGAMP" : 5,
    "INHORRIBLESTATE" : 6
    }
Colors = {"RED": (255, 0, 0), "ORANGE": (255, 100, 100), "GRAY": (100, 100, 100), "GREEN": (0,255,0), "BLUE":(0,0,255), "BLACK":(0,0,0)}

robot_state = RobotStates["NOTHOLDINGSTATE"]
robot_mode = RobotModes["NOCODE"]
r, g, b = 0, 0, 0
steps = 30
waittime = 0.04


"""
Sets color of all pixels, used primarily with static lights
"""
def set_color(color: str):
    global r, g, b

    if color in Colors:
        r, g, b = Colors[color]
    else:
        print("color not in Color")


def flash():
    # Dark -> Bright
    for step in range(0, steps+1, 1):
        for pixel in range(NUM_PIXELS):
            pixels[pixel] = (r*step/steps, g*step/steps, b*step/steps)
        pixels.show()
        wait_and_check(waittime)

    # Bright -> Dark
    for step in range(steps, 0, -1):
        for pixel in range(NUM_PIXELS):
            pixels[pixel] = (r*step/steps, g*step/steps, b*step/steps)
        pixels.show()
        wait_and_check(waittime)


def static():
    for pixel in range(NUM_PIXELS):
        pixels[pixel] = (r, g, b)
    pixels.show()
    time.sleep(waittime)
 

def wait_and_check(waittime: float):
    # Robot updates every "waittime", so our frames per second is 1/waittime, waittime = 0.04 means 25 fps
    if robot_state == get_robot_state() and robot_mode == get_robot_mode():
        time.sleep(waittime)
    else:
        raise StateChangedException("Robot state or mode changed")
            

def get_robot_state():
    return RobotStates["HOLDINGNOTE"]


def get_robot_mode():
    return RobotModes["ENABLED"]


# Main function
def main():
    # Assuming we are getting a state
    # Also, "action" or "rainbow" states should have higher priority than static
    global robot_state
    global robot_mode
    robot_state = get_robot_state()
    robot_mode = get_robot_mode()

    # Run the lights (actual displaying)
    try:
        if not robot_mode in RobotModes:
            print("Robot mode not matched")
            return
        
        if robot_mode == RobotModes["NOCODE"]:
            set_color(Colors["ORANGE"])
            static()

        elif robot_mode == RobotModes["DISABLEDNOAUTO"]:
            set_color(Colors["GRAY"])
            static()

        elif robot_mode == RobotModes["DISABLEDWITHAUTO"]:
            set_color(Colors["GRAY"])
            flash()

        else:
            # Else enabled
            if robot_state == RobotStates["NOTHOLDINGNOTE"]:
                set_color(Colors["BLUE"])
                static()
            elif robot_state == RobotStates["HOLDINGNOTE"]:
                set_color(Colors["GREEN"])
                static()
            elif robot_state == RobotStates["SHOOTING"]:
                pass
            elif robot_state == RobotStates["INTAKING"]:
                pass
            elif robot_state == RobotStates["SIGNALINGAMP"]:
                pass
            else:
                pass

    except StateChangedException:
        # Restarting loop as mode has been changed
        pass
    
        

# Main Loop
if __name__ == "__main__":
    while True:
        main()


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
