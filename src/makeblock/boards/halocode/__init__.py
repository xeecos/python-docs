# -*- coding: utf-8 -*
from makeblock.boards.halocode.modules import *
from makeblock.boards.base import _BaseEngine
import makeblock.protocols as Protocols
from makeblock.protocols.PackData import HalocodePackData
from time import sleep

MODE_REQUEST = 0
MODE_CHANGE = 1
MODE_PERIOD = 2

def create(device):
    return Halocode(device)
    
class Halocode(_BaseEngine):
    def __init__(self,device):
        super().__init__(device,Protocols.HalocodeProtocol())
        while not self.protocol.ready:
            self.broadcast()
            sleep(0.5)
        sleep(1)
        self.setTransferMode()
        sleep(1)

    def setTransferMode(self):
        # pack = HalocodePackData()
        # pack.type = HalocodePackData.TYPE_SCRIPT
        # pack.mode = HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE
        # pack.script = "global_objects.communication_o.enable_protocol(global_objects.communication_o.REPL_PROTOCOL_GROUP_ID)"
        # self.call(pack)
        # sleep(1)
        self.repl('import communication')
        self.repl('communication.bind_passthrough_channels("uart0", "uart1")')
        sleep(1)

    def broadcast(self):
        pack = HalocodePackData()
        pack.type = HalocodePackData.TYPE_SCRIPT
        pack.mode = HalocodePackData.TYPE_RUN_WITH_RESPONSE
        pack.script = ""
        self.call(pack)
