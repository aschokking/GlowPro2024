import digitalio
import board
import neopixel

def main():
    led = digitalio.DigitalInOut(board.D9)
    led.direction = digitalio.Direction.OUTPUT
    count = 0
    count2 = 0

    light = neopixel.NeoPixel(board.D5, 20, brightness=1, auto_write=False)

    while True:
        for pixel in range(20):
            light[pixel] = (0, 255, 0)
        light.show()
        count += 1
        if count == 20:
            count = 0
            count2 += 1
            if count2 == 80:
                break

            led.value = not led.value

    while True:
        for pixel in range(20):
            light[pixel] = (255, 0, 0)
        light.show()
        pass