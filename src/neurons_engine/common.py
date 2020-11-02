import math
from struct import pack, unpack
import uos as os
import time

AD12_TRANSLATE_COE = 100 / 4095
########################################
def run_safe(func):
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except Exception as e:
            print('run safe: ' + str(e))
            return ''
    return _wrapper

node_table = \
{ \
  'C2': 65,
  'D2': 73,
  'E2': 82,
  'F2': 87,
  'G2': 98,
  'A2': 110,
  'B2': 123,
  'C3': 131,
  'D3': 147,
  'E3': 165,
  'F3': 175,
  'G3': 196,
  'A3': 220,
  'B3': 247,
  'C4': 262,
  'D4': 294,
  'E4': 330,
  'F4': 349,
  'G4': 392,
  'A4': 440,
  'B4': 494,
  'C5': 523,
  'D5': 587,
  'E5': 659,
  'F5': 698,
  'G5': 784,
  'A5': 880,
  'B5': 988,
  'C6': 1047,
  'D6': 1175,
  'E6': 1319,
  'F6': 1397,
  'G6': 1568,
  'A6': 1760,
  'B6': 1976,
  'C7': 2093,
  'D7': 2349,
  'E7': 2637,
  'F7': 2794,
  'G7': 3136,
  'A7': 3520,
  'B7': 3951,
  'C8': 4186,
  'D8': 4699,
}
MIDI_NOTE_NUM0 = 8.18
NOTE_FREQUENCE_RATIO = math.pow(2, (1 / 12))

# color table
color_table = {"red":(255,0,0), "green":(0,255,0), "blue":(0,0,255),\
               "yellow":(255,255,0), "purple":(255,0,255), "cyan":(0,255,255),\
               "white":(150,150,150), "orange":(255,50,0), "black":(0,0,0), "gray":(0,0,0), \
               "r":(255,0,0), "g":(0,255,0), "b":(0,0,255),\
               "y":(255,255,0), "p":(255,0,255), "c":(0,255,255),\
               "w":(150,150,150), "o":(255,50,0), "k":(0,0,0) \
               }

led_ring_tble = ((0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), (0, 255, 0), \
                 (255, 50, 0), (255, 50, 0), (255, 50, 0),\
                 (255, 0, 0), (255, 0, 0))

mbuild_color_table = {"red":1, "orange":2,"yellow":3,
                      "green":4, "cyan":5,"blue":6,
                      "purple":7,"white":8, "black":0,
                      "r":1, "o":2,"y":3,
                      "g":4, "c":5,"b":6,
                      "p":7,"w":8, "k":0
                      }

#for common use

# check the range of number
def num_range_scale(num, min_n = None, max_n = None, to_range = True):
    if min_n == None and max_n == None:
        return num
    
    if min_n != None:
        if to_range and num < min_n:
            num = min_n

    if max_n != None:
        if to_range and num > max_n:
            num = max_n
    return num

# debug
__PY_DEBUG = False 
def start_dbg_out():
    global __PY_DEBUG
    __PY_DEBUG = True

def stop_dbg_out():
    global __PY_DEBUG
    __PY_DEBUG = False

def print_dbg(*args):
    global __PY_DEBUG
    if __PY_DEBUG:
        print(*args)

# function type check
# warning!!!:  may not work
def __function_type():
    pass

def is_function(func):
    if type(func) == type(__function_type):
        return True
    else:
        return False

# bytes switch
def float_to_byte_4(data): 
    float_bytes = pack('f', data)
    return bytearray(float_bytes)

def int_to_byte_4(data):
    if type(data) == float:
        data = int(data)
    int_bytes = data.to_bytes(4, "little")
    return bytearray(int_bytes)

def int_to_byte_2(data):
    if type(data) == float:
        data = int(data)
    int_bytes = data.to_bytes(2, "little")
    return bytearray(int_bytes)

def byte_2_to_short(data):
    if len(data) != 2:
        return None
    result = unpack('h', bytearray(data))
    result = result[0]
    return bytearray(result)

def byte_4_to_float(data): 
    float_bytes = unpack('f', bytearray(data))
    result = result[0]
    return bytearray(result)

def byte_4_to_int(data):
    if len(data) != 4:
        return None
    result = unpack('l', bytearray(data))
    result = result[0]
    return bytearray(result)

def list_to_hex_str(data):
    for i in range(len(data)):
        temp = hex(data[i])
        if len(temp) == 3:
            temp = '0' + temp[-1]
        else:
            temp = temp[-2:]
        data[i] = temp

    return ''.join(data)
# stack usage print
from micropython import mem_info
from micropython import stack_use
def print_stack_usage(tag):
    print(tag)
    print(stack_use())

def print_mem_info(tag):
    print(tag)
    print(mem_info())


