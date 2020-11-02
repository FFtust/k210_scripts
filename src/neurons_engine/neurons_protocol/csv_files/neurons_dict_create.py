REMOVE_NUEONS_MODULE_FLAG = True

import time

general_command_request_dict_new = dict()
general_command_response_dict_new = dict()

common_neurons_command_request_dict_new = dict()
common_neurons_command_response_dict_new = dict()
common_neurons_command_default_result_dict_new = dict()

def read_general_command_request_to_dict():
    global general_command_request_dict_new
    # uos.chdir("/lib")
    with open("request_general_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        while line:
            general_command_request_block_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)
            general_command_request_block_dict["type"] = int(line_elements[1],16);
            if(line_elements[2] != "None"):
                general_command_request_block_dict["subtype"] = int(line_elements[2],16);
            else:
                general_command_request_block_dict["subtype"] = None;
            para_num = 1
            while line_elements[para_num+2] != "" and \
                  line_elements[para_num+2] != "\n" and \
                  (para_num + 2) < elements_length:
                general_command_request_block_dict[para_num] = line_elements[para_num+2];
                para_num = para_num + 1
            general_command_request_block_dict["para_num"] = para_num - 1
            general_command_request_dict_new[line_elements[0]] = general_command_request_block_dict
           
            line = f.readline()
    f.close( )
    #print(general_command_request_dict_new)

def read_general_command_response_to_dict():
    global general_command_response_dict_new
    # uos.chdir("/lib")
    with open("response_general_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        while line:
            general_command_response_block_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)
            type_str = (int(line_elements[2],16)) & 0x7f
            if(line_elements[3] != "None"):
                type_str = type_str * 256 + int(line_elements[3],16)
            else:
                type_str = type_str * 256
            general_command_response_block_dict["name"] = line_elements[0]

            para_num = 1
            while line_elements[para_num+3] != "" and \
                  line_elements[para_num+3] != "\n" and \
                  (para_num + 3) < elements_length:
                general_command_response_block_dict[para_num] = line_elements[para_num+3];
                para_num = para_num + 1
            general_command_response_block_dict["para_num"] = para_num - 1
            general_command_response_dict_new[type_str] = general_command_response_block_dict
            line = f.readline()

    #print(general_command_response_dict_new)
    f.close( )

def read_common_neurons_command_request_to_dict():
    global common_neurons_command_request_dict_new
    # uos.chdir("/lib")
    with open("request_common_neurons_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        common_neurons_command_request_block_dict = dict()

        while line:
            if REMOVE_NUEONS_MODULE_FLAG:
                if line[0] != 'm':
                    line = f.readline()
                    continue
            common_neurons_command_request_function_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)

            type_str = (int(line_elements[1],16)) & 0x7f

            if(line_elements[2] != "None"):
                type_str = type_str * 256 + int(line_elements[2],16);
            else:
                type_str = type_str * 256 + 0;

            if type_str in common_neurons_command_request_dict_new:
                pass
            else:
                common_neurons_command_request_function_dict_list = dict()
                common_neurons_command_request_block_dict = dict()
                common_neurons_command_request_block_dict["name"] =  line_elements[0]

            common_neurons_command_request_function_dict["command_id"] = int(line_elements[4],16);
            
            para_num = 1
            while line_elements[para_num+4] != "" and \
                  line_elements[para_num+4] != "\n" and \
                  (para_num + 4) < elements_length:
                common_neurons_command_request_function_dict[para_num] = line_elements[para_num+4];
                para_num = para_num + 1
            common_neurons_command_request_function_dict["para_num"] = para_num - 1
            common_neurons_command_request_function_dict_list[line_elements[3]] = common_neurons_command_request_function_dict
            common_neurons_command_request_block_dict["function"] = common_neurons_command_request_function_dict_list
            common_neurons_command_request_dict_new[type_str] = common_neurons_command_request_block_dict
           
            line = f.readline()
    f.close( )
    #print(common_neurons_command_request_dict_new)

