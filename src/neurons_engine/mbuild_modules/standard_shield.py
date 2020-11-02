from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_get_block_index
import time
##############################################################################################################
#########################   DC motor API   ###################################################################
##############################################################################################################
def dc_motor_set_power(motor_index, power, device_index = 1):
    if not isinstance(motor_index, (int, float)):
        return     
    if not isinstance(power, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    motor_index = num_range_scale(motor_index, 0, 127)
    power = num_range_scale(power, -100, 100) 
    neurons_request("m_standard_shield", "dc_motor_set_power", (motor_index, power), device_index)


def dc_motor_set_power_both(power_1, power_2, device_index = 1):
    if not isinstance(power_1, (int, float)):
        return     
    if not isinstance(power_2, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    power_1 = num_range_scale(power_1, -100, 100)
    power_2 = num_range_scale(power_2, -100, 100) 
    neurons_request("m_standard_shield", "dc_motor_set_power_both", (power_1,power_2), device_index)


def dc_motor_change_power(motor_index, power, device_index = 1):
    if not isinstance(motor_index, (int, float)):
        return     
    if not isinstance(power, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    motor_index = num_range_scale(motor_index, 0, 127)
    power = num_range_scale(power, -200, 200)
    neurons_request("m_standard_shield", "dc_motor_change_power", (motor_index, power), device_index)


def dc_motor_stop(motor_index = 1, device_index = 1):
    if not isinstance(motor_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    motor_index = num_range_scale(motor_index, 0, 127)
    power = 0
    neurons_request("m_standard_shield", "dc_motor_stop",(motor_index), device_index)


def dc_motor_get_power(motor_index = 1, device_index = 1):
    if not isinstance(motor_index, (int, float)):
        return -1
    if not isinstance(device_index, (int, float)):
        return -1
    if motor_index not in [1, 2]:
        return -1
    ret = neurons_blocking_read("m_standard_shield", "dc_motor_get_power", (motor_index), device_index)
    if ret:
        return ret[1]
    else:
        return 0
##############################################################################################################
#########################   DC motor API   ###################################################################
##############################################################################################################




##############################################################################################################
#########################   AC servo API   ###################################################################
##############################################################################################################
__INQUIRE_REPORT_MODE = 0x00
__CHANGE_REPORT_MODE = 0x01
__PERIOD_REPORT_MODE = 0x02

def servo_set_angle(servo_index, angle, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(angle, (int, float)):
        return
    servo_index = num_range_scale(servo_index, 0, 127)
    angle = num_range_scale(angle, 0, 180)
    neurons_request("m_standard_shield", "servo_set_angle", (servo_index, angle), device_index)


def servo_set_angle_both(angle_1, angle_2, device_index = 1):
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(angle_1, (int, float)):
        return
    if not isinstance(angle_2, (int, float)):
        return
    angle_1 = num_range_scale(angle_1, 0, 180)
    angle_2 = num_range_scale(angle_2, 0, 180)    
    neurons_request("m_standard_shield", "servo_set_angle_both", (angle_1, angle_2), device_index)


def servo_change_angle(servo_index, angle, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(angle, (int, float)):
        return
    servo_index = num_range_scale(servo_index, 0, 127)        
    angle = num_range_scale(angle, -180, 180)
    neurons_request("m_standard_shield", "servo_change_angle", (servo_index, angle), device_index)


def servo_change_angle_both(angle_1, angle_2, device_index = 1):
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(angle_1, (int, float)):
        return
    if not isinstance(angle_2, (int, float)):
        return
    angle_1 = num_range_scale(angle_1, -180, 180)
    angle_2 = num_range_scale(angle_2, -180, 180)    
    neurons_request("m_standard_shield", "servo_change_angle_both", (angle_1, angle_2), device_index)


def servo_release(servo_index = 1, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    servo_index = num_range_scale(servo_index, 0, 127)        
    neurons_request("m_standard_shield", "servo_release", (servo_index), device_index)


def servo_set_pulse_width(servo_index, pulse_width, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(pulse_width, (int, float)):
        return
    servo_index = num_range_scale(servo_index, 0, 127)
    pulse_width = num_range_scale(pulse_width, 0, 16383)
    neurons_request("m_standard_shield", "servo_set_pulse_width", (servo_index, pulse_width), device_index)


def servo_get_angle(servo_index = 1, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return -1
    if not isinstance(device_index, (int, float)):
        return -1
    if servo_index not in [1, 2]:
        return -1
    value = neurons_blocking_read("m_standard_shield", "servo_get_angle", (servo_index), device_index)
    if value != None:
        return value[1]
    else:
        return 0


def servo_get_angle_both(device_index = 1):
    if not isinstance(device_index, (int, float)):
        return -1
    value = neurons_blocking_read("m_standard_shield", "servo_get_angle_both", (), device_index)
    if value != None:
        return value
    else:
        return [0,0]


def servo_get_load(servo_index = 1, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return -1
    if not isinstance(device_index, (int, float)):
        return -1
    if servo_index not in [1, 2]:
        return -1
    value = neurons_blocking_read("m_standard_shield", "servo_get_load", (servo_index), device_index)
    if value != None:
        return value[0]
    else:
        return 0


def servo_reset(servo_index = 1, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    neurons_request("m_standard_shield", "servo_reset", (servo_index), device_index)


def servo_set_report_mode(servo_index, mode, timestamp, device_index = 1):
    if not isinstance(servo_index, (int, float)):
        return
    if not isinstance(timestamp, (int, float)):
        return
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == __INQUIRE_REPORT_MODE or mode == __CHANGE_REPORT_MODE or mode == __PERIOD_REPORT_MODE:
        neurons_request("m_standard_shield", "servo_set_report_mode", (servo_index, mode, timestamp), device_index)
    else:
        return
##############################################################################################################
#########################   AC servo API   ###################################################################
##############################################################################################################




##############################################################################################################
#########################   LED strip API  ###################################################################
##############################################################################################################
def led_strip_set_single(strip_index, led_index, red_value, green_value, blue_value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return
    if not isinstance(led_index, (int, float)):
        return
    if not isinstance(red_value, (int, float)):
        return
    if not isinstance(green_value, (int, float)):
        return
    if not isinstance(blue_value, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return 
    strip_index = num_range_scale(strip_index, 0, 127)            
    led_index = num_range_scale(led_index, 0, 127)       
    red_value = num_range_scale(red_value, 0, 255)
    green_value = num_range_scale(green_value, 0, 255)
    blue_value = num_range_scale(blue_value, 0, 255)
    neurons_request("m_standard_shield", "led_strip_set_single", (strip_index, led_index, red_value, green_value, blue_value), device_index)


def led_strip_set_all(strip_index, red_value, green_value, blue_value, device_index = 1):
    led_strip_set_single(strip_index, 00, red_value, green_value, blue_value, device_index)


def led_strip_off_all(strip_index, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    neurons_request("m_standard_shield", "led_strip_off_all", (strip_index), device_index)


def led_strip_set_red(strip_index, led_index, value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 0, 127)
    value = num_range_scale(value, 0, 255)
    neurons_request("m_standard_shield", "led_strip_set_red", (strip_index, led_index, value), device_index)


def led_strip_set_green(strip_index, led_index, value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 0, 127)
    value = num_range_scale(value, 0, 255)
    neurons_request("m_standard_shield", "led_strip_set_green", (strip_index, led_index, value), device_index)


def led_strip_set_blue(strip_index, led_index, value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 0, 127)
    value = num_range_scale(value, 0, 255)
    neurons_request("m_standard_shield", "led_strip_set_blue", (strip_index, led_index, value), device_index)


def led_strip_change_red(strip_index, led_index, value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 0, 127)
    value = num_range_scale(value, -255, 255)
    neurons_request("m_standard_shield", "led_strip_change_red", (strip_index, led_index, value), device_index)


def led_strip_change_green(strip_index, led_index, value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)     
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 0, 127)
    value = num_range_scale(value, -255, 255)
    neurons_request("m_standard_shield", "led_strip_change_green", (strip_index, led_index, value), device_index)


def led_strip_change_blue(strip_index, led_index, value, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)        
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 0, 127)
    value = num_range_scale(value, -255, 255)
    neurons_request("m_standard_shield", "led_strip_change_blue", (strip_index, led_index, value), device_index)


def led_strip_set_mode(strip_index, mode, device_index =1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(mode, (str,)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)        
    if mode == "static":
        mode = 0x00
    elif mode == "marquee":
        mode = 0x03
    elif mode == "breathe":
        mode = 0x04
    else:
        return
    neurons_request("m_standard_shield", "led_strip_set_mode", (strip_index, mode), device_index)
 

def led_strip_set_block(strip_index, led_num, data, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(led_num, (int, float)):
        return
    if not isinstance(data, (list, tuple)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)        
    list_data = list()
    if led_num <= 0:
        return
    elif led_num < len(data):
        list_data.extend(data[0 : led_num])
    else:
        list_data.extend(data)       
    neurons_request("m_standard_shield", "led_strip_set_block", (strip_index, list_data), device_index)


def led_strip_set_brightness(strip_index = 1, brightness = 50, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(brightness, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    brightness = num_range_scale(brightness, 0, 100)   
    neurons_request("m_standard_shield", "led_strip_set_brightness", (strip_index, brightness), device_index)


def led_strip_change_brightness(strip_index = 1, brightness = 30, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(brightness, (int, float)):
        return   
    strip_index = num_range_scale(strip_index, 0, 127)
    brightness = num_range_scale(brightness, -100, 100) 
    neurons_request("m_standard_shield", "led_strip_change_brightness", (strip_index, brightness), device_index)


def led_strip_get_brightness(strip_index = 1, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return -1 
    if not isinstance(device_index, (int, float)):
        return -1
    if strip_index not in [1, 2]:
        return -1
    ret = neurons_blocking_read("m_standard_shield", "led_strip_get_brightness", (strip_index), device_index)
    if ret:
        return ret[1]
    else:
        return -1


def led_strip_set_move(strip_index = 1, move_step = 1, move_cycle = 1, device_index = 1):          ##  led_move(step, cycle, port)
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(move_step, (int, float)):
        return
    if not isinstance(move_cycle, (int, float)):
        return
    strip_index = num_range_scale(strip_index, 0, 127)
    move_step = num_range_scale(move_step, -128, 127)
    move_cycle = num_range_scale(move_cycle, 0, 127)                          
    neurons_request("m_standard_shield", "led_strip_set_move", (strip_index, move_step,move_cycle), device_index)


'''
def led_strip_set_effect(strip_index, mode, speed, data, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return       
    if not isinstance(speed, (int, float)):
        return
    if not isinstance(data, (list, tuple)):
        return
    if mode == "static" or mode == "steady":
        mode = 0x00
    elif mode == "marquee":
        mode = 0x03
    elif mode == "breathe":
        mode = 0x04
    else:
        return
    speed = num_range_scale(speed, 0, 8)
    list_data = list()
    list_data.append(speed)
    list_data.extend(data)
    neurons_request("m_standard_shield", "led_strip_set_mode", (strip_index, mode), device_index)
    neurons_request("m_standard_shield", "led_strip_set_block", (strip_index, data), device_index)


def led_strip_show(strip_index, color, device_index = 1):
    if not isinstance(strip_index, (int, float)):
        return 
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(color, (list, tuple)):
        return   
    for i in range(len(color)):
        if isinstance(color[i], str) and (color[i] in mbuild_color_table):
            color[i] = mbuild_color_table[color[i]]
        elif isinstance(color[i], (int, float)):
            pass
        else:
            color[i] = 0
        
    neurons_request("m_standard_shield", "led_strip_set_block", (strip_index, color), device_index)
'''    
##############################################################################################################
#########################   LED strip API  ###################################################################
##############################################################################################################





##############################################################################################################
#########################   power management API  ############################################################
##############################################################################################################
def power_get_battery_voltag(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    ret = neurons_blocking_read("m_standard_shield", "power_get_battery_voltag", (), device_index)
    if ret:
        return ret[0]
    else:
        return 0 


def power_set_battery_voltag_mode(mode, period, device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    if not isinstance(mode, (int, float)):
        return 0
    if not isinstance(period, (int, float)):
        return 0        
    neurons_request("m_standard_shield", "power_set_battery_voltag_mode", (mode, period), device_index)


def power_get_usb_state(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    ret = neurons_blocking_read("m_standard_shield", "power_get_usb_state", (), device_index)
    if ret:
        return ret[0]
    else:
        return 0


def power_set_usb_state_mode(mode, period, device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    if not isinstance(mode, (int, float)):
        return 0
    if not isinstance(period, (int, float)):
        return 0        
    neurons_request("m_standard_shield", "power_set_usb_state_mode", (mode, period), device_index)


def power_get_switch_state(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    ret = neurons_blocking_read("m_standard_shield", "power_get_switch_state", (), device_index)
    if ret:
        return ret[0]
    else:
        return 0


def power_set_switch_state_mode(mode, period, device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    if not isinstance(mode, (int, float)):
        return 0
    if not isinstance(period, (int, float)):
        return 0        
    neurons_request("m_standard_shield", "power_set_switch_state_mode", (mode, period), device_index)


def power_get_charge_state(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    ret = neurons_blocking_read("m_standard_shield", "power_get_charge_state", (), device_index)
    if ret:
        return ret[0]
    else:
        return 0


def power_set_charge_state_mode(mode, period, device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    if not isinstance(mode, (int, float)):
        return 0
    if not isinstance(period, (int, float)):
        return 0        
    neurons_request("m_standard_shield", "power_set_charge_state_mode", (mode, period), device_index)


def power_get_battery_level(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    ret = neurons_blocking_read("m_standard_shield", "power_get_battery_level", (), device_index)
    if ret:
        return ret[0]
    else:
        return 0


def power_set_battery_level_mode(mode, period, device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    if not isinstance(mode, (int, float)):
        return 0
    if not isinstance(period, (int, float)):
        return 0        
    neurons_request("m_standard_shield", "power_set_battery_level_mode", (mode, period), device_index) 


def power_get_power_all_state(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    ret = neurons_blocking_read("m_standard_shield", "power_get_power_all_state", (), device_index)
    if ret:
        return ret
    else:
        return 0


def power_set_power_all_state_mode(mode, period, device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return 0
    if not isinstance(mode, (int, float)):
        return 0
    if not isinstance(period, (int, float)):
        return 0        
    neurons_request("m_standard_shield", "power_set_power_all_state_mode", (mode, period), device_index) 


def power_respond_power_all_state(device_index = 1):    
    if not isinstance(device_index, (int, float)):
        return False       
    ret = neurons_async_read("m_standard_shield", "power_get_power_all_state", (), device_index)
    if ret:
        return ret
    else:
        return False    
##############################################################################################################
#########################   power management API  ############################################################
##############################################################################################################




##############################################################################################################
#########################   multifunction port API  ##########################################################
##############################################################################################################
def multifunction_digital_write(port, value, device_index =1):
    if not isinstance(port, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(value, (int, float)):
        return
    port = num_range_scale(port, 0, 127)        
    value = num_range_scale(value, 0, 1)
    neurons_request("m_standard_shield", "multifunction_digital_write", (port, value), device_index)


def multifunction_digital_read(port, device_index =1):
    if not isinstance(port, (int, float)):
        return -1
    if not isinstance(device_index, (int, float)):
        return -1
    if port not in [1, 2]:
        return -1          
    ret = neurons_blocking_read("m_standard_shield", "multifunction_digital_read", (port), device_index)
    if ret:
        return ret[1]
    else:
        return -1
        

def multifunction_analog_read(port, device_index =1):
    if not isinstance(port, (int, float)):
        return -1
    if not isinstance(device_index, (int, float)):
        return -1
    if port not in [1, 2]:
        return -1
    ret = neurons_blocking_read("m_standard_shield", "multifunction_analog_read", (port), device_index)
    if ret:
        return ret[1]
    else:
        return -1


def multifunction_pwm_set(port, duty, frequency, device_index =1):
    if not isinstance(port, (int, float)):
        return
    if not isinstance(device_index, (int, float)):
        return
    if not isinstance(duty, (int, float)):
        return
    if not isinstance(frequency, (int, float)):
        return
    port = num_range_scale(port, 0, 127)
    duty = num_range_scale(duty, 0, 100)
    frequency = num_range_scale(frequency, 0, 2000)    
    neurons_request("m_standard_shield", "multifunction_pwm_set", (port, duty, frequency), device_index)
##############################################################################################################
#########################   multifunction port API  ##########################################################
##############################################################################################################






