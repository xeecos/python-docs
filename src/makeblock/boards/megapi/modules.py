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
        :type board: MegaPi
        :param port: Port Number, range: PORT1～PORT4
        :type port: int
        :param slot: Slot Number, range: SLOT1～SLOT2
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            dcmotor = MegaPi.DCMotor(board,MegaPi.PORT1,MegaPi.SLOT1)

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

class RGBLed(_BaseModule):
    """
        :description: RGB Led Driver - |rgbled_more_info|

        .. |rgbled_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/me-rgb-led.html" target="_blank">Me RGB LED</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/led-rgb-strip-addressable-sealed-0-5m1m.html" target="_blank">LED RGB Strip</a> | 

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5～PORT8
        :type port: int
        :param slot: Slot Number when using led rgb strip, range: SLOT1～SLOT2
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            rgbled = MegaPi.RGBLed(board,MegaPi.PORT6)

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
            
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    rgbled.set_pixel(0,0xff,0x0,0x0)
                    sleep(1)
                    rgbled.set_pixel(0,0x0,0xff,0x0)
                    sleep(1)
                    rgbled.set_pixel(0,0x0,0x0,0xff)
                    sleep(1)
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
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/main-control-boards/megapi.html" target="_blank">More Info</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/42byg-stepper-motor.html" target="_blank">42BYG Stepper Motor</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/42byg-geared-stepper-motor.html" target="_blank">42BYG Geared Stepper Motor</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/57byg-stepper-motor.html" target="_blank">57BYG Stepper Motor</a>

        :param board: main controller
        :type board: MegaPi
        :param slot: Slot Number, range: SLOT1～SLOT4
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            stepper = MegaPi.StepperMotor(board,MegaPi.SLOT1)

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
            
            :example:

            .. code-block:: python
                :linenos:

                position = 0
                def on_finished(value):
                    global position
                    position = 5000 - position
                    stepper.move_to(position,10000,on_finished)
                on_finished(position)
        """
        self._callback = callback
        self._pack.data = [0x6,self._pack.port]
        self._pack.data.extend(makeblock.utils.long2bytes(position))
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        super().request(self._pack)

    def run(self,speed):
        """
            :description: run with speed

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
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motor-drivers/megapi-encoder-dc-driver-v1.html" target="_blank">More Info</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/motors/dc-encoder-motor-25-6v-185rpm.html" target="_blank">DC Encoder Motor – 25 6V-185RPM</a>

        :param board: main controller
        :type board: MegaPi
        :param slot: Slot Number, range: SLOT1～SLOT4
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            encoder = MegaPi.EncoderMotor(board,MegaPi.SLOT1)

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

            :example:

            .. code-block:: python
                :linenos:

                position = 0
                def on_finished(value):
                    position = 5000 - position
                    encoder.move_to(position,100,on_finished)
                on_finished(position)
            
        """
        self._callback = callback
        self._pack.data = [0x6,self._pack.port]
        self._pack.data.extend(makeblock.utils.long2bytes(position))
        self._pack.data.extend(makeblock.utils.short2bytes(speed))
        super().request(self._pack)

    def run(self,speed):
        """
            :description: run with speed

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
    """
        :description: Seven Segment Display - |7segdisplay_more_info|

        .. |7segdisplay_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/me-7-segment-display.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            sevseg = MegaPi.SevenSegmentDisplay(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x9

    def set_number(self,number):
        """
            :description: display number

            :param number: number
            :type number: float
            
            :example:

            .. code-block:: python
                :linenos:

                i = 0.0
                while True:
                    sevseg.set_number(i)
                    i+=0.4
                    if i>10.0:
                        i=0.0
                    sleep(1)

        """
        self._pack.data = [self._pack.port,self._pack.slot]
        self._pack.data.append(makeblock.utils.float2bytes(number))
        self.call(self._pack)

class Shutter(_BaseModule):
    """
        :description: Shutter for DSLR - |shutter_more_info|

        .. |shutter_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/execution/me-shutter.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            shutter = MegaPi.Shutter(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x14

    def turn_on(self):
        """
            :description: turn on

            :example:

            .. code-block:: python
                :linenos:

                while True:
                    sleep(5)
                    shutter.turn_on()
                    sleep(0.1)
                    shutter.turn_off()

        """
        self._pack.data = [self._pack.port,1]
        self.call(self._pack)

    def turn_off(self):
        """
            :description: turn off

        """
        self._pack.data = [self._pack.port,2]
        self.call(self._pack)

class LedMatrix(_BaseModule):
    """
        :description: LED Matrix Display - |ledmatrix_more_info|

        .. |ledmatrix_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/displays/me-led-matrix-8x16.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            ledmatrix = MegaPi.LedMatrix(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.module = 0x29

    def set_string(self,msg):
        """
            :description: display string

            :param msg: show message
            :type msg: str

            :example:

            .. code-block:: python
                :linenos:

                while True:
                    sleep(1)
                    ledmatrix.set_string('hello')
                    sleep(1)
                    ledmatrix.set_string('world')

        """
        self._pack.data = [self._pack.port,1,0,0,len(msg)]
        self._pack.data.append(makeblock.utils.string2bytes(msg))
        self.call(self._pack)

    def set_pixels(self,pixels):
        """
            :description: show leds by pixels

            :param pixels: 2 bytes
            :type pixels: list

            :example:

            .. code-block:: python
                :linenos:

                while True:
                    sleep(1)
                    ledmatrix.set_pixels([0xff,0xff])
                    sleep(1)
                    ledmatrix.set_pixels([0x0,0x0])

        """
        self._pack.data = [self._pack.port,2,0,0]
        self._pack.data.append(pixels)
        self.call(self._pack)

    def set_time(self,hours,minutes,colon=1):
        """
            :description: show time

            :param hours: hours
            :type hours: int
            :param minutes: minutes
            :type minutes: int
            :param colon: show colon
            :type colon: bool

            :example:

            .. code-block:: python
                :linenos:

                while True:
                    sleep(1)
                    ledmatrix.set_pixels([0xff,0xff])
                    sleep(1)
                    ledmatrix.set_pixels([0x0,0x0])

        """
        self._pack.data = [self._pack.port,3,colon,hours,minutes]
        self.call(self._pack)

    def set_number(self,number):
        """
            :description: show number

            :param number: number
            :type number: float

            :example:

            .. code-block:: python
                :linenos:

                i=0.0
                while True:
                    i+=0.4
                    if i>10:
                        i=0.0
                    ledmatrix.set_number(i)
                    sleep(1)

        """
        self._pack.data = [self._pack.port,4]
        self._pack.data.append(makeblock.utils.float2bytes(number))
        self.call(self._pack)

class InfrareReceiver(_BaseModule):
    """
        :description: Infrare Receiver - |infrare_more_info|

        .. |infrare_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/communicators/me-infrared-reciver-decode.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            ir = MegaPi.InfrareReceiver(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x10
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read ir code

            :param callback: trig when ir code has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("value:",value)

                while True:
                    ir.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Temperature(_BaseModule):
    """
        :description: Temperature - |temperature_more_info|

        .. |temperature_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/temperature-sensor-waterproofds18b20.html" target="_blank">Me Temperature Sensor</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int
        :param slot: Slot Number, range: SLOT1~SLOT2
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            temp = MegaPi.Temperature(board,MegaPi.PORT6,MegaPi.SLOT1)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x02
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read temperature asynchronously

            :param callback: trig when temperature has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("temperature:",value)

                while True:
                    temp.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port,self._pack.slot]
        super().request(self._pack)

class Ultrasonic(_BaseModule):
    """
        :description: Ultrasonic Sensor - |ultrasonic_more_info|

        .. |ultrasonic_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-ultrasonic-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            us = MegaPi.Ultrasonic(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x01
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read distance asynchronously

            :param callback: trig when distance has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("distance:",value)

                while True:
                    us.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Button(_BaseModule):
    """
        :description: Button - |button_more_info|

        .. |button_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/control/me-4-button.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            button = MegaPi.Button(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x16
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(pack.data[1])

    def read(self,callback):
        """
            :description: read pressed key code asynchronously

            :param callback: trig when pressed key code has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("button key pressed:",value)

                while True:
                    button.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port,4]
        super().request(self._pack)

class LineFollower(_BaseModule):
    """
        :description: LineFollower - |linefollower_more_info|

        .. |linefollower_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-line-follower.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            linefollower = MegaPi.LineFollower(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x11
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read linefollower status asynchronously

            :param callback: trig when linefollower status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("linefollower status:",value)

                while True:
                    linefollower.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class LimitSwitch(_BaseModule):
    """
        :description: LimitSwitch - |limitswitch_more_info|

        .. |limitswitch_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/adapters/me-rj25-adapter.html" target="_blank">Me RJ25 Adapter</a> | 
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-micro-switch-ab.html" target="_blank">Me Micro Switch A</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int
        :param slot: Slot Number, range: SLOT1~SLOT2
        :type slot: int

        :example:

        .. code-block:: python
            :linenos:

            limitswitch = MegaPi.LimitSwitch(board,MegaPi.PORT6,MegaPi.SLOT1)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x15
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read limitswitch status asynchronously

            :param callback: trig when limitswitch status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("limitswitch status:",value)

                while True:
                    limitswitch.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port,self._pack.slot]
        super().request(self._pack)

class PIRMotion(_BaseModule):
    """
        :description: PIR Motion - |pirmotion_more_info|

        .. |pirmotion_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-pir-motion-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            pir = MegaPi.PIRMotion(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x0F
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read pirmotion status asynchronously

            :param callback: trig when pirmotion status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("pirmotion status:",value)

                while True:
                    pir.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Light(_BaseModule):
    """
        :description: Light Sensor - |light_more_info|

        .. |light_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-light-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            light = MegaPi.Light(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x03
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read brightness asynchronously

            :param callback: trig when brightness has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("brightness:",value)

                while True:
                    light.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Sound(_BaseModule):
    """
        :description: Sound Sensor - |sound_more_info|

        .. |sound_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-sound-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            sound = MegaPi.Sound(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x07
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read loudness asynchronously

            :param callback: trig when loudness has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("loudness:",value)

                while True:
                    sound.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Potentiometer(_BaseModule):
    """
        :description: Potentiometer - |potentiometer_more_info|

        .. |potentiometer_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/control/me-potentiometer.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            potentiometer = MegaPi.Potentiometer(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x04
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read potentiometer asynchronously

            :param callback: trig when potentiometer has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("potentiometer:",value)

                while True:
                    potentiometer.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Gyro(_BaseModule):
    """
        :description: Gyro Sensor - |gyro_more_info|

        .. |gyro_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-3-axis-accelerometer-and-gyro-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi

        :example:

        .. code-block:: python
            :linenos:

            gyro = MegaPi.Gyro(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x06
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1),makeblock.utils.bytes2float(pack.data,5),makeblock.utils.bytes2float(pack.data,9))

    def read(self,callback):
        """
            :description: read gyro data asynchronously

            :param callback: trig when gyro data has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(values):
                    print("gyro:",values)

                while True:
                    gyro.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [0,0]
        super().request(self._pack)

class Compass(_BaseModule):
    """
        :description: Compass Sensor - |compass_more_info|

        .. |compass_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-compass.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            compass = MegaPi.Compass(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x1A
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def read(self,callback):
        """
            :description: read compass data asynchronously

            :param callback: trig when compass data has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("compass:",value)

                while True:
                    compass.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Joystick(_BaseModule):
    """
        :description: Joystick - |joystick_more_info|

        .. |joystick_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/control/me-joystick.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            joystick = MegaPi.Joystick(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x05
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2short(pack.data,1),makeblock.utils.bytes2short(pack.data,4))

    def read(self,callback):
        """
            :description: read joystick data asynchronously

            :param callback: trig when joystick data has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(values):
                    print("joystick:",values)

                while True:
                    joystick.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port,0]
        super().request(self._pack)

class Humiture(_BaseModule):
    """
        :description: Humiture Sensor - |humiture_more_info|

        .. |humiture_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-temperature-and-humidity-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            humiture = MegaPi.Humiture(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x17
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(pack.data[1],pack.data[2])

    def read(self,mode,callback):
        """
            :description: read humiture and temperature asynchronously

            :param callback: trig when humiture and temperature data has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(hum,temp):
                    print("humiture:",hum," temperature:",temp)

                while True:
                    humiture.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port,2]
        super().request(self._pack)

class Flame(_BaseModule):
    """
        :description: Flame Sensor - |flame_more_info|

        .. |flame_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-flame-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            flame = MegaPi.Flame(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x18
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2short(pack.data,1))

    def read(self,callback):
        """
            :description: read flame status asynchronously

            :param callback: trig when flame status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("flame:",value)

                while True:
                    flame.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Gas(_BaseModule):
    """
        :description: Gas Sensor - |gas_more_info|

        .. |gas_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-gas-sensormq2.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            gas = MegaPi.Gas(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x19
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2short(pack.data,1))

    def read(self,callback):
        """
            :description: read gas status asynchronously

            :param callback: trig when gas status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("gas:",value)

                while True:
                    gas.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Touch(_BaseModule):
    """
        :description: Touch Sensor - |touch_more_info|

        .. |touch_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/sensors/me-touch-sensor.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi
        :param port: Port Number, range: PORT5~PORT8
        :type port: int

        :example:

        .. code-block:: python
            :linenos:

            touch = MegaPi.Touch(board,MegaPi.PORT6)

    """
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.action = MegaPiPackData.ACTION_GET
        self._pack.module = 0x33
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(pack.data[1])

    def read(self,callback):
        """
            :description: read touch status asynchronously

            :param callback: trig when touch status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("touch:",value)

                while True:
                    touch.read(onReceived)
                    sleep(1)

        """
        self._callback = callback
        self._pack.data = [self._pack.port]
        super().request(self._pack)

class Pin(_BaseModule):
    """
        :description: Pin - |pin_more_info|

        .. |pin_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/main-control-boards/megapi.html" target="_blank">More Info</a>

        :param board: main controller
        :type board: MegaPi

        :example:

        .. code-block:: python
            :linenos:

            pin = MegaPi.Pin(board)

    """
    MODE_DIGITAL = 0x1E
    MODE_ANALOG = 0x1F
    MODE_PWM = 0x20
    def _init_module(self):
        self._pack = MegaPiPackData()
        self._pack.on_response = self.__on_parse

    def __on_parse(self, pack):
        self._callback(makeblock.utils.bytes2float(pack.data,1))

    def digital_write(self,pin,level):
        """
            :description: set digital pin output

            :param pin: digital io number 
            :type pin: int
            :param pwm: pwm value, range: 0~1
            :type pwm: int

            :example:

            .. code-block:: python
                :linenos:

                while True:
                    pin.digital_write(5,1)
                    sleep(1)
                    pin.digital_write(5,0)
                    sleep(1)

        """
        self._pack.module = Pin.MODE_DIGITAL
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.data = [pin,level]
        self.call(self._pack)

    def pwm_write(self,pin,pwm):
        """
            :description: set pwm pin output

            :param pin: pwm pin number 
            :type pin: int
            :param pwm: pwm value, range: 0~255
            :type pwm: int

            :example:

            .. code-block:: python
                :linenos:

                while True:
                    pin.pwm_write(5,100)
                    sleep(1)
                    pin.pwm_write(5,0)
                    sleep(1)

        """
        self._pack.module = Pin.MODE_PWM
        self._pack.action = MegaPiPackData.ACTION_RUN
        self._pack.data = [pin,pwm]
        self.call(self._pack)

    def read(self,pin,mode,callback):

        """
            :description: read pin status asynchronously

            :param callback: trig when pin status has been received 
            :type callback: function

            :example:

            .. code-block:: python
                :linenos:

                def onReceived(value):
                    print("pin:",value)

                while True:
                    pin.read(onReceived)
                    sleep(1)

        """
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