def read_common_neurons_command_response_to_dict():
    global common_neurons_command_response_dict_new
    global common_neurons_command_default_result_dict_new
    # uos.chdir("/lib")
    with open("response_common_neurons_command.csv", "r") as f:
        line = f.readline()   #read the title line
        line = f.readline()
        while line:
            if REMOVE_NUEONS_MODULE_FLAG:
                if line[0] != 'm':
                    line = f.readline()
                    continue

            common_neurons_command_response_function_dict = dict()
            line_elements = line.split(',')
            elements_length = len(line_elements)
            type_str = (int(line_elements[2],16)) & 0x7f
            if(line_elements[3] != "None"):
                type_str = type_str * 256 + int(line_elements[3],16);
            else:
                type_str = type_str * 256 + 0;

            if type_str in common_neurons_command_response_dict_new:
                common_neurons_command_default_function_result_list = []
                pass
            else:
                common_neurons_command_response_function_dict_list = dict()
                common_neurons_command_response_block_dict = dict()
                common_neurons_command_response_block_dict["name"] =  line_elements[0]

                common_neurons_command_default_function_result_list = []
                common_neurons_command_default_block_result_dict = dict()

            common_neurons_command_response_function_dict["command_name"] = line_elements[4];
            para_num = 1
            while line_elements[para_num+5] != "" and \
                  line_elements[para_num+5] != "\n" and \
                  (para_num + 5) < elements_length:
                str_para = line_elements[para_num+5];
                pos = str_para.rfind('/')
                if pos == -1:
                    para_type = str_para
                    para_default_value = 0
                else:
                    para_type = str_para[0:pos]
                    para_default_value_str = str_para.split('/')[-1]
                    para_default_value = conversion_str_to_data(para_type, para_default_value_str)
                common_neurons_command_response_function_dict[para_num] = line_elements[para_num+5];
                common_neurons_command_default_function_result_list.append(para_default_value)
                para_num = para_num + 1
            common_neurons_command_response_function_dict["para_num"] = para_num - 1
            common_neurons_command_response_function_dict_list[int(line_elements[5],16)] = common_neurons_command_response_function_dict
            common_neurons_command_response_block_dict["function"] = common_neurons_command_response_function_dict_list
            common_neurons_command_default_block_result_dict[line_elements[4]] = common_neurons_command_default_function_result_list
            common_neurons_command_response_dict_new[type_str] = common_neurons_command_response_block_dict
            common_neurons_command_default_result_dict_new[line_elements[0]] = common_neurons_command_default_block_result_dict
            line = f.readline()
    f.close( )


def write_new_dict():
    with open("../neurons_dicts.py", "w") as f:
        f.write("# create by neurons_dict_create.py\r\n")
        f.write("#release_note: %s \r\n" %(release_note, ))
        f.write("# %s\r\n" %(time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()),))
        f.write("general_command_request_dict = " + str(general_command_request_dict_new) + "\r\n")
        f.write("general_command_response_dict = " + str(general_command_response_dict_new) + "\r\n")
        f.write("common_neurons_command_request_dict = " + str(common_neurons_command_request_dict_new) + "\r\n")
        f.write("common_neurons_command_response_dict = " + str(common_neurons_command_response_dict_new) + "\r\n")
        f.write("common_neurons_command_default_result_dict = " + str(common_neurons_command_default_result_dict_new) + "\r\n")

def print_new_dict():
    print("general_command_request_dict_new = ", general_command_request_dict_new)
    print("general_command_response_dict_new = ", general_command_response_dict_new)
    print("common_neurons_command_request_dict_new = ", common_neurons_command_request_dict_new)
    print("common_neurons_command_response_dict_new = ", common_neurons_command_response_dict_new)
    print("common_neurons_command_default_result_dict_new = ", common_neurons_command_default_result_dict_new)

read_general_command_request_to_dict()
read_general_command_response_to_dict()
read_common_neurons_command_request_to_dict()
read_common_neurons_command_response_to_dict()



release_note = "add command for smart servo "

try:
    import sys
    sys.path.append("..")

    from neurons_dicts import *

    if general_command_request_dict_new == general_command_request_dict \
       and general_command_response_dict_new == general_command_response_dict \
       and common_neurons_command_request_dict_new == common_neurons_command_request_dict \
       and common_neurons_command_response_dict_new == common_neurons_command_response_dict \
       and common_neurons_command_default_result_dict_new == common_neurons_command_default_result_dict:

        print("moudle is not update!!!!!!!!")
    else:
        print_new_dict()
        write_new_dict()
except:
    print_new_dict()
    write_new_dict();