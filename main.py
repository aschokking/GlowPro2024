from digitalio import DigitalInOut, Direction, Pull
import busio
import board
import patterns
from robot_communication import recorded_mode, get_mode, get_states
import time
import neopixel

Colors = {
    "RED": (255, 0, 0),
    "ORANGE": (255, 100, 100),
    "GRAY": (100, 100, 100),
    "GREEN": (0,255,0),
    "BLUE":(0,0,255)}

robot_state: list[int]
mainloop_count = 0


#import usb_cdc
# import json
# # usb_cdc.enable(console=True, data=True)
# serial = usb_cdc.data

# print(serial)
# print(type(serial))

pix = neopixel.NeoPixel(board.D5, 20, brightness=1, auto_write=False)

# print("Wasssup dude")
# pix[0] = (200,50,50)
# pix.show()
# while True:
#     # read the secondary serial line by line when there's data
#     # note that this assumes that the host always sends a full line
    
#     if serial.in_waiting > 0:
#         data_in = serial.readline()

#         # try to convert the data to a dict (with JSON)
#         data = None
#         if data_in:
#             try:
#                 data = json.loads(data_in)
#             except ValueError:
#                 data = {"raw": data_in}

#         # by using a dictionary, you can add any entry and data into it
#         # to transmit any command you want and parse it here
#         if isinstance(data, dict):

#             # change the color of the neopixel
#             if "color" in data:
#                 print("Color received:", data["color"])
#                 if pix is not None:
#                     pix.fill(data["color"])

"""
Read the REPL to receive color data for the neopixel.
Not using the usb_cdc module.
"""

import json
import time
import supervisor
import sys

################################################################
# select the serial REPL port
################################################################

serial = sys.stdin

################################################################
# init board's LEDs for visual output
# replace with your own pins and stuff
################################################################

################################################################
# loop-y-loop
################################################################
# f = open("Logs.txt", "a")
loopcount = 0
while True:
    loopcount += 1
    # read the REPL serial line by line when there's data
    # note that this assumes that the host always sends a full line
    if supervisor.runtime.serial_bytes_available:
        data_in = serial.readline()
        # f.write(data_in)
        #print("Data in: "+data_in)
        #print(type(data_in))

        # Red if bytes available but can't get, yellow if == 36
        # Green if otherwise
        # if 1 then yellow
        if not data_in:
            for pixel in range(20):
                pix[pixel] = (255,0,0) # RED
            pix.show()
            time.sleep(0.5)
            continue

        temp = data_in.strip()

        if temp == "1":
            for pixel in range(20):
                pix[pixel] = (165, 42, 42) # Pink
            pix.show()
            time.sleep(0.5)
        elif temp == "2":
            for pixel in range(20):
                pix[pixel] = (42, 42, 165) # Random
            pix.show()
            time.sleep(0.5)
    
    else:
        # Blue if nothing to read
        if loopcount % 2 == 0:
            for pixel in range(20):
                pix[pixel] = (0,0,100) # BLUE
            pix.show()
        else:
            for pixel in range(20):
                pix[pixel] = (0,0,0) # Nothing
            pix.show()
        time.sleep(0.5)




# print(dir(board))
# uart = busio.UART(board.TX, board.RX, baudrate=9600)


# while True:
#     data = uart.readline(8)
#     if data != "None":
#         print(data)

# usb_cdc.enable(console=True, data=True)
# usb.enable(console=True, data=True)
# import supervisor

# l = LightStrip(0, board.D5, 20)
# while True:
#     if supervisor.runtime.serial_bytes_available:

#         for pixel in range(l.PIXEL_COUNT):
#                 l.neopixel[pixel] = (0,255*supervisor.runtime.serial_bytes_available/20,0)
#                 l.neopixel.show()
#         value = input()
#         # Sometimes Windows sends an extra (or missing) newline - ignore them
#         if value == "":
#             continue
#         else:
#             for pixel in range(l.PIXEL_COUNT):
#                 l.neopixel[pixel] = (0,0,255)
#                 l.neopixel.show()
#     else:
#         for pixel in range(l.PIXEL_COUNT):
#                 l.neopixel[pixel] = (255,0,0)
#                 l.neopixel.show()