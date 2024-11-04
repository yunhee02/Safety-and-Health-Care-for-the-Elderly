from RPLCD.i2c import CharLCD
import smbus
import RPi.GPIO as GPIO
import time

# I2C 주소
lcd_i2c_addr = 0x27  # 실제 사용하는 LCD의 주소에 맞게 변경해야 합니다.

# I2C 
bus =smbus.SMBus(1)

# LCD 초기화
lcd = CharLCD(i2c_expander=lcd_i2c_addr)

# GPIO 핀 설정
led_pin = 11
touch_pin = 12

# GPIO 초기화
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(touch_pin, GPIO.IN)

# 알람 함수
def alarm():
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string('Time to take')
    lcd.cursor_pos = (1, 0)
    lcd.write_string('your medicine!')
    GPIO.output(led_pin, GPIO.HIGH)  # LED 켜기
    time.sleep(10)  # 10초 동안 알림 유지
    GPIO.output(led_pin, GPIO.LOW)  # LED 끄기

# 터치 센서 인터럽트 핸들러
def touch_callback(channel):
    alarm()  # 알람 함수 호출

# 터치 센서 감지 설정
GPIO.add_event_detect(touch_pin, GPIO.RISING, callback=touch_callback, bouncetime=300)

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    lcd.clear()
    lcd.close()
    GPIO.cleanup()
