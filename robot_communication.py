import time
from light import Light
frames = 25
frame_interval = 1
frame_time_per_interval = frame_interval / frames

recorded_mode = 0


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