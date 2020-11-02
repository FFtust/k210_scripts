from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

ACTIVE_THRESHOLD = 30

def get_value(opt, index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_async_read("m_joystick", "get_value", (), index)

    if value:
        if opt == 'x':
            return value[0]
        elif opt == 'y':
            return value[1]
        elif opt == 'all':
            return value

    else:
        if opt == 'all':
            return [0, 0]
        elif opt == 'y':
            return 0

    return 0

def is_active(opt, index = 1):
    value = get_value("all", index)
    if opt == "up":
        return bool(value[1] > ACTIVE_THRESHOLD)
    elif opt == "down":
        return bool(value[1] < -ACTIVE_THRESHOLD)
    elif opt == "left":
        return bool(value[0] < -ACTIVE_THRESHOLD)
    elif opt == "right":
        return bool(value[0] > ACTIVE_THRESHOLD)
    else:
        return False

def set_report_mode(mode,timestamp,index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_joystick", "set_report_mode", (mode,timestamp), index)
    else:
        pass


def is_up(index = 1):
    value = get_value("all", index)
    return bool(value[1] > ACTIVE_THRESHOLD)

def is_down(index = 1):
    value = get_value("all", index)
    return bool(value[1] < -ACTIVE_THRESHOLD)

def is_left(index = 1):
    value = get_value("all", index)
    return bool(value[0] < -ACTIVE_THRESHOLD)

def is_right(index = 1):
    value = get_value("all", index)
    return bool(value[0] > ACTIVE_THRESHOLD)