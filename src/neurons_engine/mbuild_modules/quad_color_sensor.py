from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_get_block_index
import time

__SENSOR_CHANNEL_1 = 0x00
__SENSOR_CHANNEL_2 = 0x01
__SENSOR_CHANNEL_3 = 0x02
__SENSOR_CHANNEL_4 = 0x03

__TOTAL_CHANNEL_NUM = 0x04
__SENSOR_ALL_CHANNEL = 0x04
__SENSOR_ANY_CHANNEL = 0x05

__INQUIRE_REPORT_MODE = 0x00
__PERIOD_REPORT_MODE = 0x02
__REPORT_TIME = 10

__ON_TRACK = 0X00
__ON_BACKGROUND = 0X01

#global variable definition
g_kp = 0
g_report_time = -1001

# common functions
def _get_channel(channel):
    if channel == "RGB1" or channel == "R2" or channel == "r2" or channel == 1:
        return __SENSOR_CHANNEL_1
    elif channel == "RGB2" or channel == "R1" or channel == "r1" or channel == 2:
        return __SENSOR_CHANNEL_2
    elif channel == "RGB3" or channel == "L1" or channel == "l1" or channel == 3:
        return __SENSOR_CHANNEL_3
    elif channel == "RGB4" or channel == "L2" or channel == "l2" or channel == 4:
        return __SENSOR_CHANNEL_4
    elif channel == "ALL" or channel == "all" or channel == 0:
        return __SENSOR_ALL_CHANNEL
    elif channel == "ANY" or channel == "any" or channel == -1:
        return __SENSOR_ANY_CHANNEL
    else:
        return None

def _get_color_id(color):
        #assert
    if color == "WHITE" or color == "white" or color == "W" or color == "w" :
        color_id = 0x00
    elif color == "PURPLE" or color == "purple" or color == "P" or color == "p":
        color_id = 0x01
    elif color == "RED" or color == "red" or color == "R" or color == "r":
        color_id = 0x02
    elif color == "YELLOW" or color == "yellow" or color == "Y" or color == "y":
        color_id = 0x04
    elif color == "GREEN" or color == "green" or color == "G" or color == "g":
        color_id = 0x05
    elif color == "CYAN" or color == "cyan" or color == "C" or color == "c":
        color_id = 0x06
    elif color == "BLUE" or color == "blue" or color == "B" or color == "b":
        color_id = 0x07
    elif color == "BLACK" or color == "black" or color == "K" or color == "k":
        color_id = 0x09    
    else:
        color_id = None

    return color_id

def _get_state_id(state):
    if state == "0000":
        sta_num = 0
    elif state == "0001":
        sta_num = 1
    elif state == "0010":
        sta_num = 2
    elif state == "0011":
        sta_num = 3
    elif state == "0100":
        sta_num = 4
    elif state == "0101":
        sta_num = 5
    elif state == "0110":
        sta_num = 6
    elif state == "0111":
        sta_num = 7
    elif state == "1000":
        sta_num = 8
    elif state == "1001":
        sta_num = 9
    elif state == "1010":
        sta_num = 10
    elif state == "1011":
        sta_num = 11
    elif state == "1100":
        sta_num = 12
    elif state == "1101":
        sta_num = 13
    elif state == "1110":
        sta_num = 14
    elif state == "1111":
        sta_num = 15
    else:
        sta_num = None

    return sta_num    



def _get_rgb_value(item, channel, index):
    if not isinstance(index, (int, float)):
        return 0

    channel =  _get_channel(channel) 
    if channel == None or channel == __SENSOR_ALL_CHANNEL or channel == __SENSOR_ALL_CHANNEL:
        return 0

    value = neurons_blocking_read("m_quad_color_sensor", "get_color_rgb", (), index)

    if value == None:
        return 0
  
    if channel == __SENSOR_CHANNEL_1:
        ret = value[item]
    elif channel == __SENSOR_CHANNEL_2:
        ret = value[item + 3]
    elif channel == __SENSOR_CHANNEL_3:
        ret = value[item + 6]
    elif channel == __SENSOR_CHANNEL_4:
        ret = value[item + 9]
    return ret

