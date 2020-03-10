# -*- coding: utf-8 -*
import glob
import signal
import sys
import threading
from multiprocessing import Array, Manager, Process
from time import ctime, sleep

import serial
import makeblock.utils

_ports = []

def create(port,baudrate=115200):
    """
    .. code-block:: python
        :linenos:

        from makeblock import SerialPort
        from makeblock.boards import MegaPi

        uart = SerialPort.create("COM3")
        board = MegaPi.create(uart)

    """
    uart = SerialPort(port,baudrate)
    _ports.append(uart)
    return uart

def __exiting(signal, frame):
    for uart in _ports:
        uart.exit()
    sys.exit(0)

signal.signal(signal.SIGINT, __exiting)

class SerialPort():
    """
    """
    def __init__(self, port, baudrate=115200, timeout=1):
        self.exiting = False
        self._responses = []
        self._ser = serial.Serial(port,baudrate)
        sleep(1)
        th = threading.Thread(target=self._on_read,args=(self._callback,))
        th.start()

    def setup(self,callback):
        self._responses.append(callback)

    def _callback(self,received):
        for method in self._responses:
            method(received)

    def _on_read(self,callback):
        while 1:
            if self.exiting:
                break
            if self.is_open():
                n = self.in_waiting()
                for i in range(n):
                    r = ord(self.read())
                    callback(r)
                sleep(0.002)
            else:    
                sleep(0.5)
                
    def send(self,buffer):
        # makeblock.utils.print_hex(buffer)
        if self.is_open():
            self._ser.write(buffer)
        sleep(0.002)

    def read(self):
        return self._ser.read()

    def is_open(self):
        return self._ser.isOpen()

    def in_waiting(self):
        return self._ser.inWaiting()

    def close(self):
        self._ser.close()

    def exit(self):
        self.exiting = True

    @staticmethod
    def list():
        """
        获取串口列表

        .. code-block:: python
            :linenos:

            from makeblock import SerialPort
            print(SerialPort.list())

        :param: 无
        :return: 串口列表
        """

        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
