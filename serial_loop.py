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
from lightstrip import LightStrip, modes
import patterns
import time
import sys

# Serial data variables
serial = sys.stdin
tolerance = 2
tolerance_count = 0
current_mode = modes["ROBOT_NOCODE"]
last_mode = modes["ROBOT_NOCODE"]

# Create light objects
strip1 = LightStrip(board.D5, 8)
lightstrips: tuple[LightStrip] = (strip1,)


# Retrieves and returns serial data sent by Java side
def get_serial_data() -> str:
    global tolerance_count

    # Return serial data if any
    if supervisor.runtime.serial_bytes_available:
        data = serial.readline()
        if data:
            print(data)
            tolerance_count = 0
            return data.strip()
    
    # Check tolerance and return previous, if tolerance count reached, "31"
    # Tolerance is for if there are no serial data sent from the Java side
    # *There may be some delay if both sides are sending at same or similar rate*
    # Tolerance count is 2, therefore it will tolerate two frames/fps seconds
    if tolerance_count >= tolerance:
        tolerance_count = 0
        return modes["ROBOT_NOCODE"]
    tolerance_count += 1
    return last_mode


def main_loop():
    global current_mode
    global last_mode

    # Increment loopcount
    patterns.loopcount += 1

    # Read serial data sent by RoboRIO
    # current_mode = str(get_serial_data())
    # test_arr = ["1", "2", "3", "4", "31", "32", "33", "34"]

    # # Match lights with serial data and update lights
    # # for lightstrip in lightstrips:
    # for i in range(len(test_arr)):
    #     print(test_arr[i])
    #     time.sleep(5)
    strip1.assign_mode(current_mode, last_mode)
    strip1.pattern_function(strip1)
    #     if i == len(test_arr) - 1:
    #         i = 0

    last_mode = current_mode


def main():
    while True:
        main_loop()
        time.sleep(1 / patterns.frames_per_second)