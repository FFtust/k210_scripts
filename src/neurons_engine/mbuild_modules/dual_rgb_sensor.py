from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_get_block_index
import time

__SENSOR_CHANNEL_1 = 0x00
__SENSOR_CHANNEL_2 = 0x01
__SENSOR_ALL_CHANNEL = 0x02
__TOTAL_CHANNEL_NUM = 0x02

__INQUIRE_REPORT_MODE = 0x00
__PERIOD_REPORT_MODE = 0x02
__REPORT_TIME = 30

__ON_TRACK = 0X00
__ON_BACKGROUND = 0X01

#global variable definition
g_kp = 0
g_report_time = -1001

# common functions
def _get_channel(ch):
    if ch == "RGB1":
        return __SENSOR_CHANNEL_1
    elif ch == "RGB2":
        return __SENSOR_CHANNEL_2
    elif ch == "ALL":
        return __SENSOR_ALL_CHANNEL
    elif ch == 1:
        return __SENSOR_CHANNEL_1
    elif ch == 2:
        return __SENSOR_CHANNEL_2
    else:
        return None

def _get_color_id(color):
        #assert
    if color == "white" or color == "w":
        color_id = 0x00
    elif color == "purple" or color == "p":
        color_id = 0x01
    elif color == "red" or color == "r":
        color_id = 0x02
    elif color == "yellow" or color == "y":
        color_id = 0x04
    elif color == "green" or color == "g":
        color_id = 0x05
    elif color == "cyan" or color == "c":
        color_id = 0x06
    elif color == "blue" or color == "b":
        color_id = 0x07
    elif color == "black" or color == "k":
        color_id = 0x09    
    else:
        color_id = None

    return color_id

def _get_rgb_value(item, ch, index):
    if not isinstance(index, (int, float)):
        return 0

    ch =  _get_channel(ch) 
    if ch == None:
        return 0

    value = neurons_blocking_read("m_dual_rgb_sensor", "get_color_rgb", (), index)

    if value == None:
        return 0
  
    if ch == __SENSOR_CHANNEL_1:
        ret = value[item]
    elif ch == __SENSOR_CHANNEL_2:
        ret = value[item + 3]

    return ret

