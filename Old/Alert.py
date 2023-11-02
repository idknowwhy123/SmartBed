from time import sleep
import requests

token = 'MCOvDtlW3S0loiha1p5JbJZfP9hATNM1aw99toiVk5v'
url = 'https://notify-api.line.me/api/notify'


#function ส่งข้อความ  
def messageNotify(message):
   payload = {'message':message}
   return _send(payload)

#ส่งรูปภาพเป็นไฟล์ รองรับ png jpg
def fileNotify(filename):
    file = {'imageFile':open(filename,'rb')}
    return _send(file)

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


if __name__ == "__main__":
    while(1):
        messageNotify("กรุณาตรวจสอบผู้ป่วย")
        stickerNotify("10551378","6136")
        sleep(18000)