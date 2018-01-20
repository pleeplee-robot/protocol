import socket

class Client:
    """Represent the basic operations that could occur between the client
        and the server.
    """

    def __init__(self, sock, address, name=""):
        """
        Setup the connection socket and inner data.
        """
        socket.setdefaulttimeout(0.01)
        self.socket = sock
        self.address = address
        self.name = name
        self.msg_id = 0

    def conn(self):
        """Set our public name on the server.
        """
        self.send("setname/{}/{}".format(self.msg_id, self.name))
        self.msg_id += 1

    def recv(self, size):
        return self.socket.recv(size).decode()

    def send(self, buf):
        return self.socket.send(buf.encode())

    def sendto(self, name, msg):
        """Send a message to a specific actor on the server.

        Params:
            name: The name of the actor that must receive the command.
            msg: The message to transmit.
        """
        self.send("send/{}/{}:{}".format(self.msg_id, name, msg))
        self.msg_id += 1

    def sendtoserial(self, module, msg):
        """Send a message to the server that must be transmitted to the Arduino.

        Params:
            module: The name of the module on the Arduino.
            msg: The message to transmit to the module.
        """
        self.send("sendserial/{}/{}:{}\n".format(self.msg_id, module, msg))
        self.msg_id += 1

def create_client(name):
    """Create a new client and connect it to the server.

    Args:
        name: The name that the client will take on the server.
    """
    address = "/run/com_handler.sock"
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(address)
    return Client(sock, "", name)
