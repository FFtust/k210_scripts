from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

def is_active(ch, index = 1):
    if not isinstance(ch, (int, float)):
        if ch != "any":
            return False
    if not isinstance(index, (int, float)):
        return False
   
    value = neurons_async_read("m_mult_touch", "get_status", (), index)
    if value != None:
        if ch == "any":
            return bool(value[0])
        else:
            ch = round(ch)
            if ch > 8 or ch < 1:
                return False
            return bool(value[0] & (1 << ch - 1))
    else:
        return False

def get_value(position, index = 1):
    if not isinstance(position, (int, float)):
        return 0
    if not isinstance(index, (int, float)):
        return 0
    position = num_range_scale(position, 1, 8)

    value = neurons_async_read("m_mult_touch", "get_value", position, index)
    if value != None:
        return value[0]
    else:
        return 0

def reset_threshold(index = 1):
    if not isinstance(index, (int, float)):
        return
        
    neurons_request("m_mult_touch", "reset", (), index)

def set_sensitivity(sen, index = 1):
    if not isinstance(sen, (int, float)):
        return
    
    if not isinstance(index, (int, float)):
        return
    
    sen = num_range_scale(sen, 1, 4)
    
    neurons_request("m_mult_touch", "reset", (), index)
    neurons_request("m_mult_touch", "set_sensitivity", sen, index)

def set_report_mode(mode,timestamp,index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_mult_touch", "set_report_mode", (mode,timestamp), index)
    else:
        pass

# reserved functions
def get_all_status(index = 1):
    value = neurons_async_read("m_mult_touch", "get_status", (), index)
    if value != None:
        return value[0]
    else:
        return 0x00