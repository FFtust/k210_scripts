from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read, neurons_get_block_index
import time

def set_power(power, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(power, (int, float)):
        return

    power = num_range_scale(power, -100, 100)
    neurons_request("m_dc_motor", "set_power", power, index)

def set_power_with_time(power, t = 0, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(power, (int, float)):
        return
    if not isinstance(t, (int, float)):
        return

    if t <= 0:
        return
    else:
        power = num_range_scale(power, -100, 100)
        neurons_request("m_dc_motor", "set_power", power, index)
        time.sleep(t)
        neurons_request("m_dc_motor", "set_power", 0, index)

def change_power(power, index = 1):
    if not isinstance(index, (int, float)):
        return

    if not isinstance(power, (int, float)):
        return
    # there is a bug in mbuild dc motor, the type of power is 'byte'
    # can not cover -200 ~ 200, so we use another way to implement that
    #  power = num_range_scale(power, -200, 200)
    #  neurons_request("m_dc_motor", "change_power", power, index)

    cur_power = neurons_blocking_read("m_dc_motor", "get_power", (), index)
    if cur_power:
        power_to = cur_power[0] + power
    else:
        power_to = power

    power_to = num_range_scale(power_to, -100, 100)
    neurons_request("m_dc_motor", "set_power", power_to, index)

def get_power(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    ret = neurons_blocking_read("m_dc_motor", "get_power", (), index)
    if ret:
        return ret[0]
    else:
        return 0

def get_load(index = 1):
    if not isinstance(index, (int, float)):
        return 0

    ret = neurons_blocking_read("m_dc_motor", "get_load", (), index)
    if ret:
        return ret[0]
    else:
        return 0

def stop_all():
    id_list = neurons_get_block_index("m_dc_motor")
    for index in range(len(id_list)):
        neurons_request("m_dc_motor", "set_power", 0, index + 1)

def stop(index = 1):
    if not isinstance(index, (int, float)):
        return

    neurons_request("m_dc_motor", "set_power", 0, int(index))