# about driver
def touchpad_value_scale(tp_id, value):
    ret = 0
    if tp_id <= 2:
        ret = (750 - value) / 730
    else:
        ret = (900 - value) / 880
    
    if ret < 0:
        ret = 0.0
    else:
        ret = round(ret * 100.0, 1)
    return ret

def get_tp_default_threshold(id):
    from global_objects import pin_o
    if id == 0:
        return pin_o.TOUCHPAD0_THRESHOLD_DEFAULT / 1000
    elif id == 1:
        return pin_o.TOUCHPAD1_THRESHOLD_DEFAULT / 1000
    elif id == 2:
        return pin_o.TOUCHPAD2_THRESHOLD_DEFAULT / 1000
    elif id == 3:
        return pin_o.TOUCHPAD3_THRESHOLD_DEFAULT / 1000
    else:
        return 0.1

# get battery percentage
# 4.05v is a empirical value, not the real threshold
''' data from battery suppliers
3.0-3.6V：20%
3.6-3.7V: 20-40%    
3.7-3.8V: 40-60%
3.8-3.9V: 60%-85%    
3.9-4.0V: 85%-90%
4.0-4.2V: 90%-100% 
'''

battery_per_list = \
((4.05, 100),
 ( 4.0, 90 ),
 ( 3.90, 85 ),
 ( 3.86, 70 ),
 ( 3.80, 60 ),
 ( 3.75, 50 ),
 ( 3.70, 40 ),
 ( 3.60, 20 ),
 ( 2.50, 0  )
)


def get_battery_percentage(vol):
    for item in battery_per_list:
      if vol >= item[0]:
        return item[1]
    return 0

# about filesystem
def filesys_get_files_structure():
    pass

def filesys_get_sta(path = '/'):
    '''
    {"f1_name":[size], "f2_name":[size]}
    '''
    cur_path = os.getcwd()
    os.chdir(path)
    ret = {}
    for item in os.listdir():
        ret.update({item:os.stat(item)[6]})

    return ret

# const value
class const_class():    
    def __init__(self):
      pass

IR_REMOTE = const_class()
IR_REMOTE.up = [0,64] #    ↑
IR_REMOTE.down = [0,25] #  ↓
IR_REMOTE.left = [0,7] #  ←
IR_REMOTE.right = [0,9] # →
IR_REMOTE.set  = [0,21] # set
IR_REMOTE.zero = [0,22] # 0
IR_REMOTE.one = [0,12]  # 1
IR_REMOTE.two = [0,24]  # 2
IR_REMOTE.three = [0,94] # 3
IR_REMOTE.four = [0,8] # 4
IR_REMOTE.five = [0,28] # 5
IR_REMOTE.six = [0,90]  # 6
IR_REMOTE.seven = [0,66] # 7
IR_REMOTE.eight = [0,82] # 8
IR_REMOTE.nine = [0,74] # 9
IR_REMOTE.A = [0,69]    # A
IR_REMOTE.B = [0,70]   # B
IR_REMOTE.C = [0,71]   # C
IR_REMOTE.D = [0,68]   # D
IR_REMOTE.E = [0,67]   # E
IR_REMOTE.F = [0,13]   # F

SPEAKER = const_class()
SPEAKER.hello = "!001" # hello 
SPEAKER.up = "!!00"  # up  
SPEAKER.down = "!!01"  # down  
SPEAKER.left = "!!02 " # left  
SPEAKER.right =  "!!03"  # right  

SPEAKER.hello = "!101" # hello
SPEAKER.hi = "!102" # hi 
SPEAKER.bye = "!103"  
SPEAKER.yeah = "!104"  
SPEAKER.wow = "!105"  
SPEAKER.laugh = "!106"  
SPEAKER.hum = "!107"  
SPEAKER.sad = "!108"  
SPEAKER.sigh = "!109"  
SPEAKER.annoyed = "!110"  
SPEAKER.angry = "!111"  
SPEAKER.surprised = "!112"  
SPEAKER.yummy = "!113"  
SPEAKER.curious = "!114"  
SPEAKER.embarrassed = "!115"  
SPEAKER.ready = "!116"  
SPEAKER.sprint = "!117"  
SPEAKER.sleepy = "!118"  
SPEAKER.meow = "!119"  
SPEAKER.hurt = "!120"  
  
SPEAKER.start = "!201"
SPEAKER.switch = "!202"  
SPEAKER.beeps = "!203"  
SPEAKER.buzzing = "!204"  
SPEAKER.exhaust = "!205"  
SPEAKER.explosion = "!206"  
SPEAKER.gotcha = "!207"  
SPEAKER.jump = "!208"  
SPEAKER.laser = "!209"  
SPEAKER.level_up = "!210"  
SPEAKER.low_energy = "!211"  
SPEAKER.prompt_tone = "!212"  
SPEAKER.prompt_tone_up = "!213"  
SPEAKER.prompt_tone_down = "!214"  
SPEAKER.right = "!215"  
SPEAKER.wrong = "!216"  
SPEAKER.ring = "!217"  
SPEAKER.score = "!218"  
SPEAKER.step_1 = "!219"  
SPEAKER.step_2 = "!220"  
SPEAKER.wake = "!221"  
SPEAKER.warning = "!222"  
SPEAKER.radar = "!223"  

