""" Communicate with RoboRIO to obtain robot states and what robot is doing """
from time import sleep as wait

fps = 25
waittime_per_frame = 1 / fps

robot_mode = 1
robot_state = 1


def get_fps() -> int:
    return fps


def get_robot_state():
    return 1


def get_robot_mode():
    # 4: ENABLED
    return 4


def update_state_and_mode():
    global current_mode
    global current_state
    current_mode = get_robot_mode()
    current_state = get_robot_state()


class RobotChangedException(Exception):
    pass

def check_robot_changed():
    # Robot updates every "waittime", so our frames per second is 1/waittime, waittime = 0.04 means 25 fps
    global waittime_per_frame

    if not (current_state == get_robot_state() and current_mode == get_robot_mode()):
        raise RobotChangedException("Robot state or mode changed.")

    wait(waittime_per_frame)