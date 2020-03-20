# -*- coding: utf-8 -*
from makeblock.protocols import HalocodeProtocol,MegaPiProtocol,NeuronProtocol
class _BaseEngine:
    MegaPi = "megapi"
    MeOrion = "meorion"
    mCore = "mcore"
    MeAutiga = "meauriga"
    mBuild = "mbuild"
    Halocode = "halocode"
    HalocodePro = "halocodepro"
    Neuron = "neuron"
    def __init__(self,type,device):
        self._type = type
        self._dev = device
        if type==_BaseEngine.Halocode :
            self._protocol = HalocodeProtocol()
        elif type==_BaseEngine.mBuild or type==_BaseEngine.Neuron :
            self._protocol = NeuronProtocol()
        else:
            self._protocol = MegaPiProtocol()
        self._dev.setup(self._protocol.on_parse)
        self._protocol.setup(self)
        self._responses = []
        self._subscribe_responses = []

    def call(self,pack):
        self._dev.send(pack.to_buffer())

    def request(self,pack):
        if pack.idx==0:
            pack.idx = self._protocol.next_idx
        self._responses.append(pack)
        self._dev.send(pack.to_buffer())

    def repl(self,script):
        buf = bytearray()
        buf.extend(map(ord, script+"\r\n"))
        self._dev.send(buf)

    def subscribe(self,pack):
        pack.subscribe_key = self._protocol.next_subscribe_key
        self._subscribe_responses.append(pack)
        self._dev.send(pack.to_buffer())

    def unsubscribe(self,pack):
        subscribe_pack = self.find_subscribe_response(pack)
        self.remove_subscribe_response(subscribe_pack)
        self._dev.send(pack.to_buffer())

    def on_response(self,pack):
        resp = self.find_response(pack)
        if not resp is None:
            resp.on_response(pack)

    def on_subscribe_response(self,pack):
        resp = self.find_subscribe_response(pack)
        if not resp is None:
            pack.value_name = resp.value_name
            resp.on_response(pack)

    def find_response(self,pack):
        for i in range(len(self._responses)):
            if self._protocol.check_response(pack,self._responses[i]):
                return self._responses[i]
        return None

    def remove_response(self,pack):
        if pack in self._responses:
            self._responses.remove(pack)
    
    def find_subscribe_response(self,pack):
        for i in range(len(self._subscribe_responses)):
            if self._protocol.check_subscribe_response(pack,self._subscribe_responses[i]):
                return self._subscribe_responses[i]
        return None

    def remove_subscribe_response(self,pack):
        if pack in self._subscribe_responses:
            self._subscribe_responses.remove(pack)

    @property
    def protocol(self):
        return self._protocol

    @property
    def type(self):
        return self._type
    
from makeblock.utils import bytes2string
class TestEngine():
    def __init__(self,device,protocol):
        self._dev = device
        self._protocol = protocol
        self._dev.setup(self._protocol.on_parse)
        self._protocol.setup(self)
        self._callback = None

    def on_response(self,resp):
        if not self._callback is None:
            msg = bytes2string(resp)
            try:
                self._callback(eval(msg))
            except(RuntimeError, SyntaxError, TypeError, NameError):
                self._callback(eval("{'err':'json parse err'}"))
        
    def setCallback(self,callback):
        self._callback = callback