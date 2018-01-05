import client
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
servo=GPIO.PWM(17, 100)

c = client.create_client("test")
c.conn()
import time
time.sleep(1)
c.send("take/9999999/motor1:1\n")
time.sleep(1)
c.send("take/9999999/odometry:1\n")

i = [0, 0, 0, 0]
last_time = time.time()

def p():
    global i
    while True:
        msg = c.recv(10000)
        try:
            i = list(map(int, msg.rsplit(":", 1)[1].split(" ")))
        except:
            continue
#        print(i)
        time.sleep(0.25)

import threading
a = threading.Thread(target=p)
a.start()


def get_pos(vals):
    return vals[1] / 0.345  + vals[2] / 0.394, vals[0] / 0.390 + vals[3] / 0.388

def move(dist, to_left=1, to_right=1):
    vals = list(i)
#    print(vals)
    left, right = get_pos(vals)
    end_left = left + dist
    end_right = right + dist
    last_left, last_right = left, right
    sl = 180
    sr = 180
    cu_l = 0
    cu_r = 0
    while left < end_left or right < end_right:
        old_sl = sl
        old_sr = sr
        cur_left, cur_right = get_pos(i)
        dl = cur_left - last_left
        dr = cur_right - last_right
        cu_l += dl
        cu_r += dr
        ratio = (cu_l + 0.1) / (cu_r + 0.1)
        ratio2 = (cu_r + 0.1) / (cu_l + 0.1)
        cur_ratio = (dl + 0.1) / (dr + 0.1)
        cur_ratio2 = (dr + 0.1) / (dl + 0.1)
        print("dl", dl, "dr", dr, "cu_l", cu_l, "cu_r", cu_r, "ratio", ratio, "ratio2", ratio2)
        if cu_l < cu_r:
            if sl < 150 or sr < 150:
                sl *= ratio2
            else:
                sr /= ratio2
        elif cu_l > cu_r:
            if sr < 150 or sl < 150:
                sr *= ratio
            else:
                sl /= ratio
        if sl < 140:
            sl = 140
        if sr < 140:
            sr = 140
        if sl > 200:
            sl = 200
        if sr > 200:
            sr = 200
        c.sendtoserial("motor1", int(sr) * to_left)
        c.sendtoserial("motor2", int(sl) * to_right)
        c.sendtoserial("motor3", int(sl) * to_right)
        c.sendtoserial("motor4", int(sr) * to_left)
        left, right = cur_left, cur_right
        last_left, last_right = cur_left, cur_right
        print("speed:", sl, sr)
        print("cur:", cur_left, cur_right)
        print("end:", end_left, end_right)
        time.sleep(0.25)
    c.sendtoserial("motor1", "0")
    c.sendtoserial("motor2", "0")
    c.sendtoserial("motor3", "0")
    c.sendtoserial("motor4", "0")

def move_centimeter(cm):
    unit_per_cm = 704 / 71
    forward(unit_per_cm * cm)

def set_servo_angle(angle_idx):
    vals = [5, 9, 13, 17, 21]
    servo.start(vals[angle_idx])
    time.sleep(1.5)
    servo.start(0)

def turn(rad):
    rad *= -1
    while rad > 3.14:
        rad -= 3.14 * 2
    while rad < 0:
        rad += 3.14 * 2
    left_val = -1 if rad > 0 else 1
    right_val = -left_val
    c.sendtoserial("motor1", str(180 * left_val))
    c.sendtoserial("motor2", str(180 * right_val))
    c.sendtoserial("motor3", str(180 * right_val))
    c.sendtoserial("motor4", str(180 * left_val))
    time.sleep(10 * rad / 3.14)
    c.sendtoserial("motor1", "0")
    c.sendtoserial("motor2", "0")
    c.sendtoserial("motor3", "0")
    c.sendtoserial("motor4", "0")
    

#time.sleep(5)

#while True:
#    forward(2000)
#    time.sleep(15)


while True:
    set_servo_angle(0)
    set_servo_angle(1)
    set_servo_angle(2)
    set_servo_angle(3)
    set_servo_angle(4)


#time.sleep(20)
#turn(3.14 / 2)
#time.sleep(5)
#turn(-3.14 / 2)
