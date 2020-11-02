from machine import SPI
from fpioa_manager import fm, board_info
from machine import UART
import utime

import sensor, lcd

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.B128X128)
#sensor.set_framesize(sensor.QVGA)
sensor.run(1)
sensor.skip_frames()
lcd.init()

fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
uart_B = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
spi1 = SPI(SPI.SPI1, mode=SPI.MODE_MASTER, baudrate=5000000, polarity=0 , phase=0, bits=8, firstbit=SPI.MSB, sck=6, mosi=7, miso=30, cs0=8)

def colorTo565(r, g, b):
    val = ((r & 0xf8) << 8) + ((g & 0xfc) << 3 ) + (b >> 3)

    return val & 0xff, val >> 8

def fill(r, g, b):
    l, m =  colorTo565(r, g, b)
    print(l,m)
    da = bytearray([0xff] * 128 * 128 * 2)
    for i in range(128 * 128):
        da[2 * i] = m
        da[2 * i + 1] = l
    spi1.write(da)
    #for i in range(8):
        #spi1.write(da[i * 128 * 32:(i+1)*32*128 ])
        #utime.sleep(0.01)
        #break

def update_screen():
    ss = sensor.snapshot()
    lcd.display(ss)
    ss = ss.to_bytes()
    spi1.write(ss)

count = 0
color_table = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
utime.sleep(10)
while True:

    #read_data = uart_B.read()
    #if None == read_data:
        #continue

    #fill(*color_table[count])
    #print("string = ", read_data)
    update_screen()
    utime.sleep(0.1)
    count += 1
    count %= 4

