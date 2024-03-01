import main_loop
import patterns
import time

if __name__ == "__main__":
    while True:
        main_loop.main_loop()
        time.sleep(patterns.frames_per_second / 1)