"""
MODES:
[31] No code on robot:
RoboRIO inactive/not receiving serial data from RoboRIO

[32] Disabled without auto
RoboRIO is disabled, and has NO autonomous program set

[33] Disabled with auto
RoboRIO is disabled, and DOES have autonomous program set


--< Modes for when RoboRIO is enabled >--
Priority: 1 > 2 > 3 > 4 > 34

[34] Enabled
RoboRIO is enabled, but none of the above are active.

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
strip1 = LightStrip(board.D5, 8)
lightstrips: tuple[LightStrip] = (strip1,)


# Retrieves and returns serial data sent by Java side
def get_serial_data() -> str:
    global tolerance_count

    # Return serial data if any
    if supervisor.serial_bytes_available:
        data = serial.readline()
        if data != None:
            tolerance_count = 0
            return data.strip()
    
    # Check tolerance and return previous, if tolerance count reached, "31"
    # Tolerance is for if there are no serial data sent from the Java side
    # *There may be some delay if both sides are sending at same or similar rate*
    # Tolerance count is 2, therefore it will tolerate two frames/fps seconds
    if tolerance_count >= tolerance:
        tolerance_count = 0
        return "31"
    tolerance_count += 1
    return last_mode


# MODES
modes = {
    "AMP_SIGNAL": "1",
    "READY_TO_SHOOT": "2",
    "ROBOT_CONTAINS_NOTE": "3",
    "VISION_SEES_NOTE": "4",
    "DISABLED_WITHOUT_AUTO": "32",
    "DISABLED_WITH_AUTO": "33",
    "PURELY_ENABLED": "34" # None of modes 1-4 are active
}


# Assign colors and patterns to light strips
def assign_mode(light: LightStrip):
    # No need to reassign if mode is same as previous loop
    if current_mode == last_mode:
        return
    
    light.pattern_starting_loop = patterns.loopcount

    # Update color and pattern on light to display
    if current_mode == modes["AMP_SIGNAL"]:
        light.pattern = patterns.rainbow

    elif current_mode == modes["READY_TO_SHOOT"]:
        # Ready to shoot, railgun pattern (requested by drivers)
        light.primary = (0, 255, 0)
        light.pattern = patterns.railgun

    elif current_mode == modes["ROBOT_CONTAINS_NOTE"]:
        light.primary = (255, 165, 0)
        light.pattern = patterns.static

    elif current_mode == modes["VISION_SEES_NOTE"]:
        light.primary = (173, 216, 230)
        light.secondary = (255, 255, 255)
        light.pattern = patterns.alternating

    elif current_mode == modes["DISABLED_WITHOUT_AUTO"]:
        # TO-DO
        pass

    elif current_mode == modes["DISABLED_WITH_AUTO"]:
        # TO-DO
        pass

    elif current_mode == modes["PURELY_ENABLED"]:
        light.primary = (255, 255, 255)
        light.pattern = patterns.static
    else:
        light.primary = (255, 0, 0)
        light.pattern = patterns.static


def main_loop():
    global current_mode
    global last_mode

    # Increment loopcount
    patterns.loopcount += 1

    # Read serial data sent by RoboRIO
    current_mode = get_serial_data()

    # Match lights with serial data and update lights
    for lightstrip in lightstrips:
        assign_mode(lightstrip)
        lightstrip.pattern(lightstrip)

    last_mode = current_mode


def main():
    while True:
        main_loop()
        time.sleep(1 / patterns.frames_per_second)