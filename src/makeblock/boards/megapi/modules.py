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
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range：PORT1～PORT4
        :type port: int
        :param slot: Slot Number, range：SLOT1～SLOT2
        :type slot: int

        :example:
            
        .. code-block:: python
            :linenos:

            servo = MegaPi.Servo(board,MegaPi.PORT1,MegaPi.SLOT1)
            while True:
                servo.set_angle(30)
                sleep(1)
                servo.set_angle(120)
                sleep(1)

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
        """
        self._pack.data = [self._pack.port,self._pack.slot,angle]
        self.call(self._pack)

class DCMotor(_BaseModule):
    """
        :description: DC Motor Driver - |dc_motor_more_info|

        .. |dc_motor_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT1～PORT4
        :type port: int
        :param slot: Slot Number, range: SLOT1～SLOT2
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            dcmotor = MegaPi.DCMotor(board,MegaPi.PORT1,MegaPi.SLOT1)
            while True:
                dcmotor.run(40)
                sleep(5)
                dcmotor.run(0)
                sleep(5)
                dcmotor.run(-40)
                sleep(5)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x0A

    def run(self,speed):
        """
            :description: motor run

            :param speed: speed (percent), range: -100~100
            :type speed: int
        """
        self._pack.data = [self._pack.port,self._pack.slot]
        self._pack.data.extend(makeblock.utils.short2bytes(int(speed*2.55)))
        self.call(self._pack)

class RGBLed(_BaseModule):
    """
        :description: RGB Led Driver - |rgbled_more_info|

        .. |rgbled_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT1～PORT4
        :type port: int
        :param slot: Slot Number, range: SLOT1～SLOT2
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            rgbled = MegaPi.RGBLed(board,MegaPi.PORT1,MegaPi.SLOT1)
            while True:
                rgbled.set_pixel(0,0xff,0x0,0x0)
                sleep(1)
                rgbled.set_pixel(0,0x0,0xff,0x0)
                sleep(1)
                rgbled.set_pixel(0,0x0,0x0,0xff)
                sleep(1)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x08

    def set_color(self,index,red,green,blue):
        """
            :description: set color for led

            :param index: led index, 0 for all, range: >=0
            :type index: int
            :param red: color red, range: 0~255
            :type red: int
            :param blue: color blue, range: 0~255
            :type blue: int
            :param green: color green, range: 0~255
            :type green: int
        """
        self._pack.data = [self._pack.port,self._pack.slot,index]
        self._pack.data.append(red)
        self._pack.data.append(green)
        self._pack.data.append(blue)
        self.call(self._pack)

    def set_colors(self,pixels):
        """
            :description: set colors for all leds

            :param pixels: rgb colors for all leds, [red1,green1,blue1,red2,green2,blue2...]
            :type pixels: list
        """
        self._pack.data = [self._pack.port,self._pack.slot]
        self._pack.data.extend(pixels)
        self.call(self._pack)

class StepperMotor(_BaseModule):
    """
        :description: Stepper Motor Driver - |stepper_more_info|

        .. |stepper_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param slot: Slot Number, range: SLOT1～SLOT4
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            stepper = MegaPi.StepperMotor(board,MegaPi.SLOT1)
            position = 0
            def on_finished(value):
                global position
                position = 5000 - position
                stepper.move_to(position,10000,on_finished)
            on_finished(position)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x4C
        self._pack.on_response = self.__on_parse

    def __on_parse(self,pack):
        self._callback(pack.data[0])

    def move_to(self,position,speed,callback):
        """
            :description: move to position with speed

            :param position: absolute position ( steps )
            :type position: int
            :param speed: stepper motor speed
            :type speed: int
            :param callback: trig function when moving finish
            :type callback: function
            
        """
        self._callback = callback
        self._pack.data = [0x6,self._pack.port]
        self._pack.data.extend(makeblock.utils.long2bytes(position))
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        super().request(self._pack)

    def run(self,speed):
        """
            :description: stepper motor run with speed

            :param speed: stepper motor speed
            :type speed: int
            
        """
        self._pack.data = [0x2,self._pack.port]
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        super().call(self._pack)

    def set_home(self):
        """
            :description: set position to zero
            
        """
        self._pack.data = [0x4,self._pack.port]
        super().call(self._pack)

