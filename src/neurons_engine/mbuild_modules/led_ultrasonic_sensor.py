from common import num_range_scale
from neurons_engine import neurons_request, neurons_async_read ,neurons_blocking_read
import time


def get_distance(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_async_read("m_led_ultrasonic_sensor", "get_centimeter", (), index)
    if value != None:
        return round(value[0], 1)
    else:
        return 0

def set_both_led_bri(bri_1, bri_2 = 0, bri_3 = 0, bri_4 = 0, bri_5 = 0, bri_6 = 0, bri_7 = 0, bri_8 = 0, index = 1):
    if not isinstance(index, (int, float)):
        return
    if isinstance(bri_1,list):
        if len(bri_1) < 8:
            bri_1.extend([0]* (8 - len(bri_1)))
        elif len(bri_1) > 8:
            bri_1 = bri_1[0:8]
        for i in range(8):
            bri_1[i] = num_range_scale(bri_1[i], 0, 100)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", bri_1, index)
    else:
        bri_1 = num_range_scale(bri_1, 0, 100)
        bri_2 = num_range_scale(bri_2, 0, 100)
        bri_3 = num_range_scale(bri_3, 0, 100)
        bri_4 = num_range_scale(bri_4, 0, 100)
        bri_5 = num_range_scale(bri_5, 0, 100)
        bri_6 = num_range_scale(bri_6, 0, 100)
        bri_7 = num_range_scale(bri_7, 0, 100)
        bri_8 = num_range_scale(bri_8, 0, 100)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (bri_1, bri_2, bri_3, bri_4, bri_5, bri_6, bri_7, bri_8), index)

def set_single_led_bri(led_bri, led_index, index = 1):
    if not isinstance(index, (int, float)):
        return
    led_bri = num_range_scale(led_bri, 0, 100)
    if led_index not in [1, 2, 3, 4, 5, 6, 7, 8, "ALL", "all"]:
        return
    if led_index == "ALL" or "all":
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (led_bri, ) * 8, index)
    else:
        led_arr = [-1] * 8
        led_arr[led_index - 1] = led_bri
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", led_arr, index)

def change_led_bri(led_bri, led_index, index = 1):
    if not isinstance(index, (int, float)):
        return
    led_bri = num_range_scale(led_bri, -100, 100)
    if led_index not in [1, 2, 3, 4, 5, 6, 7, 8, "ALL", "all"]:
        return
    if led_index == "ALL" or "all":
        neurons_request("m_led_ultrasonic_sensor", "change_led_bri", (led_bri, ) * 8, index)
    else:
        led_arr = [0] * 8
        led_arr[led_index - 1] = led_bri
        neurons_request("m_led_ultrasonic_sensor", "change_led_bri", led_arr, index)

def get_led_bri(led_index, index = 1):
    if not isinstance(index, (int, float)):
        return 0
    if led_index not in [1, 2, 3, 4, 5, 6, 7, 8]:
        return
    value = neurons_blocking_read("m_led_ultrasonic_sensor", "get_led_bri", (), index)
    if value != None:
        return value[led_index - 1]
    else:
        return 0

def happy_effect(led_bri, index):
    led_arr = [0, led_bri, led_bri, 0, 0, led_bri, led_bri, 0]
    for count in range(3):
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", led_arr, index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, ) * 8, index)
        time.sleep(0.25)

def wink_effect(led_bri, index):
    led_arr = [led_bri] * 8
    for count in range(3):
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", led_arr, index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, ) * 8, index)
        time.sleep(0.25)

def naughty_effect(led_bri, index):
    for count in range(3):
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, ) * 8, index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (led_bri, 0, 0, 0, led_bri, 0, 0, 0), index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, led_bri, 0, 0, 0, led_bri, 0, 0), index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, 0, led_bri, 0, 0, 0, led_bri, 0), index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, 0, 0, led_bri, 0, 0, 0, led_bri), index)
        time.sleep(0.25)

def aggrieved_effect(led_bri, index):
    for count in range(3):
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (led_bri, 0, 0, led_bri, led_bri, 0, 0, led_bri), index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, ) * 8, index)
        time.sleep(0.25)

def  look_left_effect(led_bri, index):
    for count in range(3):
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (led_bri, led_bri, 0, 0, led_bri, led_bri, 0, 0), index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, ) * 8, index)
        time.sleep(0.25)

def look_right_effect(led_bri, index):
    for count in range(3):
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, 0, led_bri, led_bri, 0, 0, led_bri, led_bri), index)
        time.sleep(0.25)
        neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, ) * 8, index)
        time.sleep(0.25)

def eye_left_effect(led_bri, index):
    neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (led_bri, led_bri, led_bri, led_bri, 0, 0, 0, 0), index)

def  eye_right_effect(led_bri, index):
    neurons_request("m_led_ultrasonic_sensor", "set_led_bri", (0, 0, 0, 0, led_bri, led_bri, led_bri, led_bri), index)
    
def show_led_emotion(led_bri, name = "happy", index = 1):
    if name == 'happy':
        happy_effect(led_bri, index)
    elif name == 'wink':
        wink_effect(led_bri, index)
    elif name == 'naughty':
        naughty_effect(led_bri, index)
    elif name == 'aggrieved':
        aggrieved_effect(led_bri, index)
    elif name == 'look_left':
        look_left_effect(led_bri, index)
    elif name == 'look_right':
        look_right_effect(led_bri, index)
    elif name == 'eye_left':
        eye_left_effect(led_bri, index)
    elif name == 'eye_right':
        eye_right_effect(led_bri, index)
    else:
        return

def set_report_mode(mode, timestamp, index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_led_ultrasonic_sensor", "set_report_mode", (mode, timestamp), index)
    else:
        pass

get = get_distance
set_bri = set_single_led_bri
add_bri = change_led_bri
get_bri = get_led_bri
led_show = set_both_led_bri