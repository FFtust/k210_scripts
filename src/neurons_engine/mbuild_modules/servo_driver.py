from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

__INQUIRE_REPORT_MODE = 0x00
__CHANGE_REPORT_MODE = 0x01
__PERIOD_REPORT_MODE = 0x02

def set_angle(angle, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(angle, (int, float)):
        return

    angle = num_range_scale(angle, 0, 180)
    neurons_request("m_servo", "set_angle", angle, index)

def change_angle(angle, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(angle, (int, float)):
        return

    angle = num_range_scale(angle, -180, 180)
    neurons_request("m_servo", "change_angle", angle, index)

def get_angle(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_blocking_read("m_servo", "get_angle", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def get_load(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_blocking_read("m_servo", "get_load", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def reset(index = 1):
    if not isinstance(index, (int, float)):
        return

    neurons_request("m_servo", "goto_zero", (), index)

def release(index = 1):
    if not isinstance(index, (int, float)):
        return

    neurons_request("m_servo", "release", (), index)


def set_report_mode(mode, timestamp, index = 1):
    if not isinstance(timestamp, (int, float)):
        return

    timestamp = num_range_scale(timestamp, 10, None)
    if mode == __INQUIRE_REPORT_MODE or mode == __CHANGE_REPORT_MODE or mode == __PERIOD_REPORT_MODE:
        neurons_request("m_servo", "set_report_mode", (mode,timestamp), index)
    else:
        return