from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read

#channel dictionary
channel_dict = {
    "M1": 0x00,
    "M2": 0x01,
}

def run(left_speed, right_speed, index = 1):#rpm
    if not isinstance(index, (int, float)):
        return
    if not isinstance(left_speed, (int, float)):
        return

    neurons_request("m_mbot", "run", (left_speed, right_speed), index)

def set_power(channel = None, power =0, index = 1):
    if index != 0x01:
        return
    if channel != "ALL" and channel != "M1" and channel != "M2":
        return
    if not isinstance(power, (int,float)):
        return
    power = int(power)
    power = num_range_scale(power, -100, 100)

    print("set_power")
    neurons_request("m_mbot", "set_pwm", (channel_dict[channel], power), index)