def set_report_mode(mode, timestamp, index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_dual_rgb_sensor", "set_all_data_report_mode", (mode,timestamp), index)
    else:
        pass

def study(index = 1):
    neurons_request("m_dual_rgb_sensor", "study", (), index)

'''
list: sensor1­_intensity + sensor2­_intensity + sensor1_state + sensor2_state + offset + sensor1_color + sensor2_color
'''
def get_all_data(index = 1):
    global g_report_time
    
    if time.ticks_ms() - g_report_time > 1000:
        g_report_time = time.ticks_ms()
        set_report_mode(__PERIOD_REPORT_MODE, __REPORT_TIME, index)
    value = neurons_async_read("m_dual_rgb_sensor", "get_all_data", (), index)#0.25ms
    
    return value

def get_intensity(ch, index = 1):
    if not isinstance(index, (int, float)):
        return 0
    ch =  _get_channel(ch) 
    if ch == None:
        return 0

    value = get_all_data(index)
    
    return round(value[ch] * 100 / 255)

def is_state(state, index = 1):
    if not isinstance(index, (int, float)):
        return False
    
    if state == "00":
        state = 0x00
    elif state == "01":
        state = 0x01
    elif state == "10":
        state = 0x02
    elif state == "11":
        state = 0x03
    else:
        return False

    value = get_all_data(index)
    status = (value[2] | (value[3]<<1))
    if state == status:
        return True
    else:
        return False

def get_offset_track_value(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = get_all_data(index)

    return round(value[4] * 100 / 512, 1) # -100 ~ 100

'''
0 – white  1 – purple  2 - red  4–yellow 5 – green 6 – cyan 7 – blue 9 – black
'''
def is_color(ch, color, index = 1):
    if not isinstance(index, (int, float)):
        return False
    if not isinstance(color, (str,)):
        return False
    
    id_list = neurons_get_block_index("m_dual_rgb_sensor")
    if index > len(id_list):
        return False
        
    ch =  _get_channel(ch) 
    if ch == None:
        return False
    
    #assert
    obj_color = _get_color_id(color)
    if obj_color == None:
        return False

    value = get_all_data(index)
    if ch == __SENSOR_CHANNEL_1:
        actual_color = value[5]
    elif ch == __SENSOR_CHANNEL_2:
        actual_color = value[6]
    else:
        return False

    if obj_color == actual_color:
        return True
    else:
        return False

#color dictionary
color_switch = {
    0: 'white',
    1: 'purple',
    2: 'red',
    4: 'yellow',
    5: 'green',
    6: 'cyan',
    7: 'blue',
    9: 'black'
}

def get_color(ch, index = 1):
    if not isinstance(index, (int, float)):
        return None
    ch =  _get_channel(ch) 
    if ch == None:
        return None

    value = get_all_data(index)
    if ch == __SENSOR_CHANNEL_1:
        actual_color_id = value[5]
    elif ch == __SENSOR_CHANNEL_2:
        actual_color_id = value[6]
    elif ch == __SENSOR_ALL_CHANNEL:
        '''
        if value[5] == value[6]:
            actual_color_id = value[5]
        else:
            actual_color_id = None
        '''
        color_list = []
        try:
            color_list.append(color_switch[value[5]])
            color_list.append(color_switch[value[6]])
            return color_list
        except KeyError as e:
            return None
    else:
        return None
    try:
        return color_switch[actual_color_id]
    except KeyError as e:
        return None

'''
0x00 – RED
0x01 – GREEN
0x02 – BLUE
'''
def set_led_color(color, index = 1):
    if not isinstance(index, (int, float)):
        return None
    if isinstance(color, (str,)) == False:
        return None

    #assert
    if color == "red":
        obj_color = 0x00
    elif color == "green":
        obj_color = 0x01
    elif color == "blue":
        obj_color = 0x02
    else:
        return None

    neurons_request("m_dual_rgb_sensor", "set_light_color", (obj_color), index)

'''
0 - on_track
1 - on_background
'''
def is_on_track(ch, index = 1):
    if not isinstance(index, (int, float)):
        return False
    ch =  _get_channel(ch) 
    if ch == None:
        return False

    value = get_all_data(index)
    if ch == __SENSOR_CHANNEL_1:
        actual_value = value[2]
    elif ch == __SENSOR_CHANNEL_2:
        actual_value = value[3]
    else:
        return False

    if actual_value == __ON_TRACK:
        return True
    else:
        return False

def is_on_background(ch, index = 1):
    if not isinstance(index, (int, float)):
        return False
    ch =  _get_channel(ch) 
    if ch == None:
        return False

    value = get_all_data(index)
    if ch == __SENSOR_CHANNEL_1:
        actual_value = value[2]
    elif ch == __SENSOR_CHANNEL_2:
        actual_value = value[3]
    else:
        return False

    if actual_value == __ON_BACKGROUND:
        return True
    else:
        return False

def set_motor_diff_speed_kp(value):
    global g_kp

    if isinstance(value, (float,))==False:
        return None
    g_kp = value

def get_motor_diff_speed(index = 1):
    global g_kp

    value = get_all_data(index)
    track_offset_value = value[4] * 100 / 512 # -100 ~ 100
    return g_kp * track_offset_value    #（get_offset_track_value）* kp

def get_red(ch, index = 1):
    return _get_rgb_value(0x00, ch, index)

def get_green(ch, index = 1):
    return _get_rgb_value(0x01, ch, index)

def get_blue(ch, index = 1):
    return _get_rgb_value(0x02, ch, index)

def get_reflected_light(ch, index = 1):
    if not isinstance(index, (int, float)):
        return 0

    ch =  _get_channel(ch) 
    if ch == None:
        return 0

    value = neurons_blocking_read("m_dual_rgb_sensor", "get_reflect_data", (), index)
    if value == None:
        return 0
    else:
        if ch == __SENSOR_CHANNEL_1:
            return value[0]
        elif ch == __SENSOR_CHANNEL_2:
            return value[1]

def set_light_color(color, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(color, (str,)):
        return

    color_id = _get_color_id(color)
    if color_id == None:
        return
    
    neurons_request("m_dual_rgb_sensor", "set_rgb_color", color_id, index)