def set_report_mode(mode, timestamp, index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_quad_color_sensor", "set_all_data_report_mode", (mode,timestamp), index)
    else:
        pass

def study(index = 1):
    neurons_request("m_quad_color_sensor", "study", (), index)

'''
list: sensor1­_intensity + sensor2­_intensity + sensor1_state + sensor2_state + offset + sensor1_color + sensor2_color
'''
def get_all_data(index = 1):
    global g_report_time
    
    if time.ticks_ms() - g_report_time > 1000:
        g_report_time = time.ticks_ms()
        set_report_mode(__PERIOD_REPORT_MODE, __REPORT_TIME, index)
    value = neurons_async_read("m_quad_color_sensor", "get_all_data", (), index)#0.25ms
    
    return value

def get_intensity(channel, index = 1):
    if not isinstance(index, (int, float)):
        return 0
    channel =  _get_channel(channel) 
    if channel == None:
        return 0

    value = get_all_data(index)
    return value[channel]

def is_state(state, index = 1):
    if not isinstance(index, (int, float)):
        return False

    if isinstance(state, (str,)):
        sta_num = _get_state_id(state)
    elif isinstance(state, (int,)):
        sta_num = state
    else:
        sta_num = None

    value = get_all_data(index)
    status = int((value[4] | (value[5]<<1) | (value[6]<< 2) | (value[7]<<3)))
    if sta_num == status:
        return True
    else:
        return False

def get_line_sta(index = 1):
    if not isinstance(index, (int, float)):
        return False
    
    value = get_all_data(index)
    status = int((value[4] | (value[5]<<1) | (value[6]<< 2) | (value[7]<<3)))
    return status        

def get_offset_track(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = get_all_data(index)

    return round(value[8] * 100 / 512, 1) # -100 ~ 100

'''
0 – white  1 – purple  2 - red  4–yellow 5 – green 6 – cyan 7 – blue 9 – black
'''
def is_color(color, ch, index = 1):
    if not isinstance(index, (int, float)):
        return False
    if not isinstance(color, (str,)):
        return False
    
    id_list = neurons_get_block_index("m_quad_color_sensor")
    if index > len(id_list):
        return False
        
    channel =  _get_channel(ch) 
    if channel == None:
        return False
    
    #assert
    obj_color = _get_color_id(color)
    if obj_color == None:
        return False

    value = get_all_data(index)
    if channel == __SENSOR_CHANNEL_1:
        actual_color = value[9]
    elif channel == __SENSOR_CHANNEL_2:
        actual_color = value[10]
    elif channel == __SENSOR_CHANNEL_3:
        actual_color = value[11]
    elif channel == __SENSOR_CHANNEL_4:
        actual_color = value[12]
    elif channel == __SENSOR_ALL_CHANNEL:
        if (value[9] == obj_color) and (value[10] == obj_color) and \
            (value[11] == obj_color) and (value[12] == obj_color):
            return True
        else:
            return False
    elif channel == __SENSOR_ANY_CHANNEL:
        if (value[9] == obj_color) or (value[10] == obj_color) or \
            (value[11] == obj_color) or (value[12] == obj_color):
            return True
        else:
            return False
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

def get_color_sta(ch, index = 1):
    if not isinstance(index, (int, float)):
        return None
    channel =  _get_channel(ch) 
    if channel == None:
        return None

    value = get_all_data(index)
    if channel == __SENSOR_CHANNEL_1:
        actual_color_id = value[9]
    elif channel == __SENSOR_CHANNEL_2:
        actual_color_id = value[10]
    elif channel == __SENSOR_CHANNEL_3:
        actual_color_id = value[11]
    elif channel == __SENSOR_CHANNEL_4:
        actual_color_id = value[12]
    else:
        return None
    try:
        return color_switch[actual_color_id]
    except KeyError as e:
        return None


def get_color(ch, index = 1):
    if not isinstance(index, (int, float)):
        return 0

    channel =  _get_channel(ch) 
    if channel == None or channel == __SENSOR_ALL_CHANNEL or channel == __SENSOR_ALL_CHANNEL:
        return 0

    value = neurons_blocking_read("m_quad_color_sensor", "get_color_rgb", (), index)

    if value == None:
        return 0

    ret = (value[channel * 3] << 16) + (value[channel * 3 + 1] << 8)  + (value[channel * 3 + 2])
    return hex(ret)


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

    neurons_request("m_quad_color_sensor", "set_light_color", (obj_color), index)

'''
0 - on_track
1 - on_background
'''
def is_line(ch, index = 1):
    if not isinstance(index, (int, float)):
        return False
    channel =  _get_channel(ch) 
    if channel == None:
        return False

    value = get_all_data(index)
    if channel == __SENSOR_CHANNEL_1:
        actual_value = value[4]
    elif channel == __SENSOR_CHANNEL_2:
        actual_value = value[5]
    elif channel == __SENSOR_CHANNEL_3:
        actual_value = value[6]
    elif channel == __SENSOR_CHANNEL_4:
        actual_value = value[7]
    elif channel == __SENSOR_ALL_CHANNEL:
        actual_value = value[4] or value[5] or value[6] or value[7]
    elif channel == __SENSOR_ANY_CHANNEL:
        actual_value = value[4] and value[5] and value[6] and value[7]
    else:
        return False

    if actual_value == __ON_TRACK:
        return True
    else:
        return False

def is_background(ch, index = 1):
    if not isinstance(index, (int, float)):
        return False
    channel =  _get_channel(ch) 
    if channel == None:
        return False

    value = get_all_data(index)
    if channel == __SENSOR_CHANNEL_1:
        actual_value = value[4]
    elif channel == __SENSOR_CHANNEL_2:
        actual_value = value[5]
    elif channel == __SENSOR_CHANNEL_3:
        actual_value = value[6]
    elif channel == __SENSOR_CHANNEL_4:
        actual_value = value[7]
    elif channel == __SENSOR_ALL_CHANNEL:
        actual_value = value[4] and value[5] and value[6] and value[7] 
    elif channel == __SENSOR_ANY_CHANNEL:
        actual_value = value[4] or value[5] or value[6] or value[7]
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
    track_offset_value = value[8] * 100 / 512 # -100 ~ 100
    return g_kp * track_offset_value    #（get_offset_track_value）* kp

def get_red(ch, index = 1):
    return _get_rgb_value(0x00, ch, index)

def get_green(ch, index = 1):
    return _get_rgb_value(0x01, ch, index)

def get_blue(ch, index = 1):
    return _get_rgb_value(0x02, ch, index)

def get_gray(ch, index = 1):
    if not isinstance(index, (int, float)):
        return 0

    channel =  _get_channel(ch) 
    if channel == None or channel == __SENSOR_ALL_CHANNEL or channel == __SENSOR_ALL_CHANNEL:
        return 0

    value = neurons_blocking_read("m_quad_color_sensor", "get_reflect_data", (), index)
    if value == None:
        return 0
    else:
        if channel == __SENSOR_CHANNEL_1:
            return value[0]
        elif channel == __SENSOR_CHANNEL_2:
            return value[1]
        if channel == __SENSOR_CHANNEL_3:
            return value[2]
        elif channel == __SENSOR_CHANNEL_4:
            return value[3]


def get_light(ch, index = 1):
    if not isinstance(index, (int, float)):
        return 0

    channel =  _get_channel(ch) 
    if channel == None or channel == __SENSOR_ALL_CHANNEL or channel == __SENSOR_ALL_CHANNEL:
        return 0

    value = neurons_blocking_read("m_quad_color_sensor", "get_evm_data", (), index)
    if value == None:
        return 0
    else:
        if channel == __SENSOR_CHANNEL_1:
            return value[0]
        elif channel == __SENSOR_CHANNEL_2:
            return value[1]
        if channel == __SENSOR_CHANNEL_3:
            return value[2]
        elif channel == __SENSOR_CHANNEL_4:
            return value[3]



def set_led(color="white", index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(color, (str,)):
        return

    color_id = _get_color_id(color)
    if color_id == None:
        return
    
    neurons_request("m_quad_color_sensor", "set_rgb_color", color_id, index)


def off_led(index = 1):
    if not isinstance(index, (int, float)):
        return

    color_id = _get_color_id("black")
    if color_id == None:
        return
    
    neurons_request("m_quad_color_sensor", "set_rgb_color", color_id, index)