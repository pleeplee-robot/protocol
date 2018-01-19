import socket
import sys
import os
import serial

from state import server_state

SERIAL = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=9600, timeout=0.05)

def tick(sock, state):
    print("tick")
    try:
        conn = sock.accept()
        state.connect(conn)
        print("Got a new client")
    except socket.timeout:
        pass
    for client in state.get_readable_clients(0.05):
        try:
            msg = client.recv(1024)
            if not msg:
                raise ConnectionResetError()
        except ConnectionResetError:
            state.disconnect(client)
            continue
        print("mesage received:", msg)

        for m in msg.split("\n"):
            if not m:
                continue
            m = m.split("/")
            print(m)
            kind, id, m = m
            print(kind, id, m)
            try:
                MSG_HANDLERS[kind](state, client, id, m)
            except KeyError:
                MSG_HANDLERS["nohandler"](state, client, id, m)
    try:
        line = SERIAL.readline().decode()[0:-2]
        if line:
            print("Received from serial:", line)
            src, msg = line.split(":", 1)
            client = state.get_owner(src)
            if client is not None:
                client.send("from" + src + ":" + msg + "\n")
    except:
         pass

def release_handler(state, client, id, message):
    try:
        state.release_possession(client, message)
        client.send("{}/{}".format(id, "OK"))
    except:
        client.send("{}/{}".format(id, "ERROR:Not in possession"))

def take_handler(state, client, id, message):
    try:
        slave, prio = message.split(":")
        prio = int(prio, 10)
    except:
        client.send("{}/{}".format(id, "ERROR:Not in 'slave colon prio' "
                                          "format"))
        return
    try:
        if state.take_possession(client, prio, slave):
            pass
#            client.send("{}/{}".format(id, "OK"))
        else:
            client.send("{}/{}".format(id, "FAILED:TAKEN"))
    except:
        client.send("{}/{}".format(id, "FAILED:NOSLAVE"))

def no_handler_handler(state, client, id, message):
    client.send("{}/{}".format(id, "ERROR:No handler registered."))

def setname_handler(state, client, id, message):
    print("Changing a name to", message)
    client.name = message

def send_handler(state, client, id, message):
    dst, msg = message.split(":", 1)
    c = state.get_client_by_name(dst)
    c.send(msg)

def send_serial_handler(state, client, id, message):
    print(message)
    SERIAL.write((message + "\n").encode())

MSG_HANDLERS = {
    "release": release_handler,
    "take": take_handler,
    "setname": setname_handler,
    "send": send_handler,
    "sendserial": send_serial_handler,
    "nohandler": no_handler_handler
}


def main():
    address = "/run/com_handler.sock"
    try:
        os.unlink(address)
    except:
        if os.path.exists(address):
            raise
    socket.setdefaulttimeout(0.01)
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(10)

    state = server_state()
    while True:
        tick(sock, state)

main()
