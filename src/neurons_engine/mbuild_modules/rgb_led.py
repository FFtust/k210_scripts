from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

GET_RGB_USE_STRICT_MODE = 1

# most 8 
__RGB_NUM_MAX = 8
__led_value = [[None, None, None]] * (__RGB_NUM_MAX + 1)

def show(r, g, b, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    if not isinstance(r, (int, float)):
        return
    if not isinstance(g, (int, float)):
        return
    if not isinstance(b, (int, float)):
        return

    if index > __RGB_NUM_MAX:
        return

    r = int(num_range_scale(r, 0, 255))
    g = int(num_range_scale(g, 0, 255))
    b = int(num_range_scale(b, 0, 255))
    
    __led_value[int(index)] = [r, g, b]

    neurons_request("m_rgb", "show", (r, g, b), index)

def set_red(val, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    if not isinstance(val, (int, float)):
        return
    
    if index > __RGB_NUM_MAX:
        return

    val = num_range_scale(val, 0, 255)
    __led_value[int(index)][0] = val

    neurons_request("m_rgb", "set_red", val, index)

def set_green(val, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    if not isinstance(val, (int, float)):
        return

    if index > __RGB_NUM_MAX:
        return

    val = num_range_scale(val, 0, 255)
    __led_value[int(index)][1] = val

    neurons_request("m_rgb", "set_green", val, index)

def set_blue(val, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    if not isinstance(val, (int, float)):
        return

    if index > __RGB_NUM_MAX:
        return

    val = num_range_scale(val, 0, 255)
    __led_value[int(index)][2] = val

    neurons_request("m_rgb", "set_blue", val, index)

def change_red(val, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return

    if not isinstance(val, (int, float)):
        return
    
    if index > __RGB_NUM_MAX:
        return

    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][0] == None:
            __get_info(index)

    __led_value[int(index)][0] += val
    __led_value[int(index)][0] = num_range_scale(__led_value[int(index)][0], 0, 255)

    neurons_request("m_rgb", "set_red", __led_value[int(index)][0], index)

def change_green(val, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    if not isinstance(val, (int, float)):
        return

    if index > __RGB_NUM_MAX:
        return

    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][1] == None:
            __get_info(index)

    __led_value[int(index)][1] += val
    __led_value[int(index)][1] = num_range_scale(__led_value[int(index)][1], 0, 255)

    neurons_request("m_rgb", "set_green", __led_value[int(index)][1], index)

def change_blue(val, index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    if not isinstance(val, (int, float)):
        return

    if index > __RGB_NUM_MAX:
        return

    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][2] == None:
            __get_info(index)

    __led_value[int(index)][2] += val
    __led_value[int(index)][2] = num_range_scale(__led_value[int(index)][2], 0, 255)

    neurons_request("m_rgb", "set_blue", __led_value[int(index)][2], index)

def __get_info(index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return
    value = neurons_blocking_read("m_rgb", "get_info", (), index)
    value = value if value != None else [0,0,0]

    if index > __RGB_NUM_MAX:
        return

    __led_value[int(index)] = value

    return value

def get_red(index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return 0
    if index > __RGB_NUM_MAX:
        return 0    
    
    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][0] == None:
            __get_info(index)

    return __led_value[int(index)][0]

def get_green(index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return 0
    if index > __RGB_NUM_MAX:
        return 0    
    
    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][1] == None:
            __get_info(index)

    return __led_value[int(index)][1]


def get_blue(index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return 0
    if index > __RGB_NUM_MAX:
        return 0    
    
    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][2] == None:
            __get_info(index)

    return __led_value[int(index)][2] 

def off(index = 1):
    global __led_value

    if not isinstance(index, (int, float)):
        return

    if index > __RGB_NUM_MAX:
        return    

    neurons_request("m_rgb", "show", (0, 0, 0), index)
    __led_value[int(index)] = [0, 0, 0]



# for online mode, dangerous for user's calling
# index: 0, 1, 2 --- red, green, blue
r_g_b_list = ["set_red", "set_green", "set_blue"] 

def __set_r_g_b(col_id, value, index):
    global __led_value

    value = num_range_scale(value, 0, 255)
    __led_value[index][col_id] = value
    
    neurons_request("m_rgb", r_g_b_list[col_id], value, index)

def __change_r_g_b(col_id, value, index):
    global __led_value

    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][0] == None or __led_value[int(index)][1] == None or \
           __led_value[int(index)][2] == None:
            __get_info(index)

    __led_value[index][col_id] += value
    __led_value[index][col_id] = num_range_scale(__led_value[index][col_id], 0, 255)

    neurons_request("m_rgb", r_g_b_list[col_id], __led_value[index][col_id], index)

def __get_r_g_b(index):
    global __led_value

    if GET_RGB_USE_STRICT_MODE:
        __get_info(index)
    else:
        if __led_value[int(index)][0] == None or __led_value[int(index)][1] == None or \
           __led_value[int(index)][2] == None:
            __get_info(index)

    return __led_value[index]
