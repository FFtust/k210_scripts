from common import num_range_scale, mbuild_color_table
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

def set_single(led_index, red_value, green_value, blue_value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(led_index, (int, float)):
        return
    if not isinstance(red_value, (int, float)):
        return
    if not isinstance(green_value, (int, float)):
        return
    if not isinstance(blue_value, (int, float)):
        return
    
    led_index = num_range_scale(led_index, 1, 127)
        
    red_value = num_range_scale(red_value, 0, 255)
    green_value = num_range_scale(green_value, 0, 255)
    blue_value = num_range_scale(blue_value, 0, 255)
    neurons_request("m_rgb_led_ring", "set_rgb", (led_index, red_value, green_value, blue_value), index)

def set_all(red_value, green_value, blue_value, index = 1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(red_value, (int, float)):
        return
    if not isinstance(green_value, (int, float)):
        return
    if not isinstance(blue_value, (int, float)):
        return

    red_value = num_range_scale(red_value, 0, 255)
    green_value = num_range_scale(green_value, 0, 255)
    blue_value = num_range_scale(blue_value, 0, 255)
    neurons_request("m_rgb_led_ring", "set_rgb", (0x00, red_value, green_value, blue_value), index)

def off_all(index = 1):
    if not isinstance(index, (int, float)):
        return

    neurons_request("m_rgb_led_ring", "off_all", (), index)

def set_red(led_index, value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return
    
    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 1, 127)

    value = num_range_scale(value, 0, 255)
    neurons_request("m_rgb_led_ring", "set_red", (led_index, value), index)

def set_green(led_index, value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return

    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 1, 127)

    value = num_range_scale(value, 0, 255)
    neurons_request("m_rgb_led_ring", "set_green", (led_index, value), index)

def set_blue(led_index, value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return

    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 1, 127)

    value = num_range_scale(value, 0, 255)
    neurons_request("m_rgb_led_ring", "set_blue", (led_index, value), index)

def change_red(led_index, value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return

    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 1, 127)

    value = num_range_scale(value, -255, 255)
    neurons_request("m_rgb_led_ring", "change_red", (led_index, value), index)

def change_green(led_index, value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return

    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 1, 127)

    value = num_range_scale(value, -255, 255)
    neurons_request("m_rgb_led_ring", "change_green", (led_index, value), index)

def change_blue(led_index, value, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not (isinstance(led_index, (int, float)) or (led_index == "all")):
        return
    if not isinstance(value, (int, float)):
        return

    if led_index == "all":
        led_index = 0
    else:
        led_index = num_range_scale(led_index, 1, 127)

    value = num_range_scale(value, -255, 255)
    neurons_request("m_rgb_led_ring", "change_blue", (led_index, value), index)

def set_mode(mode, index =1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(mode, (str,)):
        return

    if mode == "static":
        mode = 0x00
    elif mode == "marquee":
        mode = 0x03
    elif mode == "breathe":
        mode = 0x04
    else:
        return
    neurons_request("m_rgb_led_ring", "set_mode", (mode), index)
       
def set_block(led_num, data, index = 1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(led_num, (int, float)):
        return
    if not isinstance(data, (list, tuple)):
        return

    list_data = list()
    if led_num <= 0:
        return
    elif led_num < len(data):
        list_data.extend(data[0 : led_num])
    else:
        list_data.extend(data)
        
    neurons_request("m_rgb_led_ring", "set_block", (list_data), index)

def set_effect(mode, speed, data, index = 1):
    if not isinstance(index, (int, float)):
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
    neurons_request("m_rgb_led_ring", "set_mode", (mode), index)
    neurons_request("m_rgb_led_ring", "set_block", (data), index)

def show(color, index = 1):
    if not isinstance(index, (int, float)):
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
        
    neurons_request("m_rgb_led_ring", "set_block", (color), index)