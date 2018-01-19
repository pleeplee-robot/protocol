import socket

class Client:
    def __init__(self, sock, address, name=""):
        socket.setdefaulttimeout(0.01)
        self.socket = sock
        self.address = address
        self.name = name
        self.msg_id = 0

    def conn(self):
        self.send("setname/{}/{}".format(self.msg_id, self.name))
        self.msg_id += 1

    def recv(self, size):
        return self.socket.recv(size).decode()

    def send(self, buf):
        return self.socket.send(buf.encode())

    def sendto(self, name, msg):
        self.send("send/{}/{}:{}".format(self.msg_id, name, msg))
        self.msg_id += 1

    def sendtoserial(self, module, msg):
        self.send("sendserial/{}/{}:{}\n".format(self.msg_id, module, msg))
        self.msg_id += 1

def create_client(name):
    address = "/run/com_handler.sock"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(address)
    return Client(sock, "", name)
