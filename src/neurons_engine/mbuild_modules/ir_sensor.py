from common import num_range_scale
from neurons_engine import neurons_request, neurons_blocking_read, neurons_async_read
import time

RECEIVING_INTERVAL_THRESHOLD = 110

RECORD_TIME = 3000
last_receing_time = 0

def receive(index = 1):
    global last_receing_time

    if not isinstance(index, (int, float)):
        return ""

    value = neurons_async_read("m_ir_sensor", "read_str", (), index, request_first = False)
    # ir sensor is processed specially
    if len(value) == 1:
        return ""
    else:
        if (last_receing_time != value[-1]) and (time.ticks_ms() - value[-1] < RECEIVING_INTERVAL_THRESHOLD):
            last_receing_time = value[-1]
            return value[0]
        else:
            return ""

def send(message, index = 1):
    if not isinstance(index, (int, float)):
        return
    if not isinstance(message, (str,)):
        return

    neurons_request("m_ir_sensor", "send_str", str(message, "utf8"), index)
    
def send_learned_result(record_id = 1, index = 1):
    if not isinstance(record_id, (int, float)):
        return
    
    if not isinstance(index, (int, float)):
        return

    record_id  = round(record_id)
    if record_id != 1 and record_id != 2:
        return

    neurons_request("m_ir_sensor", "send_record", record_id - 1, index)

def learn(record_id = 1, index = 1):
    global RECORD_TIME
    
    if not isinstance(record_id, (int, float)):
        return

    if not isinstance(index, (int, float)):
        return
    record_id  = round(record_id)
    if record_id != 1 and record_id != 2:
        return

    neurons_request("m_ir_sensor", "record", (RECORD_TIME, record_id - 1), index)
    time.sleep(RECORD_TIME / 1000)

def receive_remote_code(index = 1):
    if not isinstance(index, (int, float)):
        return [0, 0]

    if not isinstance(index, (int, float)):
        return [0, 0]
        
    value = neurons_async_read("m_ir_sensor", "read_cmd", (), index, request_first = False)
    # ir sensor is processed specially
    if len(value) == 1:
        return [0 , 0]
    else:
        if time.ticks_ms() - value[-1] < RECEIVING_INTERVAL_THRESHOLD:
            return value[0 : 2]
        else:
            return [0, 0]

def is_receive(cmd, index = 1):
    if not isinstance(index, (int, float)):
        return False

    if isinstance(cmd, str):
        if receive(index) == cmd:
            return True
        else:
            return False
    elif isinstance(cmd, list):
        if receive_remote_code(index) == cmd:
            return True
        else:
            return False
    else:
        return False
        

def __learn_online(record_id = 1, index = 1):
    global RECORD_TIME
    
    if not isinstance(record_id, (int, float)):
        return

    if not isinstance(index, (int, float)):
        return
    record_id  = round(record_id)
    if record_id != 1 and record_id != 2:
        return

    neurons_request("m_ir_sensor", "record", (RECORD_TIME, record_id), index)
