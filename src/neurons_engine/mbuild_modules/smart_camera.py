from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_is_block_online
import time

CAMERA_FRAME_WIDTH = 320
CAMERA_FRAME_HIGHT = 240
# WARNNING :
# for high level application, the camera frame size should be
# set to 320 * 240, but the size read from camara module is not 320 * 240
# the true zise is:
# color block mode: 316 * 208
# line mode: 80 * 53
FRAME_REVISE_COE_COLOR_BLOCK_X = 1.013  # 320 / 316
FRAME_REVISE_COE_COLOR_BLOCK_Y = 1.154  # 240 / 208
FRAME_REVISE_COE_LINE_X = 4  # 320 / 80
FRAME_REVISE_COE_LINE_Y = 4.528  # 240 / 53

__INQUIRE_REPORT_MODE = 0x00
__CHANGE_REPORT_MODE = 0x01
__PERIOD_REPORT_MODE = 0x02

POSITION_CHECK_THRESHOLD = 10

# global
__kp = [0.5, 0.5, 0.5, 0.5]
__mode = ["", "", "", ""]

# private function
def get_fills_all_data(fills_id, index = 1):# 获取某个色块所有信息
    if (not isinstance(fills_id, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    fills_id = num_range_scale(fills_id, 1, 7)
    fills_id -= 1
    value = neurons_blocking_read("m_smart_camera", "get_fills_all_data", (int(fills_id)), int(index))
    if value != None:
        value[1] = round(value[1] * FRAME_REVISE_COE_COLOR_BLOCK_X)
        value[2] = round(value[2] * FRAME_REVISE_COE_COLOR_BLOCK_Y)
        value[3] = round(value[3] * FRAME_REVISE_COE_COLOR_BLOCK_X)
        value[4] = round(value[4] * FRAME_REVISE_COE_COLOR_BLOCK_Y)
        return value
    else:
        return 0

def set_fills_report_mode(mode, timestamp, index = 1):# 设置某个色块所有信息的上报模式
    if (not isinstance(timestamp, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smart_camera", "set_fills_report_mode", (mode,timestamp), index)
    else:
        return

def get_fills_sigle_data(fills_id, type_id, index = 1):# 获取某个色块的单独的信息
    if (not isinstance(fills_id, (int, float))) or (not isinstance(type_id, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    fills_id = num_range_scale(fills_id, 1, 7)
    fills_id -= 1

    if type_id == 0x00 or type_id == 0x01 or type_id == 0x02 or type_id == 0x03:
        value = neurons_blocking_read("m_smart_camera", "get_fills_sigle_data", (fills_id,type_id), index)
        if value != None:
            if type_id == 0x00 or type_id == 0x02:
                value[2] = round(value[2] * FRAME_REVISE_COE_COLOR_BLOCK_X)
            else:
                value[2] = round(value[2] * FRAME_REVISE_COE_COLOR_BLOCK_Y)
            return value
    else:
        return 0

def get_line_all_data(index = 1):#获取线的所有信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_line_all_data", (), index)
    if value != None:
        value[0] = round(value[0] * FRAME_REVISE_COE_LINE_X)
        value[1] = round(value[1] * FRAME_REVISE_COE_LINE_Y)
        value[2] = round(value[2] * FRAME_REVISE_COE_LINE_X)
        value[3] = round(value[3] * FRAME_REVISE_COE_LINE_Y)
        return value
    else:
        return 0

def set_line_report_mode(mode, timestamp, index = 1):#设置线所有信息的上报模式
    if (not isinstance(timestamp, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smart_camera", "set_line_report_mode", (mode,timestamp), index)
    else:
        return

def get_line_sigle_data(type_id, index = 1):#获取线的单独的信息
    if (not isinstance(type_id, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0

    if type_id == 0x00 or type_id == 0x01 or type_id == 0x02 or type_id == 0x03:
        value = neurons_blocking_read("m_smart_camera", "get_line_sigle_data", (type_id), index)
        if value != None:
            if type_id == 0x00 or type_id == 0x02:
                value[1] = round(value[1] * FRAME_REVISE_COE_LINE_X)
            else:
                value[1] = round(value[1] * FRAME_REVISE_COE_LINE_Y)
            return value
    return 0

def get_crossings_all_data(index = 1):#获交叉口的所有信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_crossings_all_data", (), index)
    if value != None:
        value[0] = round(value[0] * FRAME_REVISE_COE_LINE_X)
        value[1] = round(value[1] * FRAME_REVISE_COE_LINE_Y)
        return value
    else:
        return 0

def set_crossings_report_mode(mode, timestamp, index = 1):#设置交叉口的所有信息的上报模式
    if (not isinstance(timestamp, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smart_camera", "set_crossings_report_mode", (mode,timestamp), index)
    else:
        return

def get_crossings_sigle_data(type_id, index = 1):#获取交叉口的单独的信息
    if (not isinstance(type_id, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0

    if type_id == 0x06 or type_id == 0x07 or type_id == 0x08:
        value = neurons_blocking_read("m_smart_camera", "get_crossings_sigle_data", (type_id), index)
        if value != None:
            if type_id == 0x06:
                value[1] = round(value[1] * FRAME_REVISE_COE_LINE_X)
            elif type_id == 0x07:
                value[1] = round(value[1] * FRAME_REVISE_COE_LINE_Y)           
            return value
    else:
        return 0

def get_crossings_line_angle_sigle_data(index = 1):#获取交叉口线角度的单独的信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_crossings_line_angle_sigle_data", (), index)
    if value != None:
        return value
    else:
        return 0

def get_barcode_all_data(barcode_id, index = 1):#获取某个条形码的所有信息
    if (not isinstance(barcode_id, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    barcode_id = num_range_scale(barcode_id, 0, 15)
    value = neurons_blocking_read("m_smart_camera", "get_barcode_all_data", (barcode_id), index)
    if value != None:
        value[1] = round(value[1] * FRAME_REVISE_COE_LINE_X)
        value[2] = round(value[2] * FRAME_REVISE_COE_LINE_Y)
        return value
    else:
        return 0

def set_barcode_report_mode(mode, timestamp, index = 1):#设置某个条形码的所有信息的上报模式
    if (not isinstance(timestamp, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smart_camera", "set_barcode_report_mode", (mode,timestamp), index)
    else:
        return

def get_barcode_sigle_data(barcode_id, type_id, index = 1):#获取条形码X的单独的信息
    if (not isinstance(barcode_id, (int, float))) or (not isinstance(type_id, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    barcode_id = num_range_scale(barcode_id, 0, 15)

    if type_id == 0x0b or type_id == 0x0c:
        value = neurons_blocking_read("m_smart_camera", "get_barcode_sigle_data", (barcode_id,type_id), index)
        if value != None:
            if type_id == 0x0b:
                value[2] = round(value[2] * FRAME_REVISE_COE_LINE_X)
            else:
                value[2] = round(value[2] * FRAME_REVISE_COE_LINE_Y)
            return value
    else:
        return 0

def get_button_data(index = 1):#获取按键的信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_button_data", (), index)
    if value != None:
        return value
    else:
        return 0

def set_button_report_mode(mode, timestamp, index = 1):#设置按键信息的上报模式
    if (not isinstance(timestamp, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_smart_camera", "set_button_report_mode", (mode,timestamp), index)
    else:
        return

def get_learn_data(index = 1):#获取学习的信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_learn_data", (), index)
    if value != None:
        return value
    else:
        return 0

def set_camera_sensitometry(level, index = 1):#设置摄像头曝光度
    if (not isinstance(level, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    level = num_range_scale(level, 0, 255)
    neurons_request("m_smart_camera", "set_camera_sensitometry", (level), index)

def set_led_rgb(r, g, b, index = 1):#设置RGB灯
    if (not isinstance(r, (int, float))) or (not isinstance(g, (int, float))) or (not isinstance(b, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    r = num_range_scale(r, 0, 255)
    g = num_range_scale(g, 0, 255)
    b = num_range_scale(b, 0, 255)
    neurons_request("m_smart_camera", "set_led_rgb", (r,g,b), index)

def set_fill_light_status(sta, index = 1):#设置补光灯状态
    if sta == 0x00 or sta == 0x01:
        neurons_request("m_smart_camera", "set_fill_light_status", (sta), index)
    else:
        return

def set_line_follow_vector_mode(mode, index = 1):#设置巡线vector模式（不开放）
    if mode == 0x00 or mode == 0x01:
        neurons_request("m_smart_camera", "set_line_follow_vector_mode", (mode), index)
    else:
        return

def set_line_follow_mode(mode, index = 1):#设置巡线模式
    if mode == 0x00 or mode == 0x01:
        neurons_request("m_smart_camera", "set_line_follow_mode", (mode), index)
    else:
        return

def get_turning_angle(index = 1):#获取按键的信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_turning_angle", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def get_fills_count(index = 1):#获取按键的信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_fills_count", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def get_barcode_count(index = 1):#获取按键的信息
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0
    value = neurons_blocking_read("m_smart_camera", "get_barcode_count", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def set_next_turning_angle(angle, index = 1):#设置下一次转向角度
    if (not isinstance(angle, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    angle = num_range_scale(angle, -180, 180)
    neurons_request("m_smart_camera", "set_next_turning_angle", (angle), index)

def set_default_turning_angle(angle, index = 1):#设置默认的转向角度（不开放）
    if (not isinstance(angle, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return
    angle = num_range_scale(angle, -180, 180)
    neurons_request("m_smart_camera", "set_default_turning_angle", (angle), index)

def set_fills_learn_mode(fills_id, t, index = 1):#设置学习色块模式
    if (not isinstance(fills_id, (int, float))) or (not isinstance(t, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return

    # real index is 0 ~ 7
    fills_id = num_range_scale(fills_id, 1, 8)
    fills_id -= 1

    t = num_range_scale(t, 0, None)
    neurons_request("m_smart_camera", "set_fills_learn_mode", (fills_id,t), index)

def stop_learn(index = 1):#设置结束学习（不开放）
    if (not isinstance(index, (int, float))) or (index <= 0):
        return
    neurons_request("m_smart_camera", "stop_learn", (), index)

def abandon_learn(index = 1):#设置放弃学习（不开放）
    if (not isinstance(index, (int, float))) or (index <= 0):
        return
    neurons_request("m_smart_camera", "abandon_learn", (), index)

def set_pixy_mode(mode, index = 1):#设置pixy模块模式
    if (not isinstance(index, (int, float))) or (index <= 0):
        return
    if mode == 0x01 or mode == 0x02 or mode == 0x03:
        neurons_request("m_smart_camera", "set_pixy_mode", (mode), index)

# function for building block
def set_mode(mode = "color", index = 1):
    global __mode
    if mode == "color":
        set_pixy_mode(0x01, index)
        __mode[index-1] = mode
    elif mode == "line":
        set_pixy_mode(0x02, index)
        __mode[index-1] = mode
    elif mode == "video":
        set_pixy_mode(0x03, index)
        __mode[index-1] = mode
    else:
        pass

def learn(sign = 1, t = "until_button", index = 1):
    if t == "until_button":
        # wait button pressed or module offline
        t = 0
        set_fills_learn_mode(sign, t, index)
        if not neurons_is_block_online("m_smart_camera", index):
            return
        time.sleep(0.1)
        # [0]: idle [1]: learnning
        while get_learn_data(index) == [1]:
            if not neurons_is_block_online("m_smart_camera", index):
                return        
            time.sleep(0.1)

        # reserve more time (2s) for value ready
        time.sleep(2)
    elif isinstance(t, (int, float)):
        if t <= 0:
            return
        set_fills_learn_mode(sign, t, index)
        # reserve more time (2s) for value ready
        time.sleep(sign + t + 2)

def detect_sign(sign, index = 1):
    value = get_fills_all_data(sign, index)
    # print(value)
    if value != 0:
        if value[1] != 0 or value[2] != 0 or value[3] != 0 or value[4] != 0:
            return True
        return False
    else:
        return False

def get_sign_x(sign, index = 1):
    value = get_fills_sigle_data(sign, 0x00, index)
    if value != 0:
        return value[2]
    return 0

def get_sign_y(sign, index = 1):
    value = get_fills_sigle_data(sign, 0x01, index)
    if value != 0:
        return value[2]
    return 0

def get_sign_wide(sign, index = 1):
    value = get_fills_sigle_data(sign, 0x02, index)
    if value != 0:
        return value[2]
    return 0

def get_sign_hight(sign, index = 1):
    value = get_fills_sigle_data(sign, 0x03, index)
    if value != 0:
        return value[2]
    return 0

def detect_sign_location(sign, location, index = 1):
    x = get_sign_x(sign, index)
    y = get_sign_y(sign, index)
    
    # not found
    if x == 0 and y == 0:
        return False

    if __caculate_sign_location(x, y) == location:
        return True
    else:
        return False

def get_sign_location(sign, index = 1):
    x = get_sign_x(sign, index)
    y = get_sign_y(sign, index)
    
    if x == 0 and y == 0:
        return "None"

    return __caculate_sign_location(x, y)

def __caculate_sign_location(x, y):
    MIDDLE_WIDTH = 60
    MIDDLE_HIGHT = 40
    
    # CAMERA_FRAME_WIDTH = 320
    # CAMERA_FRAME_HIGHT = 240
    
    # two lines
    # y = (240 / 320) * x ===> y = 0.75 * x
    # y = -(240 / 320) * x + 240 ===> y = -0.75 * x + 240
    def _line1_check(x, y):
        return 0.75 * x - y

    def _line2_check(x, y):
        return -0.75 * x + 240 - y

    if((CAMERA_FRAME_WIDTH - MIDDLE_WIDTH) / 2 < x) and (x < (CAMERA_FRAME_WIDTH + MIDDLE_WIDTH) / 2) and \
      ((CAMERA_FRAME_HIGHT - MIDDLE_HIGHT) / 2 < y) and (y < (CAMERA_FRAME_HIGHT + MIDDLE_HIGHT) / 2):
        return "middle"
    elif _line1_check(x, y) >= 0 and _line2_check(x, y) >= 0 :
        return "up"
    elif _line1_check(x, y) < 0 and _line2_check(x, y) < 0:
        return "down"
    elif _line1_check(x, y) >= 0 and _line2_check(x, y) <= 0:
        return "right"
    elif _line1_check(x, y) < 0 and _line2_check(x, y) > 0:
        return "left"

def open_light(index = 1):
    set_fill_light_status(0x01, index)

def close_light(index = 1):
    set_fill_light_status(0x00, index)

def reset(index = 1):
    set_fills_learn_mode(0x08, 1, index)#白平衡

def detect_label(label, index = 1):
    value = get_barcode_all_data(label, index)
    if value != 0:
        if value[1] != 0 or value[2] != 0:
            return True
        return False
    else:
        return False

def get_label_x(sign, index = 1):
    value = get_barcode_sigle_data(sign, 0x0b, index)
    if value != 0:
        return value[2]
    return 0

def get_label_y(sign, index = 1):
    value = get_barcode_sigle_data(sign, 0x0c, index)
    if value != 0:
        return value[2]
    return 0

def get_vector_end_x(index = 1):#line -> vector
    value = get_line_sigle_data(0x02, index)
    if value != 0:
        return value[1]
    return 0

def get_vector_end_y(index = 1):
    value = get_line_sigle_data(0x03, index)
    if value != 0:
        return value[1]
    return 0

def get_vector_start_x(index = 1):
    value = get_line_sigle_data(0x00, index)
    if value != 0:
        return value[1]
    return 0
    
def get_vector_start_y(index = 1):
    value = get_line_sigle_data(0x01, index)
    if value != 0:
        return value[1]
    return 0

def detect_cross(index = 1):
    value = get_crossings_all_data(index)
    if value != 0:
        if value[0] != 0 or value[1] != 0:
            return True
        else:
            return False
    else:
        return False

def get_cross_x(index = 1):
    value = get_crossings_sigle_data(0x06, index)
    if value != 0:
        return value[1]
    return 0

def get_cross_y(index = 1):
    value = get_crossings_sigle_data(0x07, index)
    if value != 0:
        return value[1]
    return 0

def get_cross_road(index = 1):#获取交叉口数目？
    value = get_crossings_sigle_data(0x08, index)
    if value != 0:
        return value[1]
    return 0

def get_cross_angle(sn = 1, index = 1):
    if (not isinstance(sn, (int, float))) or (sn <= 0):
        return 0
    sn = int(sn)
    sn = num_range_scale(sn, 1, 6)
    value = get_crossings_line_angle_sigle_data(index)
    if value != 0:
        return value[sn-1]
    return 0

def set_line(mode = "black", index = 1):
    if mode == "black":
        set_line_follow_mode(0, index)
    elif mode == "white":
        set_line_follow_mode(1, index)

def set_vector_angle(angle, index = 1):
    set_next_turning_angle(angle, index)

def get_vector_angle(index = 1):
    value = get_turning_angle(index)
    if value != 0:
        return value
    return 0

#competition function for building block
def set_kp(kp, index = 1):
    global __kp
    if (not isinstance(kp, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return

    index = int(index)

    if kp < 0:
        __kp[index-1] = 0
    elif kp > 1:
        __kp[index-1] = 1
    else:
        __kp[index-1] = kp

def get_fills_diff_speed(sign, tar_x, tar_y, index = 1):
    global __kp, __mode
    if (not isinstance(tar_x, (int, float))) or (not isinstance(tar_y, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0

    index = int(index)

    if __mode[index-1] != "color":
        return 0

    data = get_fills_all_data(sign, index)
    if data == 0:
        return 0
    cur_x = data[1]
    cur_y = data[2]

    if cur_x == 0 or cur_y == 0:
        return 0

    error = 0
    if tar_x == -1:
        error = (tar_y - cur_y) * 2
    elif tar_y == -1:
        error = (cur_x - tar_x) * 1
    else:
        return 0

    error = num_range_scale(error, -100, 100)
    error = error * __kp[index - 1]
    return error

def get_sign_diff_speed_x(sign, tar_x, index = 1):
    return get_fills_diff_speed(sign, tar_x, -1, index)

def get_sign_diff_speed_y(sign, tar_y, index = 1):
    return get_fills_diff_speed(sign, -1, tar_y, index)

def get_sign_diff_speed(sign, axis = "x", axis_val = 0, index = 1):
    if axis == "x":
        return get_sign_diff_speed_x(sign, axis_val, index)
    elif axis == "y":
        return get_sign_diff_speed_y(sign, axis_val, index)
    return 0

def get_barcode_diff_speed(label, tar_x, tar_y, index = 1):
    global __kp, __mode
    if (not isinstance(tar_x, (int, float))) or (not isinstance(tar_y, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return 0

    index = int(index)

    if __mode[index-1] != "line":
        return 0

    data = get_barcode_all_data(label, index)
    if data == 0:
        return 0
    cur_x = data[1]
    cur_y = data[2]
    # print("cur x y:", cur_x, cur_y)
    if cur_x == 0 or cur_y == 0:
        return 0

    error = 0
    if tar_x == -1:
        error = (tar_y - cur_y) * 3
    elif tar_y == -1:
        error = (cur_x - tar_x) * 3
    else:
        return 0

    error = num_range_scale(error, -100, 100)
    error = error * __kp[index-1]
    return error

def get_label_diff_speed_x(label, tar_x, index = 1):
    return get_barcode_diff_speed(label, tar_x, -1, index)

def get_label_diff_speed_y(label, tar_y, index = 1):
    return get_barcode_diff_speed(label, -1, tar_y, index)

def get_label_diff_speed(label, axis = "x", axis_val = 0, index = 1):
    if axis == "x":
        return get_label_diff_speed_x(label, axis_val, index)
    elif axis == "y":
        return get_label_diff_speed_y(label, axis_val, index)
    return 0

def get_follow_vector_diff_speed(index = 1):
    global __mode
    if (not isinstance(index, (int, float))) or (index <= 0):
        return 0

    index = int(index)

    if __mode[index-1] != "line":
        return 0

    data = get_line_all_data(index)
    if data == 0:
        return 0
    cur_x0 = data[0]
    cur_y0 = data[1]
    cur_x1 = data[2]
    cur_y1 = data[3]
    # print("end_x start_x:", cur_x0, cur_x1)
    if cur_x0 == 0 or cur_x1 == 0:
        return 0

    error = (cur_x0 - CAMERA_FRAME_WIDTH / 2) * 0.7 + (cur_x1 - CAMERA_FRAME_WIDTH / 2) * 0.3
    error = 3 * error
    error = num_range_scale(error, -100, 100)
    error = error * __kp[index-1]
    return error

def is_lock_fills(sign, tar_x, tar_y, index = 1):
    global __mode

    if (not isinstance(tar_x, (int, float))) or (not isinstance(tar_y, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return False

    index = int(index)

    if __mode[index-1] != "color":
        return False

    data = get_fills_all_data(sign, index)
    if data == 0:
        return False
    cur_x = data[1]
    cur_y = data[2]
    # print("cur x y:", cur_x, cur_y)
    if cur_x == 0 or cur_y == 0:
        return False

    if tar_x == -1 :
        if abs(tar_y - cur_y) < POSITION_CHECK_THRESHOLD:
            return True
    elif tar_y == -1 :
        if abs(cur_x - tar_x) < POSITION_CHECK_THRESHOLD:
            return True
    else:
        if abs(tar_y - cur_y) < POSITION_CHECK_THRESHOLD and abs(cur_x - tar_x) < POSITION_CHECK_THRESHOLD:
            return True
    return False

def is_lock_sign_x(sign, tar_x, index = 1):
    if tar_x == -1:
        return False
    return is_lock_fills(sign, tar_x, -1, index)

def is_lock_sign_y(sign, tar_y, index = 1):
    return is_lock_fills(sign, -1, tar_y, index)

def is_lock_sign(sign, axis = "x", axis_val = 0, index = 1):
    if axis == "x":
        return is_lock_sign_x(sign, axis_val, index)
    elif axis == "y":
        return is_lock_sign_y(sign, axis_val, index)
    return False

def is_lock_barcode(label, tar_x, tar_y, index = 1):
    global __mode
    if (not isinstance(tar_x, (int, float))) or (not isinstance(tar_y, (int, float))) or (not isinstance(index, (int, float))) or (index <= 0):
        return False

    index = int(index)

    if __mode[index-1] != "line":
        return False

    data = get_barcode_all_data(label, index)
    if data == 0:
        return False
    cur_x = data[1]
    cur_y = data[2]

    if cur_x == 0 or cur_y == 0:
        return False

    if tar_x == -1:
        if abs(tar_y - cur_y) < POSITION_CHECK_THRESHOLD:
            return True
    elif tar_y == -1:
        if abs(cur_x - tar_x) < POSITION_CHECK_THRESHOLD:
            return True
    else:
        if abs(tar_y - cur_y) < POSITION_CHECK_THRESHOLD and abs(cur_x - tar_x) < POSITION_CHECK_THRESHOLD:
            return True
    return False

def is_lock_label_x(label, tar_x, index = 1):
    if tar_x == -1:
        return False
    return is_lock_barcode(label, tar_x, -1, index)

def is_lock_label_y(label, tar_y, index = 1):
    return is_lock_barcode(label, -1, tar_y, index)

def is_lock_label(label, axis = "x", axis_val = 0, index = 1):
    if axis == "x":
        return is_lock_label_x(label, axis_val, index)
    elif axis == "y":
        return is_lock_label_y(label, axis_val, index)
    return False