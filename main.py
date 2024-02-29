"""
MODES:
[31] No code on robot:
RoboRIO inactive/not receiving serial data from RoboRIO

[32] Disabled without auto
RoboRIO is disabled, and has no autonomous program set

[33] Disabled with auto
RoboRIO is disabled, abd dose have autonomous program set


--< Modes for when RoboRIO is enabled >--
Priority: 1 > 2 > 3 > 4

[1] Signal:
For communication with teammates to activate amplifier

[2] Ready to shoot:
The robot shooter and arm is in position, ready to shoot note

[3] Has note:
The robot currently is holding a note

[4] Vision:
The robot spots a note (tells the driver that they can press a button for
robot to retrieve a note)
"""


import supervisor
import board
from lightstrip import LightStrip
import patterns
import time
import sys

# Serial data variables
serial = sys.stdin
tolerance = 2
tolerance_count = 0
current_mode = "31"
last_mode = "31"

# Create light objects
strip1 = LightStrip(0, board.D5, 20)
lightstrips: tuple[LightStrip] = (strip1,)


# Retrieves and returns serial data sent by Java side
def get_serial_data() -> str:
    # Return serial data if any
    if supervisor.serial_bytes_available > 0:
        data = serial.readline()
        if data != None:
            tolerance_count = 0
            return data.strip()
    
    # Check tolerance and return previous, if tolerance count reached, "31"
    global tolerance_count
    if tolerance_count >= tolerance:
        tolerance_count = 0
        return "31"
    tolerance_count += 1
    return last_mode


# Assign colors and patterns to light strips
def assign_mode(light: LightStrip):
    if current_mode == last_mode:
        return
    
    light.pattern_starting_loop = patterns.loopcount

    # Update color and pattern on light to display
    if current_mode == "1":
        light.pattern = patterns.rainbow

    elif current_mode == "2":
        # Ready to shoot, railgun pattern (requested by drivers)
        light.primary = (0, 0, 255)
        light.pattern = patterns.railgun

    elif current_mode == "3":
        pass
    elif current_mode == "4":
        pass
    elif current_mode == "32":
        pass
    elif current_mode == "33":
        pass
    else:
        # If serial data received does not match any of our mode
        # Or is 31 (no code)
        pass


def main_loop():
    # Increment loopcount
    patterns.loopcount += 1

    # Read serial data sent by RoboRIO
    global current_mode
    global last_mode
    current_mode = get_serial_data()

    # Match lights with serial data and update lights
    for lightstrip in lightstrips:
        assign_mode(lightstrip)
        lightstrip.pattern(lightstrip)

    last_mode = current_mode


# Main Loop
if __name__ == "__main__":
    while True:
        main_loop()
        time.sleep(patterns.frames_per_second / 1)