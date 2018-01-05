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
    index, val = int(input()), int(input())
    if index == 100:
        c.sendtoserial("servo", str(val))
        continue
    if val > i[index]:
        for j in range(i[index], val + 1, 5):
            c.sendtoserial("motor{}".format(index + 1), str(j))
            time.sleep(0.15)
    else:
        for j in range(i[index], val - 1, 5):
            print(j)
            c.sendtoserial("motor{}".format(index + 1), str(j))
            time.sleep(0.15)
    c.sendtoserial("motor{}".format(index + 1), str(val))
    i[index] = val
    print(val)
    #print(c.recv(10000))
