import numpy as np
from data_types import Angle, Vector
import pyinputplus as pyip

while(True):
    print("===========================")
    direction = pyip.inputMenu(["Calculate RL at target", "Calculate RL at instrument"], prompt="Would you like to:\n", numbered=True)
    
    if direction == "Calculate RL at target":
        start_rl = pyip.inputNum("Enter RL at instrument: ")
        instrument_height = pyip.inputNum("Enter instrument height: ")
        target_height = pyip.inputNum("Enter target height: ")
        zenith_angle = pyip.inputNum("Enter zenith angle (ddd.mmss): ")
        zenith_angle = Angle(zenith_angle, 'dms')
        slope_distance = pyip.inputNum("Enter slope distance: ")
        end_rl = start_rl + instrument_height + (slope_distance * np.cos(zenith_angle.radians)) - target_height
        print(f"RL at target: {round(end_rl, 3)}")
    elif direction == "Calculate RL at instrument":
        end_rl = pyip.inputNum("Enter RL at target: ")
        target_height = pyip.inputNum("Enter target height: ")
        instrument_height = pyip.inputNum("Enter instrument height: ")
        zenith_angle = pyip.inputNum("Enter zenith angle (ddd.mmss): ")
        zenith_angle = Angle(zenith_angle, 'dms')
        slope_distance = pyip.inputNum("Enter slope distance: ")
        start_rl = end_rl - (instrument_height + (slope_distance * np.cos(zenith_angle.radians)) - target_height)
        print(f"RL at instrument: {round(start_rl, 3)}")


