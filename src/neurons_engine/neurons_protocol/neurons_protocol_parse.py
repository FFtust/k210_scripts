#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import _thread
import time
from neurons_engine import response_distributor
from neurons_engine import neurons_heartbeat_func
from neurons_engine import neuron_request_bind_phy

# Note!!!!!!!!!!
  # find thread stack config in app/config.py 

NEURONS_PROTOCOL_HEAD = const(0xf0)
NEURONS_PROTOCOL_END = const(0xf7)

_FSM_STA_NONE = const(0)
_FSM_STA_HEAD = const(1)
_FSM_STA_DATA = const(2)
_FSM_STA_CHECKSUM = const(3)
_FSM_STA_END = const(4)


def create_f0f7_frame(data):
    frame = [0xf7]
    check_sum = 0
    for item in data:
        check_sum += item
    check_sum &= 0x7F

    frame.extend(data)
    frame.append(check_sum)
    frame.append(0xf7)

class _F0F7_frame:
    def __init__(self):
        self._frame_buf = [0] * 256
        self._data_in_index = 0
        self._check_sum = 0
        self._fsm_status = _FSM_STA_NONE
        
        self._frame_process = None

    def _frame_parse(self, data):
        for i in range(len(data)):
            if data[i] == NEURONS_PROTOCOL_HEAD:
                self._fsm_status = _FSM_STA_DATA
                self._data_in_index = 0
            elif data[i] == NEURONS_PROTOCOL_END:
                self._check_sum = 0
                for j in range(self._data_in_index):
                    self._check_sum += self._frame_buf[j]
                self._check_sum &= 0x7F

                if self._check_sum == self._frame_buf[self._data_in_index - 1]:
                    if self._frame_process:
                        _frame_process(self._frame_buf[0:self._data_in_index])

            elif self._fsm_status == _FSM_STA_DATA:
                self._frame_buf[self._data_in_index] = data[i]
                self._data_in_index += 1

    def _register_frame_process(self, func):
        self._frame_process = func

class neurons_protocol:
    def __init__(self):
        neuron_request_bind_phy(__neurons_engine_send_frame)
        _frame_c = _F0F7_frame()
        _frame_c._register_frame_process(self.parse_frame)

    def parse_frame(frame, channel_info = bytes([0x01,0x00,0x00,0x00])):
        response_distributor(frame, channel_info, 0x00)


#####################################################
def __neurons_engine_send_frame(frame, copo = -1):
    uart_B.write(create_f0f7_frame(frame))

neuron_request_bind_phy(__neurons_engine_send_frame)

neurons = neurons_protocol()

from fpioa_manager import fm, board_info
from machine import UART
import utime

def uart_rec_task():
    pre_time = utime.ticks_ms()

    while True:
        read_data = uart_B.read()
        if None != read_data:
            neurons._frame_c._frame_parse(read_data)
            continue

        if utime.ticks_ms() - pre_time > 500:
            neurons_engine.neurons_heartbeat_func()
            pre_time = utime.ticks_ms()

        utime.sleep(0.01)

def uart_rec_start():
    fm.register(board_info.PIN9,fm.fpioa.UART2_TX)
    fm.register(board_info.PIN10,fm.fpioa.UART2_RX)
    uart_A = UART(UART.UART1, 921600, 8, None, 1, timeout=1000, read_buf_len=4096)
    uart_B = UART(UART.UART2, 921600, 8, None, 1, timeout=1000, read_buf_len=4096)

    _thread.start_new_thread(uart_rec_task, ())
