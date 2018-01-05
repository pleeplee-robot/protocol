import client
import time

c = client.create_client("test")
c.conn()
import time
time.sleep(1)
c.send("take/9999999/motor1:1\n")
time.sleep(1)
c.send("take/9999999/odometry:1\n")

def p():
    print("445")
    while True:
        print(c.recv(10000))
        time.sleep(5)

import threading
a = threading.Thread(target=p)
a.start()

i = [0, 0, 0, 0]

#while True:
#    for i in [1, 2, 3, 4]:
#        c.sendtoserial("motor{}".format(i), "200")
#        time.sleep(0.5)
#    time.sleep(1)
#    for i in [1, 2, 3, 4]:
#        c.sendtoserial("motor{}".format(i), "200")
#        time.sleep(0.5)
#    time.sleep(1)

while True:
    c.sendtoserial("motor3", "1")
    c.sendtoserial("motor4", "1")
    c.sendtoserial("motor1", "1")
    c.sendtoserial("motor2", "1")
    time.sleep(2)
    c.sendtoserial("motor3", "0")
    c.sendtoserial("motor4", "0")
    c.sendtoserial("motor1", "0")
    c.sendtoserial("motor2", "0")
    c.sendtoserial("servo", "0")
    time.sleep(1)
    c.sendtoserial("servo", "90")
    time.sleep(1)
    c.sendtoserial("servo", "180")
    time.sleep(2)
    c.sendtoserial("motor3", "-255")
    c.sendtoserial("motor4", "-255")
    c.sendtoserial("motor1", "-255")
    c.sendtoserial("motor2", "-255")
    time.sleep(2)