class EncoderMotor(_BaseModule):
    """
        :description: Encoder Motor Driver - |encoder_more_info|

        .. |encoder_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param slot: Slot Number, range: SLOT1～SLOT4
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            encoder = MegaPi.EncoderMotor(board,MegaPi.SLOT1)
            position = 0
            def on_finished(value):
                position = 5000 - position
                encoder.move_to(position,100,on_finished)
            on_finished(position)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x3E
        self._pack.on_response = self.__on_parse

    def __on_parse(self,pack):
        self._callback(pack.data[0])

    def move_to(self,position,speed,callback):
        """
            :description: move to position with speed

            :param position: absolute position ( steps )
            :type position: int
            :param speed: encoder motor speed
            :type speed: int
            :param callback: trig function when moving finish
            :type callback: function
            
        """
        self._callback = callback
        self._pack.data = [0x6,self._pack.port]
        self._pack.data.extend(makeblock.utils.long2bytes(position))
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        super().request(self._pack)

    def run(self,speed):
        """
            :description: encoder motor run with speed

            :param speed: encoder motor speed
            :type speed: int
            
        """
        self._pack.data = [0x2,self._pack.port]
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        super().call(self._pack)

    def set_home(self):
        """
            :description: set position to zero
            
        """
        self._pack.data = [0x4,self._pack.port]
        super().call(self._pack)

class SevenSegmentDisplay(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x9

    def set_number(self,number):
        self._pack.data = [self._pack.port,self._pack.slot]
        self._pack.data.append(makeblock.utils.float2bytes(number))
        self.call(self._pack)

class Shutter(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x14

    def turn_on(self):
        self._pack.data = [self._pack.port,1]
        self.call(self._pack)

    def turn_off(self):
        self._pack.data = [self._pack.port,2]
        self.call(self._pack)

class LedMatrix(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x29

    def set_string(self,ssval):
        self._pack.data = [self._pack.port,1,0,0,len(ssval)]
        self._pack.data.append(makeblock.utils.string2bytes(ssval))
        self.call(self._pack)

    def set_pixels(self,pixels):
        self._pack.data = [self._pack.port,2,0,0]
        self._pack.data.append(pixels)
        self.call(self._pack)

    def set_time(self,hours,minutes,point=1):
        self._pack.data = [self._pack.port,3,point,hours,minutes]
        self.call(self._pack)

    def set_number(self,number):
        self._pack.data = [self._pack.port,4]
        self._pack.data.append(makeblock.utils.float2bytes(number))
        self.call(self._pack)

class InfrareReceiver(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x10
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Temperature(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x02
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port,self._pack.slot]
        super().request(self._pack)

class Ultrasonic(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x01
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Button(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x16
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(pack.data[1])

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port,4]
        super().request(self._pack)

class LineFollower(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x11
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class LimitSwitch(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x15
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port,self._pack.slot]
        super().request(self._pack)

class PIRMotion(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x0F
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Light(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x03
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Sound(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x07
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Potentionmeter(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x04
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Gyro(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x06
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1),makeblock.utils.bytes2float(pack.data,5),makeblock.utils.bytes2float(pack.data,9))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [0,0]
        super().request(self._pack)

class Compass(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x1A
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Joystick(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x05
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2short(pack.data,1),makeblock.utils.bytes2short(pack.data,4))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port,0]
        super().request(self._pack)

class Humiture(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x17
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(pack.data[1],pack.data[3])

    def read(self,mode,callback):
        self._callback = callback
        self._pack.data = [self._pack.port,2]
        super().request(self._pack)

class Flame(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x18
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2short(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Gas(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x19
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2short(pack.data,1))

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Touch(_BaseModule):
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x33
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(pack.data[1])

    def read(self,callback):
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Pin(_BaseModule):
    MODE_DIGITAL = 0x1E
    MODE_ANALOG = 0x1F
    MODE_PWM = 0x20
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def digital_write(self,pin,level):
        self._pack.module = Pin.MODE_DIGITAL
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.data = [pin,level]
        self.call(self._pack)

    def pwm_write(self,pin,pwm):
        self._pack.module = Pin.MODE_PWM
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.data = [pin,pwm]
        self.call(self._pack)

    def read(self,pin,mode,callback):
        self._pack.module = mode
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.data = [pin]
        super().request(self._pack)

class CNC(_BaseModule):
    def _init_module(self):
        pass

    def __on_parse(self,pack):
        pass

    def set_ratio(self,x_ratio,y_ratio,z_ratio):
        pass

    def set_spin(self,power):
        pass

    def moveTo(self,x_position,y_position,z_position):
        pass

    def move(self,x_position,y_position,z_position):
        pass