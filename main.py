import main_loop
import patterns
import time

def main():
    while True:
        main_loop.main_loop()
        time.sleep(1 / patterns.frames_per_second)


if __name__ == "__main__":
    main()