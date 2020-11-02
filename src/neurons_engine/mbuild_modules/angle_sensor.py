from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

CLOCKWISE_VALUE = 0x01
ANTICLOCKWISE_VALUE = 0x02

def get_angle(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_async_read("m_angle_sensor", "get_angle", (), index)
    if value != None:
        return value[0]
    else:
        return 0

def get_angle_speed(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    value = neurons_blocking_read("m_angle_sensor", "get_angle_speed", (), index)
    if value != None:
        return value[0]
    else:
        return 0
        
def is_rotating_clockwise(index = 1):
    if not isinstance(index, (int, float)):
        return False
        
    value = neurons_blocking_read("m_angle_sensor", "get_dir", (), index)
    if value[0] == CLOCKWISE_VALUE:
        return True
    else:
        return False

def is_rotating_anticlockwise(index = 1):
    if not isinstance(index, (int, float)):
        return False
        
    value = neurons_blocking_read("m_angle_sensor", "get_dir", (), index)
    if value[0] == ANTICLOCKWISE_VALUE:
        return True
    else:
        return False

def reset_angle(index = 1):
    if not isinstance(index, (int, float)):
        return None
        
    neurons_request("m_angle_sensor", "reset", (), index)

def set_report_mode(mode,timestamp,index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_angle_sensor", "set_report_mode", (mode,timestamp), index)
    else:
        pass
