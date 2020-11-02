import sensor
import image
import lcd
import KPU as kpu

from machine import SPI
from fpioa_manager import fm, board_info
from machine import UART
import utime

import sensor, lcd
import gc

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.B128X128)
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames()
lcd.init()


fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
uart_B = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
spi1 = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=10000000, polarity=0 , phase=0, bits=8, firstbit=SPI.MSB, sck=6, mosi=7, miso=30, cs0=8)

class neu_protocol():
    def __init__(self, dev):
        self.pro_sta = 0
        self.pro_data = []
        self.dev = dev
        self.on_line = False

    def neuros_protocol_parse(self, data):
        for i in range(len(data)):
            if self.pro_sta == 1:
                self.pro_data.append(data[i])
            if data[i] == 0xf0:
                self.pro_sta = 1
                self.pro_data = []
            if data[i] == 0xf7:
                self.pro_sta = 0
                self.respond_device()
                return self.pro_data[:-1]

    def respond_device(self):
        self.dev.write(bytes([0xf0, 0x01, 0x10, 0x67, 0x0a, 0x02, 0xf7]))

    def create_frame(self, cmd_id, data):
        frame = [0xf0, 0x01, 0x67, 0x0a, cmd_id]
        frame.extend(data)
        summ = 0
        for i in range(len(frame)- 1):
            summ += frame[i + 1]
        summ &= 0x7f
        frame.append(summ)
        frame.append(0xf7)
        return frame

    def update_position(self, code):
        data = [0, 0, 0, 0]
        data[0] = code.x() - 101
        data[1] = code.y() - 56
        data[2] = code.w()
        data[3] = code.h()

        for i in range(4):
            if data[i] < 0:
                data[i] = 0
            if data[i] > 127:
                data[i] = 127
        print(self.create_frame(0x01, data))
        uart_B.write(bytes(self.create_frame(0x01, data)))

def _320X240_to_128_128(data):
    out = []
    for i in  range(128):
        out.extend(data[(320 * (i + 56) + 101) * 2: (320 * (i + 56) + 229) *2])
    return out

def update_screen(img = None):
    if img == None:
        img = sensor.snapshot()
    ss = bytes(_320X240_to_128_128(img.to_bytes()))
    spi1.write(ss)

def update_position(code):
    data = [0, 0, 0, 0]
    data[0] = code.x() - 101
    data[1] = code.y() - 56
    data[2] = code.w()
    data[3] = code.h()

    for i in range(4):
        if data[i] < 0:
            data[i] = 0
        if data[i] > 127:
            data[i] = 127
    uart_B.write(bytes(data))


def wait_update_cmd():
    data = uart_B.read()
    if data == None:
        return False

    ret = neu_pro.neuros_protocol_parse(data)
    if ret != None:
        print(ret)
        return True

    return False

neu_pro = neu_protocol(uart_B)
task = kpu.load(0x300000) #使用kfpkg将 kmodel 与 maixpy 固件打包下载到 flash
anchor = (1.889, 2.5245, 2.9465, 3.94056, 3.99987, 5.3658, 5.155437, 6.92275, 6.718375, 9.01025)
a = kpu.init_yolo2(task, 0.5, 0.3, 5, anchor)
utime.sleep(5)
while(True):
    img = sensor.snapshot()
    code = kpu.run_yolo2(task, img)
    if code:
        for i in code:
            print(i)
            neu_pro.update_position(i)
            a = img.draw_rectangle(i.rect())


    #a = lcd.display(img)
    if wait_update_cmd():
        update_screen(img)

    #utime.sleep(0.02)
a = kpu.deinit(task)
