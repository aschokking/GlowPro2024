from digitalio import DigitalInOut, Direction, Pull
import board
from light import Light
import patterns
from robot_states import recorded_mode, get_mode, get_states, frame_time_per_interval
import time

Colors = {
    "RED": (255, 0, 0),
    "ORANGE": (255, 100, 100),
    "GRAY": (100, 100, 100),
    "GREEN": (0,255,0),
    "BLUE":(0,0,255)}

robot_state: list[int]
mainloop_count = 0


def match_state_with_pattern(light: Light):
    if light.state == 1:
        light.primary = Colors["BLUE"]
        light.pattern = patterns.static

    elif light.state == 2:
        light.primary = Colors["GREEN"]
        light.pattern = patterns.static

    elif light.state == 3:
        light.primary = Colors["GRAY"]
        light.pattern = patterns.static

    elif light.state == 4:
        light.primary = Colors["RED"]
        light.pattern = patterns.flashing

    elif light.state == 5:
        light.primary = Colors["ORANGE"]
        light.pattern = patterns.static


def main_loop(lights: list[Light]):
    # Assuming we are getting a state
    # Also, "action" or "rainbow" states should have higher priority than static
    global robot_state
    global recorded_mode
    patterns.loopcount += 1
    robot_state = get_states() # Placed here because we always want to update our states
    recorded_mode = get_mode()

    if recorded_mode == 1:
        pass

    elif recorded_mode == 2:
        pass

    elif recorded_mode == 3:
        pass

    elif recorded_mode == 4:
        for light in lights:
            light.state = robot_state[light.channel]
            match_state_with_pattern(light)

    for light in lights:
        if light.pattern != None:
            light.pattern(light)
    time.sleep(frame_time_per_interval)


def initialize():
    light1 = Light(0, board.D5, 20)
    lights = [light1]
    return lights


# Main Loop
if __name__ == "__main__":
    lights = initialize()
    while True:
        main_loop(lights)