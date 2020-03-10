# -*- coding: utf-8 -*
from .modules import *
from makeblock.boards.base import _BaseEngine
import makeblock.protocols as Protocols
from makeblock.protocols.PackData import NeuronPackData

MODE_REQUEST = 0
MODE_CHANGE = 1
MODE_PERIOD = 2

def create(device):
    return mBuild(device)

class mBuild(_BaseEngine):
    def __init__(self,device):
        super().__init__(device,Protocols.NeuronProtocol())
        self.broadcast()

    def broadcast(self):
        self._dev.send(NeuronPackData.broadcast().to_buffer())