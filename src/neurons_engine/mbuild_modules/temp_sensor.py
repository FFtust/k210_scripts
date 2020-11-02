from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_is_block_online

def _cal_fahrenheit_from_celsius(value):
    return value * 1.8 + 32
    
def get_temperature(opt = "celsius", index = 1):
    if not isinstance(index, (int, float)):
        return 0
    if opt != "celsius" and opt != "fahrenheit":
        return 0    

    if not neurons_is_block_online("m_temp_sensor", index):
        return 0
        
    value = neurons_async_read("m_temp_sensor", "get_value", (), index)

    if value:
        if opt == "fahrenheit":
            ret = _cal_fahrenheit_from_celsius(value[0])
            return int(ret)
        elif opt == "celsius":
            return int(value[0])
    else:
        return 0

def set_report_mode(mode,timestamp,index = 1):
    timestamp = num_range_scale(timestamp, 10, None)
    if mode == 0x00 or mode == 0x01 or mode == 0x02:
        neurons_request("m_temp_sensor", "set_report_mode", (mode,timestamp), index)
    else:
        pass
