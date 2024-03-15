"""
MODES:
These are defined in the Java code `LightsStateMessage` here:
https://github.com/Team488/XBot2024/blob/main/src/main/java/competition/subsystems/lights/LightSubsystem.java
[15] No code on robot:
RoboRIO inactive/not receiving serial data from RoboRIO

[7] Disabled without auto
RoboRIO is disabled, and has NO autonomous program set

[6] Disabled with auto
RoboRIO is disabled, and DOES have autonomous program set


--< Modes for when RoboRIO is enabled >--
Priority: 1 > 2 > 3 > 4 > 5

[5] Enabled
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

import digitalio

# Serial data variables
serial = sys.stdin
tolerance = 2
tolerance_count = 0
current_mode = modes["ROBOT_NOCODE"]
last_mode = modes["ROBOT_NOCODE"]

# Digital input pins for ready binary data from RoboRIO
dio_pins = (board.D10, board.D11, board.D12, board.D13)
dios = [digitalio.DigitalInOut(pin) for pin in dio_pins]

watch_dog_dio = digitalio.DigitalInOut(board.D9)
watch_dog_dio.direction = digitalio.Direction.OUTPUT

# Create light objects
lightStrip = LightStrip(board.D5, 16)
#lightstrips: LightStrip = (strip1,)

# Retrieves and returns serial data sent by Java side
def get_serial_data() -> str:
    global tolerance_count

    # Return serial data if any
    if supervisor.runtime.serial_bytes_available:
        data = serial.readline()
        if data:
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

def get_binary_data() -> int:
    result = 0
    for i, dio in enumerate(dios):
        result |= dio.value << i
    return result

loop_count = 0
def feed_watch_dog():
    global loop_count
    if loop_count % 20 == 0:
        watch_dog_dio.value = not watch_dog_dio.value
    loop_count+=1

def main_loop():
    global current_mode
    global last_mode

    feed_watch_dog()

    # Increment loopcount
    patterns.loopcount += 1

    # Read data sent by RoboRIO
    current_mode = str(get_binary_data())

    # Match lights with serial data and update lights
    #for lightstrip in lightstrips:
    lightStrip.assign_mode(current_mode, last_mode)
    lightStrip.pattern_function(lightStrip)

    last_mode = current_mode


def main():
    while True:
        main_loop()
        time.sleep(1 / patterns.frames_per_second)