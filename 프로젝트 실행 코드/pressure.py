import RPi.GPIO as GPIO
import time

FRS_pin = 17
LED_pin = 18

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FRS_pin, GPIO.IN)
    GPIO.setup(LED_pin, GPIO.OUT)
    
def loop():
    while True:
        if GPIO.input(FRS_pin) == GPIO.HIGH:
           GPIO.output(LED_pin, GPIO.HIGH)
           print("Pressure!")
        else:
            GPIO.output(LED_pin, GPIO.LOW)
            print("NO Pressure!")
            
        time.sleep(0.1)
        
def destroy():
    GPIO.cleanup()
    
if __name__ == "__main__":
    try:
        setup()
        loop()
    except keyboardInterrupt:
        destroy()