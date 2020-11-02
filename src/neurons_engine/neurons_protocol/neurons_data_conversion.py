from struct import pack, unpack
import re
## use number instead of string
# para_type_table = {'BYTE':1, "byte":2, "SHORT":3, "short":4, "long":5, "float":6, "STR1":7, "STR2":8, "STR3":9}

def send_BYTE(data):
    data_bytes = bytearray(1)

    if type(data) == float:
        data = int(data)

    data_bytes[0] = (data & 0x7f)
    return data_bytes

def send_byte(data):
    data_bytes = bytearray(2)

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(1, "big")
    data1 = input_data_to_bytes[0] & 0x7f
    data2 = (input_data_to_bytes[0] >> 7) & 0x7f

    data_bytes[0] = data1
    data_bytes[1] = data2
    return data_bytes

def send_SHORT(data):
    data_bytes = bytearray(2)

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(2, "big")
    data1 = input_data_to_bytes[1] & 0x7f
    data2 = ((input_data_to_bytes[0] << 1) + (input_data_to_bytes[1] >> 7)) & 0x7f

    data_bytes[0] = data1
    data_bytes[1] = data2
    return data_bytes

def send_short(data):
    data_bytes = bytearray(3)

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(2, "big")
    data1 = input_data_to_bytes[1] & 0x7f
    data2 = ((input_data_to_bytes[0] << 1) + (input_data_to_bytes[1] >> 7)) & 0x7f
    data3 = (input_data_to_bytes[0] >> 6) & 0x7f

    data_bytes[0] = data1
    data_bytes[1] = data2
    data_bytes[2] = data3

    return data_bytes

def send_float(data):

    data_bytes = bytearray(5)
 
    float_bytes = pack('f', data)
    input_data_to_bytes = float_bytes
    data1 = input_data_to_bytes[0] & 0x7f
    data2 = ((input_data_to_bytes[1] << 1) + (input_data_to_bytes[0] >> 7)) & 0x7f
    data3 = ((input_data_to_bytes[2] << 2) + (input_data_to_bytes[1] >> 6)) & 0x7f
    data4 = ((input_data_to_bytes[3] << 3) + (input_data_to_bytes[2] >> 5)) & 0x7f
    data5 = (input_data_to_bytes[3] >> 4) & 0x7f

    data_bytes[0] = data1
    data_bytes[1] = data2
    data_bytes[2] = data3
    data_bytes[3] = data4
    data_bytes[4] = data5
    return data_bytes

def send_long(data):
    data_bytes = bytearray(5)

    if type(data) == float:
        data = int(data)

    input_data_to_bytes = data.to_bytes(4, "big")
    data1 = input_data_to_bytes[3] & 0x7f
    data2 = ((input_data_to_bytes[2] << 1) + (input_data_to_bytes[3] >> 7)) & 0x7f
    data3 = ((input_data_to_bytes[1] << 2) + (input_data_to_bytes[2] >> 6)) & 0x7f
    data4 = ((input_data_to_bytes[0] << 3) + (input_data_to_bytes[1] >> 5)) & 0x7f
    data5 = (input_data_to_bytes[0] >> 4) & 0x7f

    data_bytes[0] = data1
    data_bytes[1] = data2
    data_bytes[2] = data3
    data_bytes[3] = data4
    data_bytes[4] = data5
    return data_bytes

def send_STR1(data):
    data_bytes = bytearray(1 + len(data))
    data_bytes_BYTE = send_BYTE(len(data))
    
    data_bytes[0] = data_bytes_BYTE[0]

    for i in range(len(data)):
        if type(data[i]) == str:
            data_bytes[1 + i] = ord(data[i])
        elif type(data[i]) == int:
            data_bytes[1 + i] = data[i]

    return data_bytes


def send_STR2(data):
    data_bytes = bytearray(2 + len(data))
    data_bytes_SHORT = send_SHORT(len(data))
    
    data_bytes[0] = data_bytes_SHORT[0]
    data_bytes[1] = data_bytes_SHORT[1]

    for i in range(len(data)):
        if type(data[i]) == str:
            data_bytes[2 + i] = ord(data[i])
        elif type(data[i]) == int:
            data_bytes[2 + i] = data[i]

    return data_bytes

def read_BYTE(data):
    result = (data) & 0x7f
    return result

def read_byte(data):
    data1 = (data[0]) & 0x7f
    temp = (data[1] << 7) & 0x80
    result = data1 | temp
    data_bytes = pack('B', result)
    result = unpack('b', data_bytes)
    result = result[0]
    return result

