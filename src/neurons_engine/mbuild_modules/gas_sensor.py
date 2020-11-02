from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

GAS_ACTIVITED_THRESOLD = {"high":10, "middle": 20, "low": 50}

def is_active(level = "middle", index = 1):
    if not isinstance(index, (int, float)):
        return False
    if level in GAS_ACTIVITED_THRESOLD:
        thes = GAS_ACTIVITED_THRESOLD[level]
    else:
        thes = GAS_ACTIVITED_THRESOLD["middle"]

    value = neurons_async_read("m_mq2_sensor", "get_value", (), index)
    if value != None:
        return bool(value[0] > thes)
    else:
        return False

def get_value(index = 1):
    if not isinstance(index, (int, float)):
        return 0
        
    value = neurons_async_read("m_mq2_sensor", "get_value", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def set_report_mode(mode,timestamp,index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_mq2_sensor", "set_report_mode", (mode,timestamp), index)
    else:
        pass
