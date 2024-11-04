import RPi.GPIO as GPIO
import time
import smtplib
import ssl

GPIO.setmode(GPIO.BOARD)
SENSOR_PIN = 13
GPIO.setup(SENSOR_PIN, GPIO.IN)

smtp_server = "smtp.gmail.com"
port = 587
sender_email = "hyh0725abcd@gmail.com"
receiver_email = "hyhe0725@naver.com"
password = "fabj ecur rxps wlgc"

def send_mail(subject, body):
    message = f"Subject: {subject}\n\n{body}"
   
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

try:
    while True:
        if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
            send_mail("Pressure!", "Pressure detected!")
            time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
