
import BlynkLib
import socket
import RPi.GPIO as GPIO
from gpiozero import AngularServo
from gpiozero import Servo
import pigpio
from time import sleep
import requests
import time


#set GPIO pinout
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ButtonPin1 = 17
ButtonPin2 = 27
ButtonPin3 = 22
ButtonPin4 = 10


GPIO.setup(ButtonPin1,GPIO.IN)
GPIO.setup(ButtonPin2,GPIO.IN)
GPIO.setup(ButtonPin3,GPIO.IN)
GPIO.setup(ButtonPin4,GPIO.IN)


x = 0

ServoPin1 = 12
ServoPin2 = 19
ServoPin3 = 26     
#GPIO.setup(26,GPIO.OUT)
servo1 = AngularServo(ServoPin1,min_angle= 0,max_angle = 90)
servo2 = AngularServo(ServoPin2,min_angle= 0,max_angle = 90)
servo3 = AngularServo(ServoPin3,min_angle= 0,max_angle = 90)
#cloud server
BLYNK_TEMPLATE_ID = 'TMPLfgpXYTzY'
BLYNK_DEVICE_NAME =  'Group19'
BLYNK_AUTH_TOKEN = 'fH4PQI6ap1bvdCFyLNHyIbLANObY0q8k'

blynk = BlynkLib.Blynk(BLYNK_AUTH_TOKEN)

token = '81876ixEScHdHq441q1PzvRr1YS7FknHIj1FJbE0Zh7'
url = 'https://notify-api.line.me/api/notify'


#function ส่งข้อความ  
#def messageNotify(message):
 #   payload = {'message':message}
 #   return _send(payload)

#ส่งรูปภาพเป็นไฟล์ รองรับ png jpg
#def fileNotify(filename):
 #   file = {'imageFile':open(filename,'rb')}
#    payload = {'message': 'ไฟล์รูปภาพ'}
#    return _send(payload,file)

#ส่งรูปภาพเป็น url
#def urlImageNotify(url):
 #   payload = {'message':" ",'imageThumbnail':url,'imageFullsize':url}
#    return _send(payload)

#ส่ง sticker สามารถดูรหัสสติกเกอร์ได้ที่ https://devdocs.line.me/files/sticker_list.pdf
#def stickerNotify(stickerID,stickerPackageID):
#    payload = {'message':" ",'stickerPackageId':stickerPackageID,'stickerId':stickerID}
#    return _send(payload)

#ส่ง ไป api ของ line
#def _send(payload,file=None):
#    headers = {'Authorization':'Bearer '+token}
 #   return requests.post(url, headers=headers , data = payload, files=file)



#ทดสอบเรียกใช้งาน
# messageNotify("ทดสอบ หวัดดี 2562")
# time.sleep(2)
# fileNotify('/home/pi/test.jpg')
# time.sleep(2)
# urlImageNotify('http://www.fleth.co.th/attachments/new/634.jpg')
# time.sleep(2)
# stickerNotify(621,4)
#for data stream Virtual Pin V0
@blynk.on('V0')
def Servo1_Moveforward(value):
#      servo1.angle = int(value[0])
    while servo1.angle < int(value[0]):
        servo1.angle += 1
        sleep(0.01)
    while servo1.angle > int(value[0]):
        servo1.angle -= 1
        sleep(0.01)


@blynk.on('V1')
def Servo2_Moveforward(value):
    print(value[0])
    while servo2.angle < int(value[0]):
        servo2.angle += 1
        sleep(0.01)
    while servo2.angle > int(value[0]):
        servo2.angle -= 1
        sleep(0.01)

@blynk.on('V2')
def Servo3_Moveforward(value):
    print(value[0])
    while servo3.angle < int(value[0]):
        servo3.angle += 1
        sleep(0.01)
    while servo3.angle > int(value[0]):
        if servo3.angle == int(value[0]):
            break
        servo3.angle -= 1
        sleep(0.01)
    
    
@blynk.on('connected')
def blynk_connected():
    print("Updating Value from Server")
    blynk.sync_virtual(0)
  

if __name__ == "__main__":
    while True:
        try:
            blynk.run()
            # if GPIO.input(17) == 0:
            #     servo3.angle = 0
            #     print("1")
            # if GPIO.input(27) == 0:
            #     servo3.angle = 30
            #     print("2")
            # if GPIO.input(22) == 0:
            #     servo3.angle = 45
            #     print("3")
            # if GPIO.input(10) == 0:
            #     servo3.angle = 90
            #     print("4")
            
        except socket.error as e:
            print(e)
            
            blynk.connect()