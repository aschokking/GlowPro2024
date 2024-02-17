import time
from light import Light
frames = 70
frame_interval = 5
frame_time_per_interval = frame_interval / frames

recorded_mode = 0
starting = time.time()


def get_states() -> list[int]:
    # if time.time() - starting >= 12:
    #     return [6]
    # if time.time() - starting >= 8:
    #     return[2]
    return [6]


def get_mode():
    """
    1: No_Code
    2: Disabled_No_Auto_Set
    3: Disabled_Auto_Set
    4: Enabled
    """
    return 4