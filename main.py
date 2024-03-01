import main_loop
import patterns
import time

def main():
    while True:
        main_loop.main_loop()
        time.sleep(patterns.frames_per_second / 1)


if __name__ == "__main__":
    main()