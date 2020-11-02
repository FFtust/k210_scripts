from common import num_range_scale, run_safe
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_is_block_online
import re
import time
import binascii
import math

COLUMN_ID_MAX = 15
LINE_ID_MAX = 7 

image_table = \
{
"normal": "00003c7e7e3c000000003c7e7e3c0000",
"hello": "00003c7e7e3c000000003c7e7e3c0000",
"laugh": "00103030303010000010303030301000",
"sad": "000207070f0e080000080e0f07070200",
"sprint": "0c0e0e060602020000020206060e0e0c",
"happy": "000c18181c0c000000000c1c18180c00",
"sleepy": "0000181c1c1800000000181c1c180000",
"angry": "00003c1e0e0400000000040e1e3c0000",
"wrong": "0000363e1c3e360000363e1c3e360000",
"cool": "103c3e3e3e3e3c10103c3e3e3e3e3c10",
"surprised": "003c4242423c000000003c4242423c00",
}

def _sting_to_bytes(string):
    hex_data = binascii.unhexlify(string)
    return hex_data

def _get_image(image_string):
    if image_string in image_table:
       image_string = image_table[image_string]

    temp_list = [0] * 16
    if len(image_string) < 32:  # 16 *2
        image_string = image_string + '0' * (32- len(image_string))
    if len(image_string) > 32:  # 16 *2
        image_string = image_string[0:32]
        
    return tuple(_sting_to_bytes(image_string))

#######################################################################################
@run_safe
def show_image(image, pos_x = 0, pos_y = 0, time_s = None, index = 1):
    if not isinstance(index, (int, float)):
        return
    if (not isinstance(pos_x, (int, float))) or (not isinstance(pos_y, (int, float))):
        return
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    if pos_x > 15 or pos_x < -15 or pos_y > 7 or  pos_y < -7:
        clear()
        
    temp_list = [0] * 16
    show_list = [0] * 16

    if isinstance(image, list):
        for i in range(len(image) if len(image) < 16 else 16):
            temp_list[i] = image[i]

    elif isinstance(image, str):
        temp_list = _get_image(image)

    else:
        return
    
    if pos_x >= 0:
        for i in range(pos_x):
            show_list[i] = 0x00
        for i in range(16 - pos_x):
            if pos_y > 0:
                show_list[pos_x + i] = temp_list[i] >> pos_y
            else:
                show_list[pos_x + i] = temp_list[i] << -pos_y
            show_list[pos_x + i] &= 0xff 
    else:
        for i in range(-pos_x):
            show_list[-i + 15] = 0x00
        for i in range(16 + pos_x):
            if pos_y > 0:
                show_list[i] = temp_list[i - pos_x] >> pos_y
            else:
                show_list[i] = temp_list[i - pos_x] << -pos_y
            show_list[pos_x + i] &= 0xff      

    if time_s == None:
        neurons_request("m_led_panel", "show_image", show_list, index)
    elif isinstance(time_s, (int, float)):
        if time_s <= 0:
            return
        neurons_request("m_led_panel", "show_image", show_list, index)
        time.sleep(time_s)
        clear()

def show(message, pos_x = None, pos_y = None, wait = True, index = 1):
    if not isinstance(index, (int, float)):
        return 0

    message = str(message)
    if message == '':
        clear()
        return

    str_len = len(message)
    if pos_x != None or pos_y != None:
        if pos_x == None:
            pos_x = 0
        if pos_y == None:
            pos_y = 0

        if (not isinstance(pos_x, (int, float))) or (not isinstance(pos_y, (int, float))):
            return
        pos_x = int(pos_x)
        pos_y = int(pos_y)
        neurons_request("m_led_panel", "show_str_with_pos", (pos_x, pos_y, message), index)
    else:       
        if wait:
            neurons_request("m_led_panel", "show_str_until_done", message, index) 
            while neurons_blocking_read("m_led_panel", "get_status", (), index) != [1]:
                if not neurons_is_block_online("m_led_panel", index):
                    return
                time.sleep(0.1)
        else:
            neurons_request("m_led_panel", "show_str", message, index)
             
def set_pixel(pos_x, pos_y, status, index = 1):
    if not isinstance(index, (int, float)):
        return
    if (not isinstance(pos_x, (int, float))) or (not isinstance(pos_y, (int, float))):
        return
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    if pos_x < 0 or pos_x > 15 or pos_y < 0 or pos_y > 7:
        return  
    if status:
        neurons_request("m_led_panel", "show_pixel", (pos_x, pos_y, 1), index)
    else:
        neurons_request("m_led_panel", "show_pixel", (pos_x, pos_y, 0), index)

def get_pixel(pos_x, pos_y, index = 1):
    if not isinstance(index, (int, float)):
        return False

    if (not isinstance(pos_x, (int, float))) or (not isinstance(pos_y, (int, float))):
        return False
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    if pos_x < 0 or pos_x > 15 or pos_y < 0 or pos_y > 7:
        return  False
    ret = neurons_blocking_read("m_led_panel", "get_pixel", (pos_x, pos_y), index)
    return bool(ret[2])

def toggle_pixel(pos_x, pos_y, index = 1):
    if not isinstance(index, (int, float)):
        return

    if (not isinstance(pos_x, (int, float))) or (not isinstance(pos_y, (int, float))):
        return
    pos_x = int(pos_x)
    pos_y = int(pos_y)
    if pos_x < 0 or pos_x > 15 or pos_y < 0 or pos_y > 7:
        return  
    neurons_request("m_led_panel", "toggle_pixel2", (pos_x, pos_y, 0), index)

def clear(index = 1):
    neurons_request("m_led_panel", "clear", (), index)
