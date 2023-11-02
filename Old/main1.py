#!/usr/bin/python3
import BlynkLib
import socket
import serial,time
import numpy as np
import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero.pins.pigpio import PiGPIOFactory
import os
factory = PiGPIOFactory()  
from time import sleep
import requests


#set GPIO pinout
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) 

factory = PiGPIOFactory()  

ButtonPin1 = 17
ButtonPin2 = 27 
ButtonPin3 = 22
ButtonPin4 = 23 

x1=0
x2=0
x3=0
y1=0
y2=0
y3=0

GPIO.setup(ButtonPin1,GPIO.IN)
GPIO.setup(ButtonPin2,GPIO.IN)
GPIO.setup(ButtonPin3,GPIO.IN)
GPIO.setup(ButtonPin4,GPIO.IN)
Time = 0
Mode = 0
rotate = 1


x = 0

ServoPin1 = 12
ServoPin2 = 13
ServoPin3 = 18
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
#GPIO.setup(26,GPIO.OUT)
servo1 = AngularServo(ServoPin1,min_angle= -1,max_angle = 91,pin_factory=factory)
servo2 = AngularServo(ServoPin2,min_angle= -1,max_angle = 91 ,initial_angle=45,pin_factory=factory)
servo3 = AngularServo(ServoPin3,min_angle= -1,max_angle = 91,pin_factory=factory)

#cloud server
BLYNK_TEMPLATE_ID = 'TMPLfgpXYTzY'
BLYNK_DEVICE_NAME =  'Group19'
BLYNK_AUTH_TOKEN = 'fH4PQI6ap1bvdCFyLNHyIbLANObY0q8k'

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

token = 'MCOvDtlW3S0loiha1p5JbJZfP9hATNM1aw99toiVk5v'
url = 'https://notify-api.line.me/api/notify'


#function ส่งข้อความ  
def messageNotify(message):
   payload = {'message':message}
   print("{}".format(message))
   return _send(payload)

#ส่งรูปภาพเป็นไฟล์ รองรับ png jpg
def fileNotify(filename):
    payload = {'message' : 'รูปภาพขณะนี้'}
    file = {'imageFile':open(filename,'rb')}
    return _send(payload,file)

#ส่งรูปภาพเป็น url
def urlImageNotify(url):
   payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
   return _send(payload)

