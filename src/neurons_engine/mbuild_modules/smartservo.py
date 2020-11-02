from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_get_block_index

import time
# RPM: revolution per minute 
# DPS: degree per second
SPEED_RPM_TO_DPS = 6        # 360 / 60   
SPEED_DPS_TO_RPM = 0.167    # 60 / 360

#private function
def set_zero(index = 1):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 
    neurons_request("m_smartservo", "set_zero", [], index)

def move_to(position, speed, index = 1):
    if (not isinstance(position, (int))) or (not isinstance(speed, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    speed = num_range_scale(speed, 1, 50)
    neurons_request("m_smartservo", "move_to", [position, speed], index)

def move(position, speed, index = 1):
    if (not isinstance(position, (int))) or (not isinstance(speed, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    speed = num_range_scale(speed, 1, 50)
    neurons_request("m_smartservo", "move", [position, speed], index)

def set_power(pwm, index = 1):
    if (not isinstance(pwm, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    pwm = num_range_scale(pwm, -255, 255)
    #print(pwm)
    neurons_request("m_smartservo", "set_pwm", -pwm, index)

def set_speed_upload_mode(mode, index = 1):
    if (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smartservo", "get_speed", mode, index)

def set_position_upload_mode(mode, index = 1):
    if (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smartservo", "get_position", mode, index)

def back_to_zero(speed, index = 1):
    if (not isinstance(speed, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    speed = num_range_scale(speed, 1, 50)
    neurons_request("m_smartservo", "back_to_zero", [0x00, speed], index)

def move_to_in_time(position, time, index = 1):
    if (not isinstance(position, (int))) or (not isinstance(time, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    time = num_range_scale(time, 1, 16383)
    neurons_request("m_smartservo", "move_to_in_time", [position, time], index)

def move_to_with_torque(position, speed, strength, index = 1):
    if (not isinstance(position, (int))) or (not isinstance(speed, (int, ))) or (not isinstance(strength, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    speed = num_range_scale(speed, 1, 50)
    strength = num_range_scale(strength, 1, 255)
    neurons_request("m_smartservo", "move_to_with_torque", [position, speed, strength], index)

def move_with_torque(position, speed, strength, index = 1):
    if (not isinstance(position, (int))) or (not isinstance(speed, (int, ))) or (not isinstance(strength, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    speed = num_range_scale(speed, 1, 50)
    strength = num_range_scale(strength, 1, 255)
    neurons_request("m_smartservo", "move_with_torque", [position, speed, strength], index)

def lock(index = 1):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    neurons_request("m_smartservo", "lock_unlock", 0x00, index)

def unlock(index = 1):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    neurons_request("m_smartservo", "lock_unlock", 0x01, index)

#function for building block
def turn(angle, speed, index = 1):  # angle: drgree   speed:unit :degree per second
    if (not isinstance(angle, (int))) or (not isinstance(speed, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    # speed unit for users is degree per second
    # but real speed unit is rpm(revolutions per minute) 
    speed = round(speed * SPEED_DPS_TO_RPM)
    speed = num_range_scale(speed, 1, 50)
    neurons_request("m_smartservo", "move", [-angle, speed], index)

def turn_to(angle, speed, index = 1 ): # angle: drgree   speed:unit :degree per second
    if (not isinstance(angle, (int))) or (not isinstance(speed, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 
    # speed unit for users is degree per second
    # but real speed unit is rpm(revolutions per minute) 
    speed = round(speed * SPEED_DPS_TO_RPM)
    speed = num_range_scale(speed, 1, 50)
    
    neurons_request("m_smartservo", "move_to", [-angle, speed], index)

def stop(index = "all"):
    if index == "all":
        id_list = neurons_get_block_index("m_smartservo")
        for index in range(len(id_list)):
            neurons_request("m_smartservo", "set_pwm", 0, index + 1)
    else:
        if (not isinstance(index, (int))) or (index <= 0):
            return
        neurons_request("m_smartservo", "set_pwm", 0, index)

def run(power, index = 1):
    if (not isinstance(power, (int, ))) or (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    power = num_range_scale(power, -100, 100)

    # scale for user is -100 ~ 100, real is -255 ~ 255
    power = round(power * 2.55) # 255 / 100

    neurons_request("m_smartservo", "set_pwm", -power, index)

def get_angle(index = 1):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return 0
    value = neurons_async_read("m_smartservo", "get_position", (0x01), index)

    if value != None:
        return -int(value[0])
    else:
        return 0

def get_speed(index = 1):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return 0
    value = neurons_async_read("m_smartservo", "get_speed", (0x01), index)

    if value != None:
        if value[0] == (-1) or value[0] == (0) or value[0] == (1) or value[0] == (2):
            return 0
        else:
            # speed unit for users is degree per second
            # but real speed unit is rpm(revolutions per minute) 
            return -int(value[0] * SPEED_RPM_TO_DPS)
    else:
        return 0

def get_cycles(index = 1):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return 0
    value = neurons_async_read("m_smartservo", "get_position", (0x01), index)
    # print(value)
    if value != None:
        cycles = -int(value[0]/360)
        return cycles
    else:
        return 0

def lock_angle(index = "all"):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 
    
    neurons_request("m_smartservo", "lock_unlock", 0x00, index)

def release_angle(index = "all"):
    if (not isinstance(index, (int, ))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    neurons_request("m_smartservo", "lock_unlock", 0x01, index)

def reset(index = "all"):
    if (not isinstance(index, (int))) or (index <= 0):
        return
    if index == "all":
        index = 0xff 

    neurons_request("m_smartservo", "set_zero", [], index)

    # reserve 3 seconds, avoid frequent calling of this function.
    # because this api will operate the flash
    time.sleep(3)