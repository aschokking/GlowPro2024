import time
from light import Light
frames = 25
frame_interval = 1
frame_time_per_interval = frame_interval / frames

recorded_mode = 0


def check_robot(light: Light, waittime: float = 0):
    """ Checks if the robot mode has changed and if the light state has changed """
    if not recorded_mode == get_mode():
        return False

    if not light.state in get_states():
        return False
    
    time.sleep(frame_time_per_interval + waittime)
    return True


def get_states() -> list[int]:
    return [1]


def get_mode():
    """
    1: No_Code
    2: Disabled_No_Auto_Set
    3: Disabled_Auto_Set
    4: Enabled
    """
    return 4