#ส่ง sticker สามารถดูรหัสสติกเกอร์ได้ที่ https://devdocs.line.me/files/sticker_list.pdf
def stickerNotify(stickerID,stickerPackageID):
    payload = {'message':" ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
    return _send(payload)

#ส่ง ไป api ของ line
def _send(payload,file=None):
    headers = {'Authorization':'Bearer '+token}
    return requests.post(url, headers=headers , data = payload, files=file)


def back():
    while servo1.angle < 0:
        servo1.angle += 1
        sleep(0.05)
    while servo1.angle > 0:
        servo1.angle -= 1
        sleep(0.05)
    while servo2.angle < 45:
        servo2.angle += 1
        sleep(0.05)
    while servo2.angle > 45:
        servo2.angle -= 1
        sleep(0.05)
    servo3.angle = 0
    while servo3.angle < 0:
        servo3.angle += 1
        sleep(0.05)
    while servo3.angle > 0:
        servo3.angle -= 1

def go_back():
    global Mode
    while servo1.angle < 0:
        servo1.angle += 1
        sleep(0.05)
    while servo1.angle > 0:
        servo1.angle -= 1
        sleep(0.05)
    while servo2.angle < 45:
        servo2.angle += 1
        sleep(0.05)
    while servo2.angle > 45:
        servo2.angle -= 1
        sleep(0.05)
    while servo3.angle < 0:
        servo3.angle += 1
        sleep(0.05)
    while servo3.angle > 0:
        servo3.angle -= 1
    Mode = 2

#ทดสอบเรียกใช้งาน
#  
# time.sleep(2)
# fileNotify('/home/pi/test.jpg')
# time.sleep(2)
# urlImageNotify('http://www.fleth.co.th/attachments/new/634.jpg')
# time.sleep(2)
# stickerNotify(621,4)
#for data stream Virtual Pin V0
@blynk.on('V0')
def Servo1_Moveforward(value):
    print(int(value[0]))
    print(servo1.angle)
#      servo1.angle = int(value[0])
    while servo1.angle < int(value[0]):
        servo1.angle += 1
        sleep(0.05)
    while servo1.angle > int(value[0]):
        servo1.angle -= 1
        sleep(0.05)
    


@blynk.on('V1')
def Servo2_Moveforward(value):
    value[0] = int(value[0])*-1 + 45
    print(servo2.angle)
    while servo2.angle < value[0]:
        servo2.angle += 1
        sleep(0.05)
    while servo2.angle > value[0]:
        servo2.angle -= 1
        sleep(0.05)

@blynk.on('V2')
def Servo3_Moveforward(value):
    while servo3.angle < int(value[0]):
        servo3.angle += 1
        sleep(0.05)
    while servo3.angle > int(value[0]):
        if servo3.angle == int(value[0]):
            break
        servo3.angle -= 1
        sleep(0.05)
    
@blynk.on('V3')
def Bed(value):
    if(int(value[0] == 1)):
        messageNotify("Now on Bed Mode")
        while servo1.angle < 0:
            servo1.angle += 1
            sleep(0.05)
        while servo1.angle > 0:
            servo1.angle -= 1
            sleep(0.05)
        while servo2.angle < 45:
            servo2.angle += 1
            sleep(0.05)
        while servo2.angle > 45:
            servo2.angle -= 1
            sleep(0.05)
        while servo3.angle < 0:
            servo3.angle += 1
            sleep(0.05)
        while servo3.angle > 0:
            servo3.angle -= 1
            sleep(0.05)

@blynk.on('V4')
def Sitt(value):
    global Mode
    if(int(value[0]) == 1):
        if(Mode == 2):
            Mode = 1
            return 0
        messageNotify("Now on Chair Mode")
        while servo1.angle < 60:
            servo1.angle += 1
            sleep(0.05)
        while servo1.angle > 60:
            servo1.angle -= 1
            sleep(0.05)
        print(Mode)
        if(Mode == 1):
            Start = 0
            while(True):
                print(Start)
                Start += 1
                sleep(1)
                if(Start == Time):
                    go_back()
                    return 0
                if(Mode == 0):
                    go_back()
                    return 0




    @blynk.on('V5')
    def Rotate_Left(value):
        global Mode
        if(int(value[0]) == 1):
            if(Mode == 2):
                Mode = 1
                return 0
            messageNotify("Now on Side Sleep Left Mode")
            while servo2.angle < 10:
                servo2.angle += 1
                sleep(0.05)
            while servo2.angle > 10:
                servo2.angle -= 1
                sleep(0.05)
            if(Mode == 1):
                Start = 0
                while(True):
                    print(Start)
                    Start += 1
                    sleep(1)
                    if(Start == Time):
                        go_back()
                        return 0
                    if(Mode == 0):
                        go_back()
                        return 0

@blynk.on('V6')
def Rotate_Right(value):
    global Mode
    if(int(value[0]) == 0) :
        if(Mode == 2):
            Mode = 1
            return 0
        messageNotify("Now on Side Sleep Right Mode")
        while servo2.angle < 80:
            servo2.angle += 1
            sleep(0.05)
        while servo2.angle > 80:
            servo2.angle -= 1
            sleep(0.05)
        if(Mode == 1):
            Start = 0
            while(True):
                print(Start)
                Start += 1
                sleep(1)
                if(Start == Time):
                    go_back()
                    return 0
                if(Mode == 0):
                    go_back()
                    return 0
    
@blynk.on('V7')
def Change_Diaple_MOde(value):
    global Mode
    if(int(value[0]) == 0) :
        if(Mode == 2):
            Mode = 1
            return 0
        messageNotify("Now on Change_Diaple Mode")
        while servo3.angle < 30:
            servo3.angle += 1
            sleep(0.05)
        while servo3.angle > 30:
            servo3.angle -= 1
            sleep(0.05)
        if(Mode == 1):
            Start = 0
            while(True):
                print(Start)
                Start += 1
                sleep(1)
                if(Start == Time):
                    go_back()
                    return 0
                if(Mode == 0):
                    go_back()
                    return 0

@blynk.on('V8')
def Time_set(value):
    global Time
    if(int(value[0]) == 1):
        Time= int(value[0])
        print(Time)
@blynk.on('V9')
def Timer_Mode(value):
    global Mode
    if(int(value[0]) == 1):
        Mode = 1
        print(Mode)
    if(int(value[0]) == 0):
        Mode = 0

@blynk.on('V10')
def Camera_Mode(value):
    if(int(value[0]) == 1):
        os.system('libcamera-still -o test.jpg')
        fileNotify('/home/pi/sp70_sc/old/test.jpg')
        return
    
    

@blynk.on('connected')
def blynk_connected():
    print("Updating Value from Server")
    blynk.sync_virtual(0)

def Gas_ss():
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        time.sleep(0.1) #wait for serial to open
        if arduino.isOpen():
            print("{} connected!".format(arduino.port))
            try:
                while True:
                    Gas_val = arduino.readline()
                    if Gas_val != b'':
                        # print("{}".format(Gas_val))
                        print(Gas_val.decode('utf-8').rstrip())
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caught.")


if __name__ == "__main__":
    Is_d=0
    global ratate
    with serial.Serial("/dev/ttyACM0", 9600, timeout=1) as arduino:
        while True:
            try:
                blynk.run()
                time.sleep(0.1) #wait for serial to open
                if arduino.isOpen():
                    # print("Arudino {} connected!".format(arduino.port))
                    Gas_val = arduino.readline()
                    Real_Gas = Gas_val.decode('utf-8').rstrip() 
                    if Real_Gas == '1' :
                        print("Gas Detected")
                        messageNotify("Gas Detected")
                if(GPIO.input(17) == 0 ):
                    messageNotify("Now on Bed Mode")
                    while servo1.angle < 0:
                        servo1.angle += 1
                        sleep(0.05)
                    while servo1.angle > 0:
                        servo1.angle -= 1
                        sleep(0.05)
                    while servo2.angle < 45:
                        servo2.angle += 1
                        sleep(0.05)
                    while servo2.angle > 45:
                        servo2.angle -= 1
                        sleep(0.05)
                    while servo3.angle < 0:
                        servo3.angle += 1
                        sleep(0.05)
                    while servo3.angle > 0:
                        servo3.angle -= 1
                        sleep(0.05)
                if GPIO.input(27) == 0 and servo1.angle != 90 and servo1.angle != 0:
                    messageNotify("Now on Chair Mode")
                    if (y1 == 0):
                        while True:
                            if(servo1.angle > 89):
                                while GPIO.input(17) == 0:
                                    pass
                                break
                            if(GPIO.input(27) == 1):
                                break
                            servo1.angle+=1
                            sleep(0.05)
                            y1 = 1
                    else:
                        while True:
                            if(servo1.angle < 1):
                                while GPIO.input(27) == 0:
                                    pass
                                break
                            if(GPIO.input(27) == 1):
                                break
                            y1 =0
                            servo1.angle -= 1
                            sleep(0.05)
                if GPIO.input(22) == 0 :
                    ss = 0
                    back()
                    if(rotate == 1 and ss == 0):
                        messageNotify("Now on Left Side Sleep Mode")
                        while servo2.angle < 10:
                            servo2.angle += 1
                            sleep(0.05)
                        while servo2.angle > 10:
                            servo2.angle -= 1
                            sleep(0.05)
                        rotate = 2
                        ss = 1
                    if(rotate == 2 and ss == 0):
                        messageNotify("Now on Right Side Sleep Mode")
                        while servo2.angle < 80:
                            servo2.angle += 1
                            sleep(0.05)
                        while servo2.angle > 80:
                            servo2.angle -= 1
                            sleep(0.05)
                        rotate = 1
                        ss = 1     
                if GPIO.input(23) == 0:
                    messageNotify("Now on Change Diaple Mode") 
                    back()
                    while servo3.angle < 45:
                        servo3.angle += 1
                        sleep(0.05)
                    while servo3.angle > 45:
                        servo3.angle -= 1
                        sleep(0.05)
                
                
                
            except socket.error as e:
                print(e)
                blynk.connect()