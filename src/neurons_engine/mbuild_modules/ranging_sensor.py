from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read
    
def get_distance(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_async_read("m_ranging_sensor", "get_value", (), index)
    if value != None:
        return round(value[0], 1)
    else:
        return 0

def set_report_mode(mode, timestamp, index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_ranging_sensor", "set_report_mode", (mode, timestamp), index)
    else:
        pass
