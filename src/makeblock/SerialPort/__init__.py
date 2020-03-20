# -*- coding: utf-8 -*
import glob
import signal
import sys
import threading
from multiprocessing import Array, Manager, Process
from time import ctime, sleep
import serial.tools.list_ports
import serial
import makeblock.utils

_ports = []

def create(port,baudrate=115200):
    """
    .. code-block:: python
        :linenos:

        from makeblock import SerialPort
        from makeblock import MegaPi

        uart = SerialPort.create("COM3")
        board = MegaPi.create(uart)

    """
    uart = SerialPort(port,baudrate)
    return uart

def __exiting(signal, frame):
    global _ports
    for uart in _ports:
        uart.exit()
    sys.exit(0)

signal.signal(signal.SIGINT, __exiting)

class SerialPort():
    """
    """
    def __init__(self, port, baudrate=115200, timeout=1):
        global _ports
        _ports.append(self)
        self.exiting = False
        self._responses = []
        self._ser = serial.Serial(port,baudrate)
        self._ser.timeout = 1
        sleep(1)
        self._thread = threading.Thread(target=self._on_read,args=(self._callback,))
        self._thread.start()

    def setup(self,callback):
        self._responses.append(callback)

    def _callback(self,received):
        for method in self._responses:
            method(received)

    def _on_read(self,callback):
        while True:
            if self.exiting:
                break
            if self.is_open():
                buf = self.read()
                if len(buf)==1:
                    callback(buf[0])
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
        self._thread.join()
        self.close()

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
        return serial.tools.list_ports.comports()
