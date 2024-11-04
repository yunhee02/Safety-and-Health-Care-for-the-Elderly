import time
import RPi.GPIO as GPIO
from datetime import datetime
from RPLCD.i2c import CharLCD

# LCD 설정 (I2C 주소와 설정을 맞춰주세요)
lcd = CharLCD('PCF8574', 0x27)

# 설정
ALARM_PIN = 11  # GPIO 핀 번호
ALARM_INTERVAL = 60  # 알람 간격 (초) - 예: 1 minute

# GPIO 설정
GPIO.setwarnings(False)  # 경고 메시지 억제
GPIO.setmode(GPIO.BOARD)  # 핀 번호매기는 방식 설정
GPIO.setup(ALARM_PIN, GPIO.OUT)

def alarm():
    print("Time to take your medication!")
    lcd.clear()
    lcd.write_string("Time to take your medication!")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
   
    GPIO.output(ALARM_PIN, GPIO.HIGH)  # LED 켜기 또는 부저 울리기
    time.sleep(5)  # 5초 동안 알람 유지
    GPIO.output(ALARM_PIN, GPIO.LOW)  # LED 끄기 또는 부저 멈추기

try:
    while True:
        time.sleep(ALARM_INTERVAL)  # 설정된 시간 동안 대기
        alarm()  # 알람 실행

except KeyboardInterrupt:
    print("Alarm system stopped by User")
    GPIO.cleanup()