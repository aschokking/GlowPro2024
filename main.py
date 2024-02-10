
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
from enum import Enum as enum
import time
from digitalio import DigitalInOut, Direction, Pull
import board
import neopixel
from rainbowio import colorwheel


# Stuff from 2023, might need to be updated
PIXEL_PIN = board.D5
NUM_PIXELS = 20
pixels = neopixel.NeoPixel(PIXEL_PIN, NUM_PIXELS, brightness=1, auto_write=False)

class StateChangedException(Exception):
    pass


class RobotMode(enum):
    NoCode = 1
    DisabledNoAuto = 2
    DisabledWithAuto = 3
    Enabled = 4
    
class RobotStateEnum(enum):
    # Static
    NotHoldingNote = 1
    HoldingNote = 2

    # Action
    Shooting = 3
    Intaking = 4

    # Communication
    SignalingAmp = 5

    # Other
    InHorribleState = 6


class LightDisplayState(enum):
    Static = 1
    Flashing = 2
    Rainbow = 3


class Colors(enum):
    Red = 1
    Orange = 2
    Green = 3
    Blue = 4
    White = 5
    Yellow = 6
    Gray = 7
    Black = 8

    
light_state = LightDisplayState.Static
robot_state = RobotStateEnum.NotHoldingNote
robot_mode = RobotMode.NoCode
r, g, b = 0, 0, 0
steps = 30
waittime = 0.04


"""
Sets color of all pixels, used primarily with static lights
"""
def set_color(color: Colors):
    global r, g, b

    match color:
        case Colors.Red:
            r, g, b = 255, 0, 0
        case Colors.Green:
            r, g, b = 0, 255, 0
        case Colors.Blue:
            r, g, b = 0, 0, 255
        case Colors.White:
            r, g, b = 255, 255, 255
        case Colors.Yellow:
            r, g, b = 255, 255, 0
        case Colors.Gray:
            r, g, b = 96, 96, 96
        case Colors.Black: 
            r, g, b = 0, 0, 0


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


# Runs when robot is enabled
def enabled():
    match light_state:
        case LightDisplayState.Static:
            static()

        case LightDisplayState.Flashing:
            flash()
        
        case _:
            print("Light state not matched")
 

def wait_and_check(waittime: float):
    # Robot updates every "waittime", so our frames per second is 1/waittime, waittime = 0.04 means 25 fps
    if robot_state == get_robot_state() and robot_mode == get_robot_mode():
        time.sleep(waittime)
    else:
        raise StateChangedException("Robot state or mode changed")
            

def get_robot_state():
    return RobotStateEnum.NotHoldingNote


def get_robot_mode():
    return RobotMode.Enabled


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
        match robot_mode:
            case RobotMode.NoCode:
                # Runs when there is no code on the RoboRIO, STATIC BLACK
                set_color(Colors.Black)
                static()

            case RobotMode.DisabledNoAuto:
                # Runs when there is code on RoboRIO, not enabled, no auto set, STATIC GRAY
                set_color(Colors.Gray)
                static()

            case RobotMode.DisabledWithAuto:
                # Runs when there is code on RoboRIO, not enabled, has auto set, FLASHING GRAY
                set_color(Colors.Gray)
                flash()

            case RobotMode.Enabled:
                # Runs when there is code on RoboRIO, enabled, actions of lights

                # Update lights color and state
                match robot_state:
                    case RobotStateEnum.NotHoldingNote:
                        set_color(Colors.Blue)
                        light_state = LightDisplayState.Static

                    case RobotStateEnum.HoldingNote:
                        set_color(Colors.Green)
                        light_state = LightDisplayState.Static

                    case RobotStateEnum.Shooting:
                        light_state = LightDisplayState.Flashing
                        pass
                    
                    case RobotStateEnum.Intaking:
                        pass

                    case RobotStateEnum.SignalingAmp:
                        pass

                    case RobotStateEnum.InHorribleState:
                        set_color(Colors.Red)
                        pass

                    case _:
                        print("Robot state not matched, Reasons: Not enabled; state passed in we do not contain.")

                enabled()

            case _:
                print("Robot mode not matched")

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