def read_SHORT(data):
    data1 = (data[0]) & 0x7f
    temp = (data[1] << 7) & 0x80
    data1 |= temp
    data2 = (data[1] >> 1) & 0x7f
    result = (data2 << 8 | data1) & 0xffff
    return result

def read_short(data):
    data1 = (data[0]) & 0x7f
    temp = (data[1] << 7) & 0x80
    data1 |= temp

    data2 = (data[1] >> 1) & 0x7f
    temp = (data[2] << 6)
    data2 = data2 | temp
    result = (data2 << 8 | data1) & 0xffff

    data_bytes = pack('H', result)
    result = unpack('h', data_bytes)
    result = result[0]
    return result

def read_long(data):
    data1 = (data[0]) & 0x7f
    temp = data[1] << 7;
    data1 |= temp;

    data2 = (data[1] >> 1) & 0x7f;
    temp = (data[2] << 6);
    data2 |= temp;

    data3 = (data[2] >> 2) & 0x7f;
    temp = (data[3] << 5);
    data3 |= temp;

    data4 =  (data[3] >> 3) & 0x7f;
    temp = (data[4] << 4);
    data4 |= temp;

    result = (data4 << 24 | data3 << 16 | data2 << 8 | data1) & 0xffffffff
    data_bytes = pack('L', result)
    result = unpack('l', data_bytes)
    result = result[0]
    return result

def read_float(data):
    data1 = (data[0]) & 0x7f
    temp = data[1] << 7;
    data1 |= temp;

    data2 = (data[1] >> 1) & 0x7f;
    temp = (data[2] << 6);
    data2 |= temp;

    data3 = (data[2] >> 2) & 0x7f;
    temp = (data[3] << 5);
    data3 |= temp;

    data4 =  (data[3] >> 3) & 0x7f;
    temp = (data[4] << 4);
    data4 |= temp;

    result = (data4 << 24 | data3 << 16 | data2 << 8 | data1) & 0xffffffff

    data_bytes = pack('L', result)
    result = unpack('f', data_bytes)
    result = result[0]
    return result

def read_STR1(data):
    length = read_BYTE(data[0])
    data = data[1:]
    if len(data) != length:
        print("str1 format error")
        return 0, []
    result = str(data, "utf8")
    return length, result

def read_STR3(data):
    length = read_SHORT(data)
    if (len(data) / 2 - 1) != length:
        print("str3 format error")
        return 0, []

    result = bytearray(length)
    for i in range(length):
        result[i] = read_SHORT(data[2 + 2 * i: 4 + 2 * i])
    
    result = str(result, "utf8") 
    return length * 2 + 2, result

def request_data_conversion(data_type, data):
    if(data_type == "BYTE"):
        return send_BYTE(data)

    elif(data_type == "byte"):
        return send_byte(data)

    elif(data_type == "SHORT"):
        return send_SHORT(data)

    elif(data_type == "short"):
        return send_short(data)

    elif(data_type == "float"):
        return send_float(data)

    elif(data_type == "long"):
        return send_long(data)

    elif(data_type == "STR1"):
        return send_STR1(data)

    elif(data_type == "STR2"):
        return send_STR2(data)

def response_data_conversion(data_type, para_stream_index, para_stream):
    if data_type == "BYTE":
        data = read_BYTE(para_stream[para_stream_index])
        para_stream_index = para_stream_index + 1
        return para_stream_index, data

    elif data_type == "byte":
        data = read_byte(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 2
        return para_stream_index, data

    elif data_type == "SHORT":
        data = read_SHORT(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 2
        return para_stream_index, data

    elif data_type == "short":
        data = read_short(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 3
        return para_stream_index, data

    elif data_type == "long":
        data = read_long(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 5
        return para_stream_index, data

    elif data_type == "float":
        data = read_float(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + 5
        return para_stream_index, data

    elif data_type == "STR1":
        l, data = read_STR1(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + l
        return para_stream_index, data

    elif data_type == "STR3":
        l, data = read_STR3(para_stream[para_stream_index:])
        para_stream_index = para_stream_index + l
        return para_stream_index, data

def conversion_str_to_data(data_type, str_data):
    data = None
    if data_type == "BYTE":
        data = int(str_data)

    elif data_type == "byte":
        data = int(str_data)

    elif data_type == "SHORT":
        data = int(str_data)

    elif data_type == "short":
        data = int(str_data)

    elif data_type == "long":
        data = long(str_data)

    elif data_type == "float":
        data = float(str_data)
    
    return data
