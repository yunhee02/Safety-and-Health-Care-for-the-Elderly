import time
import RPi.GPIO as GPIO
from hx711 import HX711

GPIO.setwarnings(False)
# 핀 설정
DT_PIN = 5  # Data Pin
SCK_PIN = 6  # Clock Pin

def cleanAndExit():
    print("Cleaning...")
    GPIO.cleanup()
    print("Bye!")
    exit()

hx = HX711(DT_PIN, SCK_PIN)
hx.reset()
hx.tare()

print("Tare done! Add weight now...")

try:
    while True:
        # 무게 측정
        val = hx.get_weight(5)
        print(f"Weight: {val} grams")

        # 측정 후 초기화
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)

except (KeyboardInterrupt, SystemExit):
    cleanAndExit()