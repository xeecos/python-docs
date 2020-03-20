# -*- coding: utf-8 -*
from .modules import *
from makeblock.boards.base import _BaseEngine
import makeblock.protocols as Protocols

PORT1 = 1
PORT2 = 2
PORT3 = 3
PORT4 = 4
PORT5 = 5
PORT6 = 6
PORT7 = 7
PORT8 = 8
SLOT1 = 1
SLOT2 = 2
SLOT3 = 3
SLOT4 = 4
M1 = 1
M2 = 2
def create(device):
    return mCore(device)

class mCore(_BaseEngine):
    
    """
    :description: mCore - |mcore_more_info|

    .. |mcore_more_info| raw:: html
    
        <a href="http://docs.makeblock.com/diy-platform/en/electronic-modules/main-control-boards/megapi.html" target="_blank">More Info</a>

    :example:

    .. code-block:: python
        :linenos:

        from time import sleep
        from makeblock import SerialPort
        from makeblock import MegaPi

        uart = SerialPort.create("COM3")
        board = MegaPi.create(uart)

    """
    def __init__(self,device):
        super().__init__(device,Protocols.MegaPiProtocol())

    def DCMotor(self,port):
        """
            :description: DC Motor
        """
        return DCMotor(self,port)