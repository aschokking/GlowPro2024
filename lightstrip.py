import neopixel
import patterns

# Serial Data Modes
modes = {
    "AMP_SIGNAL": "1",
    "READY_TO_SHOOT": "2",
    "ROBOT_CONTAINS_NOTE": "3",
    "VISION_SEES_NOTE": "4",
    "DISABLED_WITHOUT_AUTO": "32",
    "DISABLED_WITH_AUTO": "33",
    "PURELY_ENABLED": "34", # None of modes 1-4 are active
    "ROBOT_NOCODE": "31"
}


class LightStrip:

    def __init__(self, pixel_pin, pixel_count: int) -> None:
        # Create a neopixel for each lightstrip
        self.neopixel = neopixel.NeoPixel(pixel_pin, pixel_count, brightness=1, auto_write=False)
        self.PIXEL_COUNT = pixel_count

        # Colors for different patterns
        self.primary: tuple[int, int, int] = (255, 0, 0)
        self.secondary: tuple[int, int, int] = (0, 0, 0)

        # Pattern function to call on every update
        self.pattern_function = patterns.static

        # Which loopcount the pattern started on, used for patterns that require
        # Multiple loops to show its effect (railgun, rainbow)
        self.pattern_starting_loop = 0


    # Assign colors and patterns to light strip
    def assign_mode(self, current_mode: str, last_mode: str):
        # No need to reassign if mode is same as previous loop
        if current_mode == last_mode:
            return
        
        self.pattern_starting_loop = patterns.loopcount

        # Update color and pattern on light to display
        if current_mode == modes["AMP_SIGNAL"]:
            self.pattern_function = patterns.rainbow

        elif current_mode == modes["READY_TO_SHOOT"]:
            # Ready to shoot, railgun pattern (requested by drivers)
            self.primary = (0, 255, 0)
            self.pattern_function = patterns.railgun

        elif current_mode == modes["ROBOT_CONTAINS_NOTE"]:
            self.primary = (255, 165, 0)
            self.pattern_function = patterns.static

        elif current_mode == modes["CENTER_CAM_SEES_NOTE"]:
            self.primary = colors["YELLOW"]
            self.pattern_function = patterns.wavy

        elif current_mode == modes["SIDE_CAM_SEES_NOTE"]:
            self.primary = colors["YELLOW"]
            self.pattern_function = patterns.breathing
    
        elif current_mode == modes["ALL_CAMS_WORKING_DEFAULT"]:
            self.primary = colors["PURPLE"]
            self.pattern_function = patterns.static

        elif current_mode == modes["SOME_CAMS_WORKING_DEFAULT"]:
            self.primary = colors["PURPLE"]
            self.pattern_function = patterns.wavy

        elif current_mode == modes["NO_CAMS_WORKING_DEFEAULT"]:
            self.primary == colors["PURPLE"]
            self.pattern_function = patterns.breathing

        elif current_mode == modes["ALL_CAMS_WORKING_CUSTOM"]:
            self.primary == colors["HOT_PINK"]
            self.pattern_function = patterns.static

        elif current_mode == modes["SOME_CAMS_WORKING_CUSTOM"]:
            self.primary == colors["HOT_PINK"]
            self.pattern_function = patterns.wavy

        elif current_mode == modes["NO_CAMS_WORKING_CUSTOM"]:
            self.primary == colors["HOT_PINK"]
            self.pattern_function = patterns.breathing

        elif current_mode == modes["PURELY_ENABLED"]:
            self.primary = (255, 255, 255)
            self.pattern_function = patterns.static
        else:
            self.primary = (255, 0, 0)
            self.pattern_function = patterns.static