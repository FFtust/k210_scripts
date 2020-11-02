from struct import pack, unpack
import time
import re
import uos
import _thread

from neurons_data_conversion import *
from neurons_dicts import *

# Note!!!!!!!!!!
  # find thread stack config in app/config.py 
  
# neurons config 
HEART_PACKAGE_USE_INDIVIDUAL_THREAD = False
POLLING_TIME_FOR_ASSIGNMENT_ID = 0.5 # unit: second
HEART_PACKAGE_THREAD_STACK_SIZE = 5 * 1024
HEART_PACKAGE_THREAD_PRIORITY  = 1
BLOCKING_READ_MAT_TIME_MS = 200

# global variabls for neurons engine
default_link = None

online_neurons_module_request_dict = dict()
online_neurons_module_response_dict = dict()

online_neurons_module_inactive_block_dict = dict()
online_neurons_module_temporary_result_dict = dict()

def calculation_block_id_and_subcommand_id(command_name, subcommand, block_index):
    global online_neurons_module_request_dict
    block_id = 0
    subcommand_id = 0

    if block_index <= 0:
        block_id = 0
    else:
        function_block_dict = online_neurons_module_request_dict[command_name]
        device_id_list = function_block_dict["device_id"]
        if len(device_id_list) >= block_index:
            block_id = device_id_list[block_index-1]
        elif block_index == 0xff:
            block_id = 0xff
        else:
            block_id = None
        function_dict = function_block_dict["function"]
        if subcommand in function_dict:
            subcommand_id = function_dict[subcommand]["command_id"]

    return block_id, subcommand_id

def fill_element_of_online_neurons_module_request_dict(device_id, type, subtype):
    global online_neurons_module_request_dict
    global online_neurons_module_inactive_block_dict

    if subtype == None:
        str_block_type = type * 256
    else:
        str_block_type = type * 256 +  subtype

    if str_block_type in common_neurons_command_request_dict:
        block_dict = common_neurons_command_request_dict[str_block_type]
        block_name = block_dict["name"]
        if device_id in online_neurons_module_inactive_block_dict:
            # online_neurons_module_inactive_block_dict[device_id]["name"] = block_name
            online_neurons_module_inactive_block_dict[device_id]["inactive"] = 0
            # online_neurons_module_inactive_block_dict[device_id]["type"] = str_block_type
        else:
            online_neurons_module_inactive_block_info_dict = dict()
            online_neurons_module_inactive_block_info_dict["name"] = block_name
            online_neurons_module_inactive_block_info_dict["inactive"] = 0
            online_neurons_module_inactive_block_info_dict["type"] = str_block_type
            online_neurons_module_inactive_block_dict[device_id] = online_neurons_module_inactive_block_info_dict
        if block_name in online_neurons_module_request_dict:
            if device_id in online_neurons_module_request_dict[block_name]["device_id"]:
                pass
            else:
                online_neurons_module_request_dict[block_name]["device_id"].append(device_id)
                online_neurons_module_request_dict[block_name]["device_id"].sort()
        else:
            online_neurons_module_request_block_dict = dict()
            online_neurons_module_request_block_dict["device_id"] = []
            online_neurons_module_request_block_dict["type"] =  type
            online_neurons_module_request_block_dict["subtype"] =  subtype
            online_neurons_module_request_block_dict["device_id"].append(device_id)
            if "function" in block_dict:
                function_dict_list = block_dict["function"]
                online_neurons_module_request_block_dict["function"] = function_dict_list
                online_neurons_module_request_dict[block_name] = online_neurons_module_request_block_dict