SPEAKER.metal_clash = "!301"
SPEAKER.shot_1 = "!302"  
SPEAKER.shot_2 = "!303"  
SPEAKER.glass_clink = "!304"  
SPEAKER.inflator = "!305"  
SPEAKER.running_water = "!306"  
SPEAKER.clockwork = "!307"  
SPEAKER.click = "!308"  
SPEAKER.bell = "!309"  
SPEAKER.current = "!310"  
SPEAKER.switch = "!311"  
SPEAKER.wood_hit_1 = "!312"  
SPEAKER.wood_hit_2 = "!313"  
SPEAKER.wood_hit_3 = "!314"  
SPEAKER.wood_hit_4 = "!315"  
SPEAKER.wood_hit_5 = "!316"  
SPEAKER.iron_1 = "!317"  
SPEAKER.iron_2 = "!318"  
SPEAKER.buckle = "!319"  
SPEAKER.coin = "!320"  
SPEAKER.drop = "!321"  
SPEAKER.bubble_1 = "!322"  
SPEAKER.bubble_2 = "!323"  
SPEAKER.wine_bottle_open = "!324"  
SPEAKER.wave = "!325"  
SPEAKER.magic = "!326"  
SPEAKER.spitfire = "!327"  
SPEAKER.heartbeat = "!328"  
SPEAKER.load = "!329"  

SPEAKER.zero  = "!401"
SPEAKER.one = "!402" 
SPEAKER.two  = "!403" 
SPEAKER.three  = "!404" 
SPEAKER.four  = "!405" 
SPEAKER.five  = "!406" 
SPEAKER.six  = "!407" 
SPEAKER.seven  = "!408" 
SPEAKER.eight  = "!409" 
SPEAKER.night  = "!410" 
SPEAKER.point  = "!411" 

SPEAKER.A  = "!412" 
SPEAKER.B  = "!413" 
SPEAKER.C  = "!414" 
SPEAKER.D  = "!415" 
SPEAKER.E  = "!416" 
SPEAKER.F  = "!417" 
SPEAKER.G  = "!418" 
SPEAKER.H  = "!419" 
SPEAKER.I  = "!420" 
SPEAKER.J  = "!421" 
SPEAKER.K  = "!422" 
SPEAKER.L  = "!423" 
SPEAKER.M  = "!424" 
SPEAKER.N  = "!425" 
SPEAKER.O  = "!426" 
SPEAKER.P  = "!427" 
SPEAKER.Q  = "!428" 
SPEAKER.R  = "!429" 
SPEAKER.S  = "!430" 
SPEAKER.T  = "!431" 
SPEAKER.U  = "!432" 
SPEAKER.V  = "!433" 
SPEAKER.W  = "!434" 
SPEAKER.X  = "!435" 
SPEAKER.Y  = "!436" 
SPEAKER.Z  = "!437" 
  
SPEAKER.black = "!501"         
SPEAKER.red = "!502"  
SPEAKER.orange = "!503"  
SPEAKER.yellow = "!504"  
SPEAKER.green = "!505"  
SPEAKER.cyan = "!506"  
SPEAKER.blue = "!507"  
SPEAKER.purple = "!508"  
SPEAKER.gray = "!509"  
SPEAKER.white = "!510"  
SPEAKER.brown = "!511"  
SPEAKER.pink = "!512" 
   
SPEAKER.sunny = "!521"  
SPEAKER.rainy = "!522"  
SPEAKER.cloudy = "!523"  
SPEAKER.windy = "!524"  
SPEAKER.snowy = "!525"  
SPEAKER.foggy = "!526"  
     
SPEAKER.yes = "!531"  
SPEAKER.no = "!532"  
SPEAKER.ok = "!533"  
SPEAKER.good = "!534"  
SPEAKER.thank_you = "!535"  
    
SPEAKER.cm = "!541"  
SPEAKER.inch = "!542"
SPEAKER.celsius = "!543"
SPEAKER.fahrenheit = "!544"
SPEAKER.pct = "!545"


############################
class i_efficient():
    def __init__(self, t = 1):
        self.start_time = 0
        self.count = 0
        self.timer_t = t

    def reset(self):
        self.start_time = time.ticks_ms()
        self.count = 0

    def start(self):
        self.start_time = time.ticks_ms()

    def stop(self, tag):
        end_t = time.ticks_ms()
        print("{0}:{1}".format(tag,  end_t- self.start_time))

    def add(self, step = 1):
        self.count += step

    def update(self):
        t = time.ticks_ms()
        if t - self.start_time > self.timer_t * 1000:
            print("count:{0}".format(self.count))
            self.start_time = time.ticks_ms()
