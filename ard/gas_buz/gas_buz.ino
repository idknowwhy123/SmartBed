int ledPin = 4;
int analogPin = 2; //ประกาศตัวแปร ให้ analogPin แทนขา analog ขาที่5
int buzzer=2;
int val = 0;
int buz_status = 0;
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27,20,4); 
void setup() {
pinMode(ledPin, OUTPUT); // sets the pin as output
pinMode(buzzer, OUTPUT);
Serial.begin(9600);
lcd.init();                     
lcd.backlight();
lcd.setCursor(3,0);
// Print a message to the LCD.
lcd.print("PCSHS PL!");
}
void loop() {
 
val = analogRead(analogPin); //อ่านค่าสัญญาณ analog ขา5
//Serial.print("val = "); // พิมพ์ข้อมความส่งเข้าคอมพิวเตอร์ "val = "
//Serial.println(val); // พิมพ์ค่าของตัวแปร val
if (val > 300) { // สามารถกำหนดปรับค่าได้ตามสถานที่ต่างๆ
digitalWrite(ledPin, HIGH); // สั่งให้ LED ติดสว่าง
digitalWrite(buzzer,LOW); 
buz_status = 1;
Serial.println(buz_status);
lcd.setCursor(2,1);
lcd.print("GAS DETECTED!");
}
else {
  digitalWrite(buzzer,HIGH);
digitalWrite(ledPin, LOW); // สั่งให้ LED ดับ
buz_status = 0;
}
delay(100);
}
