from robotstates import get_robot_state, get_robot_mode, RobotChangedException, update_state_and_mode
from patterns import static, moving_rainbow, flash, set_primary_color, set_secondary_color, wavy #alternating


# Main function
def main_loop():
    # Assuming we are getting a state
    # Also, "action" or "rainbow" states should have higher priority than static
    update_state_and_mode()
    robot_state = get_robot_state()
    robot_mode = get_robot_mode()
    

    # Run the lights (actual displaying)
    try:
        if robot_mode == 1:
            # NO_CODE
            set_primary_color("ORANGE")
            static()

        elif robot_mode == 2:
            # DISABLED_NO_AUTO
            set_primary_color("GRAY")
            static()

        elif robot_mode == 3:
            # DISABLED_WITH_AUTO
            set_primary_color("GRAY")
            flash()

        elif robot_mode == 4:
            # ENABLED
            if robot_state == 1:
                set_primary_color("GREEN")
                wavy()
            elif robot_state == 2:
                set_primary_color("GREEN")
                moving_rainbow()
            elif robot_state == 3:
                set_primary_color("RED")
                flash()
                pass
            elif robot_state == 4:
                set_primary_color("RED")
                flash()
                pass
            elif robot_state == 5:
                set_primary_color("GREEN")
                static()
                pass
            elif robot_state == 5:
                set_primary_color("GREEN")
                #alternating()
                pass
            else:
                print("State not matched")
        else:
            print("Mode not matched") # Not the best code aesthetics
        
    except RobotChangedException:
        # Restarting loop as mode has been changed
        pass
    
        

# Main Loop
if __name__ == "__main__":
    while True:
        main_loop()


# So apparently how this year (2024) lights will work is that we will get like a serial, a text constantly on
# probably what command is running and we can update our lights based off of it
# Keep everything above line 144 just for reference ;), that way we don't have to navigate through github

# Intaking - flashing orange (or any color)

# When holding note with arm - static green

# Shooter Rev - charge up based on desired rpm
    # Shooting - flash a quick white light

# Not holding note - Blue

# Signal amp button - rave

# In a horrible state - flashing red

# # ## # # # # LightDisplayState.Charging:
#         brightness += .5
#     if brightness >= 1
#         light_state == LightDisplayState.Charging:#below is a function for testing flashing
# def flashing_lights(color):
#     delay = 0.25 
#     flashes = 10
#     for _ in range(flashes):
#         set_primary_color(color)
#         pixels.show()
#         time.sleep(delay)
#     pixels.show(False)


# #below is a function for testing shooter
# def shooting_lights(color):
#     global light_stateg
#     while True:
#         pass#below is a function for testing flashing
        
        

# def flashing_lights(color):
#     delay = 0.25 
#     flashes = 10
#     for _ in range(flashes):
#         set_primary_color(color)
#         pixels.show()
#         time.sleep(delay)
#     pixels.show(False)
# def rainbow_rave()