def fill_element_of_online_neurons_module_response_dict(device_id, type, subtype):
    global online_neurons_module_response_dict
    global common_neurons_command_response_dict

    if subtype == None:
        str_block_type = type * 256
    else:
        str_block_type = type * 256 +  subtype

    if str_block_type in online_neurons_module_response_dict:
        if device_id in online_neurons_module_response_dict[str_block_type]["device_id"]:
            pass
        else:
            online_neurons_module_response_dict[str_block_type]["device_id"].append(device_id)
            online_neurons_module_response_dict[str_block_type]["device_id"].sort()
            online_neurons_module_response_dict[str_block_type][device_id] = []


    elif str_block_type in common_neurons_command_response_dict:
        online_neurons_module_response_block_dict = dict()
        online_neurons_module_response_block_dict["device_id"] = []
        block_dict = common_neurons_command_response_dict[str_block_type]
        block_name = block_dict["name"]
        online_neurons_module_response_block_dict["name"] =  block_name
        online_neurons_module_response_block_dict["device_id"].append(device_id)
        online_neurons_module_response_block_dict[device_id] = []
        if "function" in block_dict:
            function_dict_list = block_dict["function"]
            online_neurons_module_response_block_dict["function"] = function_dict_list
            online_neurons_module_response_dict[str_block_type] = online_neurons_module_response_block_dict

def delete_online_neurons_module_request_dict(block_name, device_id):
    global online_neurons_module_request_dict
    if device_id in online_neurons_module_request_dict[block_name]["device_id"]:
        online_neurons_module_request_dict[block_name]["device_id"].remove(device_id)
        if len(online_neurons_module_request_dict[block_name]["device_id"]):
            pass
        else:
            del online_neurons_module_request_dict[block_name]

def delete_online_neurons_module_response_dict(block_type, device_id):
    global online_neurons_module_response_dict
    if block_type in online_neurons_module_response_dict:
        if device_id in online_neurons_module_response_dict[block_type]["device_id"]:
            online_neurons_module_response_dict[block_type]["device_id"].remove(device_id)
            if len(online_neurons_module_response_dict[block_type]["device_id"]):
                pass
            else:
                del online_neurons_module_response_dict[block_type]

def general_command_request(link, command_name, block_index, data_segment = []):
    global general_command_request_dict

    block_dict = general_command_request_dict[command_name]
    general_command_request_data = bytearray()

    block_id = block_index
    subcommand_id = 0x00
    general_command_request_data.append(block_id)

    # type data is added
    general_command_request_data.append(block_dict["type"])

    # subtype data is added
    if block_dict["subtype"] != None:
        general_command_request_data.append(block_dict["subtype"])

    arg_num = block_dict["para_num"]

    for i in range(arg_num):
        data_type = block_dict[i+1]
        if arg_num == 1:
            data_bytes = request_data_conversion(data_type, data_segment)
        else:
            data_bytes = request_data_conversion(data_type, data_segment[i])
        for data_element in data_bytes:
            general_command_request_data.append(data_element)

    # -1 indicate all channels 
    link(general_command_request_data, -1)
    return block_id, subcommand_id

def general_command_response(data_stream, copo = 0):
    result = None
    data_stream_temp = data_stream
    # deivce id contain the channel and port information
    device_id = (copo << 8) | (data_stream_temp[0])

    block_type = data_stream_temp[1]
    str_block_type = block_type * 256
    result = []
    if str_block_type in general_command_response_dict:
        block_dict = general_command_response_dict[str_block_type]
        if block_dict["name"] == "assign_id":
            arg_num = block_dict["para_num"]
            para_stream = data_stream_temp[2:]
            para_stream_start = 0
            for i in range(arg_num):
                data_type = block_dict[i+1]
                para_stream_start, data = response_data_conversion(data_type, para_stream_start, para_stream)
                result.append(data)
                if result[0] < 0x61 and result[0] > 0x20:
                    result.append(None)
            fill_element_of_online_neurons_module_request_dict(device_id,result[0],result[1])
            fill_element_of_online_neurons_module_response_dict(device_id,result[0],result[1])

        elif block_dict["name"] == "query_version":
            pass
        elif block_dict["name"] == "test_traffic":
            neurons_request("universal_response", None, 0xff, (0x0f))
        else:
            pass
    return device_id, result

