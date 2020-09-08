import socket
import select

UDP_IP = '<broadcast>'
UDP_PORT = 9999
RECV_BYTE_SIZE = 2048


class UdpSocket(object):
    """
    opens a socket for every object and close it after using
    an object of the class UdpClient can call the methods send or recv for UDP-communication
    """

    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def __del__(self):
        self._socket.close()

    def send(self, encoded_message, ip=UDP_IP, port=UDP_PORT):
        self._socket.sendto(encoded_message, (ip, port))

    def recv(self):
        r, w, e = select.select([self._socket], [], [], 1)
        if self._socket in r:
            recv_bytes, sender_addr = self._socket.recvfrom(RECV_BYTE_SIZE)
            return recv_bytes, sender_addr

        return None, None

    def close(self):
        self._socket.close()
