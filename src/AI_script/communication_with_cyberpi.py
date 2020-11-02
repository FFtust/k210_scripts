from fpioa_manager import fm, board_info
from machine import UART
import utime

fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
uart_B = UART(UART.UART2, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

while True:

    read_data = uart_B.read()
    if None == read_data:
        continue

    print("string = ",read_data)
    utime.sleep(0.1)
