from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

FLAME_ACTIVE_THRESHOLD = 15

def is_active(index = 1):
    if not isinstance(index, (int, float)):
        return False

    value = neurons_async_read("m_flame", "get_value", (), index)
    if value != None:
        return bool(value[0] > FLAME_ACTIVE_THRESHOLD)
    else:
        return False

def get_value(index = 1):
    if not isinstance(index, (int, float)):
        return 0
        
    value = neurons_async_read("m_flame", "get_value", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def set_report_mode(mode, timestamp, index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_flame", "set_report_mode", (mode,timestamp), index)
    else:
        pass