def common_neurons_command_request(link, command_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_request_dict

    block_dict = online_neurons_module_request_dict[command_name]
    online_neurons_module_request_data = bytearray()

    block_id, subcommand_id = calculation_block_id_and_subcommand_id(command_name, subcommand, block_index)
    if block_id == None:
        return block_id
    

    # block id contain the channel and port information
    device_id = block_id & 0xff
    copo = (block_id >> 8) & 0xff

    online_neurons_module_request_data.append(device_id & 0xff)
    
    # type data is added
    online_neurons_module_request_data.append(block_dict["type"])

    # subtype data is added
    if block_dict["subtype"] != None:
        online_neurons_module_request_data.append(block_dict["subtype"])

    # special processing for motion sensor
    if command_name == "gyro_sensor" or command_name == "m_motion_sensor":
        if subcommand != "reset_x" and subcommand != "reset_y" and subcommand != "reset_z":
            online_neurons_module_request_data.append(0x01)
            online_neurons_module_request_data.append(0x00)

    function_dict_list = block_dict["function"]
    function_dict = function_dict_list[subcommand]
    online_neurons_module_request_data.append(function_dict["command_id"])
    
    arg_num = function_dict["para_num"]
    for i in range(arg_num):
        data_type = function_dict[i+1]
        if arg_num == 1:
            data_bytes =  request_data_conversion(data_type, data_segment)
        else:
            data_bytes =  request_data_conversion(data_type, data_segment[i])
        for data_element in data_bytes:
            online_neurons_module_request_data.append(data_element)
    
    link(online_neurons_module_request_data, copo)
    return block_id, subcommand_id

def common_neurons_command_response(data_stream, copo = 0):
    global online_neurons_module_temporary_result_dict
    global online_neurons_module_response_dict
    global read_count
    global last_ticks
    data_stream_temp = data_stream
    
    # deivce id contain the channel and port information
    block_id = (copo << 8) | (data_stream_temp[0])

    block_name = data_stream_temp[1]
    if block_name < 0x61 and block_name > 0x20:
        str_block_type = block_name * 256
        command_id = data_stream_temp[2]
        para_stream = data_stream_temp[3:]
    else:
        str_block_type = block_name * 256 + data_stream_temp[2]
        command_id = data_stream_temp[3]
        para_stream = data_stream_temp[4:]
    result_id = block_id * 256 + command_id
    result = []
    if str_block_type in online_neurons_module_response_dict:
        block_dict = online_neurons_module_response_dict[str_block_type]
        if not (command_id in block_dict["function"]):
            return
        function_dict = block_dict["function"][command_id]
        # para_stream = data_stream_temp[4:]
        para_stream_start = 0
        name = block_dict["name"]
        arg_num = function_dict["para_num"]
        for i in range(arg_num):
            data_type = function_dict[i+1]
            para_stream_start, data = response_data_conversion(data_type, para_stream_start, para_stream)
            result.append(data)

        # special processing for mbuild ir sensor
        if name == "m_ir_sensor":
            result.append(time.ticks_ms())

        if result_id in online_neurons_module_temporary_result_dict:
            online_neurons_module_temporary_result_dict[result_id]["result"] = result
        else:
            online_neurons_module_temporary_result = dict()
            online_neurons_module_temporary_result["result"] = result
            online_neurons_module_temporary_result_dict[result_id] = online_neurons_module_temporary_result

def activation_block_update():
    global online_neurons_module_inactive_block_dict
    global online_neurons_module_temporary_result_dict
    for device_id in online_neurons_module_inactive_block_dict:
        online_neurons_module_inactive_block_dict[device_id]["inactive"] += 1
        if online_neurons_module_inactive_block_dict[device_id]["inactive"] > 2:
            block_name = online_neurons_module_inactive_block_dict[device_id]["name"]
            block_type = online_neurons_module_inactive_block_dict[device_id]["type"]
            delete_online_neurons_module_request_dict(block_name, device_id)
            delete_online_neurons_module_response_dict(block_type, device_id)
            del online_neurons_module_inactive_block_dict[device_id]

            for result_id in online_neurons_module_temporary_result_dict:
                if ((result_id >> 8) & 0xff) == device_id:
                    del online_neurons_module_temporary_result_dict[result_id]

def get_default_result(block_name, subcommand):
    result = None
    global common_neurons_command_default_result_dict
    default_block_result_dict = []
    if block_name in common_neurons_command_default_result_dict:
        default_block_result_dict = common_neurons_command_default_result_dict[block_name]
        if subcommand in default_block_result_dict:
            result = default_block_result_dict[subcommand]
    return result

#this is subcommand not subtype
def request_distributor(link, block_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_request_dict
    if block_name in general_command_request_dict:
        return general_command_request(link, block_name, data_segment, block_index)
    elif block_name in online_neurons_module_request_dict:
        return common_neurons_command_request(link, block_name, subcommand, data_segment, block_index)

# it will be called in protocol parsing thread
def response_distributor(frame, channel, port = 0):
    if (frame[1] & 0x10) == 0x10:
        general_command_response(frame, (channel << 4) | (port & 0x0f))
    else:
        common_neurons_command_response(frame, (channel << 4) | (port & 0x0f))

def neurons_request(block_name, subcommand, data_segment = [], block_index = 0x01):
    global default_link,online_neurons_module_request_dict

    if block_name in general_command_request_dict:
        return general_command_request(default_link, block_name, data_segment, block_index)
    elif block_name in online_neurons_module_request_dict:
        return common_neurons_command_request(default_link, block_name, subcommand, data_segment, block_index)

def neurons_del_online_module_temporary_result(block_name, subcommand, block_index):
    global online_neurons_module_request_dict
    global online_neurons_module_temporary_result_dict
    block_id = None
    result_id = 0

    if block_name in online_neurons_module_request_dict:
        block_id, subcommand_id = calculation_block_id_and_subcommand_id(block_name, subcommand, block_index)
        if block_id == None:
            result_id = 0
        else:
            result_id = block_id * 256 + subcommand_id

    if result_id in online_neurons_module_temporary_result_dict:
        del online_neurons_module_temporary_result_dict[result_id]

    return result_id

def neurons_blocking_read(block_name, subcommand, data_segment = [], block_index = 0x01):
    global online_neurons_module_temporary_result_dict
    global online_neurons_module_response_dict
    result = None

    #delete online result 
    result_id = neurons_del_online_module_temporary_result(block_name, subcommand, block_index)

    last_ticks = time.ticks_ms()
    block_id = neurons_request(block_name, subcommand, data_segment, block_index)
    if block_id == None:
        result = get_default_result(block_name,subcommand)
        return result
    
    while True:
        if result_id in online_neurons_module_temporary_result_dict:
            result = online_neurons_module_temporary_result_dict[result_id]["result"]
            return result
        elif time.ticks_ms() - last_ticks > BLOCKING_READ_MAT_TIME_MS:
            result = get_default_result(block_name,subcommand)
            return result

        time.sleep(0.01)

def neurons_async_read(block_name, subcommand, data_segment = [], block_index = 0x01, request_first = True):
    global online_neurons_module_temporary_result_dict
    global online_neurons_module_request_dict
    result = None

    if block_name in online_neurons_module_request_dict:
        block_id, subcommand_id = calculation_block_id_and_subcommand_id(block_name, subcommand, block_index)
        if block_id == None:
            result = get_default_result(block_name,subcommand)
            return result
        
        # special processing for mbuild ir sensor
        if block_name == "m_ir_sensor":
            result_id = block_id * 256 + subcommand_id - 0x06
        else:
            result_id = block_id * 256 + subcommand_id
        
        if result_id in online_neurons_module_temporary_result_dict:
            result = online_neurons_module_temporary_result_dict[result_id]["result"]
            return result
        else:
            if request_first:
                # if not, send the request command firstly
                last_ticks = time.ticks_ms()
                block_id = neurons_request(block_name, subcommand, data_segment, block_index)
                if block_id == None:
                    result = get_default_result(block_name,subcommand)
                    return result
                while True:
                    if result_id in online_neurons_module_temporary_result_dict:
                        result = online_neurons_module_temporary_result_dict[result_id]["result"]
                        return result
                    elif time.ticks_ms() - last_ticks > BLOCKING_READ_MAT_TIME_MS:
                        result = get_default_result(block_name,subcommand)
                        return result
                    time.sleep(0.01)

            else:
                result = get_default_result(block_name,subcommand)
                return result                
    else:
        result = get_default_result(block_name,subcommand)
        return result

def neurons_get_online_list():
    global online_neurons_module_request_dict
    
    return online_neurons_module_request_dict

def neurons_is_block_online(block_name, index = 1):
    global online_neurons_module_request_dict
    
    if block_name in online_neurons_module_request_dict:
        function_block_dict = online_neurons_module_request_dict[block_name]
        device_id_list = function_block_dict["device_id"]
        if len(device_id_list) >= index:
            return True
        else:
            return False
    else:
        return False

def neurons_get_block_index(block_name):
    global online_neurons_module_request_dict
    
    if block_name in online_neurons_module_request_dict:
        function_block_dict = online_neurons_module_request_dict[block_name]
        device_id_list = function_block_dict["device_id"]
        return device_id_list
    else:
        return []

def neurons_async_read_test():
    global default_link
    online_neurons_module_request_data = bytearray(4)
    online_neurons_module_request_data[0] = 0x01
    online_neurons_module_request_data[1] = 0x64
    online_neurons_module_request_data[2] = 0x02
    online_neurons_module_request_data[3] = 0x01
    default_link(online_neurons_module_request_data)

neurons_heartbeat_enable_flag = True
neurons_heartbeat_last_time = 0
neurons_heartbeat_count = 0

def neurons_heartbeat_thread():
    # from makeblock import sleep_special
    global online_neurons_module_response_dict
    global online_neurons_module_request_dict
    global online_neurons_module_temporary_result_dict
    global default_link
    global neurons_heartbeat_enable_flag

    neurons_request("assign_id", None, 0xff, (0x00))
    count = 0
    while True:
        if neurons_heartbeat_enable_flag:
            activation_block_update()
            
            neurons_request("assign_id", None, 0xff, (0x00))
        if count < 20:
            count += 1
            time.sleep(0.1)
        else:
            time.sleep(POLLING_TIME_FOR_ASSIGNMENT_ID)

def neurons_heartbeat_func():
    global neurons_heartbeat_enable_flag, neurons_heartbeat_last_time, neurons_heartbeat_count
    assign_time = POLLING_TIME_FOR_ASSIGNMENT_ID

    if neurons_heartbeat_count < 20:
        neurons_heartbeat_count += 1
        assign_time = 0.1

    if time.ticks_ms() - neurons_heartbeat_last_time > assign_time * 1000:
        if neurons_heartbeat_enable_flag:
            activation_block_update()
                
            neurons_request("assign_id", None, 0xff, (0x00))
            neurons_heartbeat_last_time = time.ticks_ms()

def neurons_heartbeat_start():
    if USE_DICT_CREATED_PRIVIOUSLY:
        pass
    else:
        try:
            read_general_command_request_to_dict()
            read_general_command_response_to_dict()
            read_common_neurons_command_request_to_dict()
            read_common_neurons_command_response_to_dict()

        except Exception as e:
            print("read csv file error")

    if HEART_PACKAGE_USE_INDIVIDUAL_THREAD:
        _thread.stack_size(HEART_PACKAGE_THREAD_STACK_SIZE)
        _thread.start_new_thread(neurons_heartbeat_thread, (), HEART_PACKAGE_THREAD_PRIORITY, 2)
    else:
        from system.sys_loop import sys_loop_add_operation
        run_handle = sys_loop_add_operation(neurons_heartbeat_func, (), 0.5)
        run_handle.run("loop")
        
def neurons_heartbeat_enable():
    global neurons_heartbeat_enable_flag
    neurons_heartbeat_enable_flag = True

def neurons_heartbeat_disable():
    global neurons_heartbeat_enable_flag
    neurons_heartbeat_enable_flag = False

def neuron_request_bind_phy(link):
    global default_link
    default_link = link
