import threading
import time

from ..util.coder import encode
from ..util.model import JSONResponse
import signal


class UDPThread(threading.Thread):

    def __init__(self, socket):
        self._running = False
        self.socket = socket
        super(UDPThread, self).__init__()

    def stop(self):
        self._running = False


class UDPSendThread(UDPThread):
    """
    Sends the message for a measurement request
    :param message_str: message as a json-string; can be send after encoding to the device
    :param socket_object: a object from type UdpClient with an open socket inside
    """
    def __init__(self, message_str, socket):
        self._message_str = message_str
        super(UDPSendThread, self).__init__(socket)
        
    def run(self):
        self._running = True
        while self._running:
            next_send = time.time() + 1
            self.send()
            next_send -= time.time()  # ToDo: not perfect, but it works (probably send a request on every full second)
            time.sleep(next_send)

    def send(self):
        self.socket.send(encode(self._message_str))


class UDPRecvThread(UDPThread):
    """
    Receives a byte_array from the device on the open socket
    :param socket_object: a object from type UdpClient with an open socket inside
    """
    def __init__(self, socket, output_parser=None):
        super(UDPRecvThread, self).__init__(socket)
        self.output_parser = output_parser

    def run(self):
        self._running = True
        while self._running:
            self.recv()

    def recv(self):
        raw_bytes, sender_addr = self.socket.recv()
        if raw_bytes is not None:
            if self.output_parser is not None:
                self.output_parser(raw_bytes, sender_addr)
            else:
                print(sender_addr, JSONResponse.from_encoded(raw_bytes).json)


def wait(udp_threads):
    """
    Gracefully stop threads in SIGINT
    :param threads:
    :return:
    """
    def handler(signal, frame):
        for t in udp_threads:
            t.stop()
            t.join(1)
        t.socket.close()
        exit(0)

    signal.signal(signal.SIGINT, handler)

    while True:
        signal.pause()
