# -*- coding: utf-8 -*
import struct
import time
from time import ctime, sleep
import makeblock.utils

from makeblock.protocols.PackData import MegaPiPackData

class _BaseModule:
    def __init__(self,board,port=0,slot=0):
        self._pack = None
        self.setup(board,port,slot)
        
    def _callback(self,data):
        pass

    def setup(self,board,port=0,slot=0):
        self._init_module()
        self._board = board
        self._pack.port = port
        self._pack.slot = slot

    def _init_module(self):
        pass

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)

class Servo(_BaseModule):
    """
        :description: Servo Driver - |servo_more_info|

        .. |servo_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/meds15-servo-motor.html" target="_blank">MEDS15 Servo</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/9g-micro-servo.html" target="_blank">9g Micro Servo</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/mg995-standard-servo.html" target="_blank">MG995 Servo</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range：PORT5～PORT8
        :type port: int
        :param slot: Slot Number, range：SLOT1～SLOT2
        :type slot: int

        :example:
            
        .. code-block:: python
            :linenos:

            servo = MegaPi.Servo(board,MegaPi.PORT6,MegaPi.SLOT1)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x0B
    
    def set_angle(self,angle):
        """
            set_angle

            :param angle: angle (°), range: 0~180
            :type angle: int

            :example:
                
            .. code-block:: python
                :linenos:

                while True:
                    servo.set_angle(30)
                    sleep(1)
                    servo.set_angle(120)
                    sleep(1)
                
        """
        self._pack.data = [self._pack.port,self._pack.slot,angle]
        self.call(self._pack)

class DCMotor(_BaseModule):
    """
        :description: DC Motor Driver - |dc_motor_more_info|

        .. |dc_motor_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">MegaPi Encoder/DC Motor Driver</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/36-dc-geared-motor-12v240rpm.html" target="_blank">36 DC Geared Motor 12V 240RPM</a> |
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/dc-motor-25-6v.html" target="_blank">DC Motor-25 6V</a> |
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/dc-motor-37-12v.html" target="_blank">DC Motor-37 12V</a> |
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/mini-metal-gear-motor-n20-dc-12v.html" target="_blank">Mini Metal Gear Motor – N20 DC 12V</a> |
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/tt-geared-motor-dc-6v-200rpm.html" target="_blank">TT Geared Motor DC 6V-200RPM</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/air-pump-motor-dc-12v-3202pm.html" target="_blank">Air Pump Motor DC 12V-3202PM</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/micro-peristaltic-pump-dc12-0v.html" target="_blank">Micro Peristaltic Pump DC12.0V</a> |
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/air-pump-motor-dc-12v-370-02pm.html" target="_blank">Air Pump Motor – DC 12V-370-02PM</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/water-pump-motor-dc-12v-370-04pm.html" target="_blank">Water Pump Motor – DC 12V-370-04PM</a>
            
        :param board: main controller
        :type board: mCore
        :param port: Port Number, range: M1～M2
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            dcmotor = mCore.DCMotor(board,mCore.M1)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x0A

    def run(self,speed):
        """
            :description: motor run with speed

            :param speed: speed (percent), range: -100~100
            :type speed: int
            
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    dcmotor.run(40)
                    sleep(5)
                    dcmotor.run(0)
                    sleep(5)
                    dcmotor.run(-40)
                    sleep(5)

        """
        self._pack.data = [self._pack.port,self._pack.slot]
        self._pack.data.extend(makeblock.utils.short2bytes(int(speed*2.55)))
        self.call(self._pack)
