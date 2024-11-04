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

# 변수 초기화
pulse_count = 0

def send_mail(subject, body):
    message = f"Subject: {subject}\n\n{body}"
   
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

try:
    while True:
        # 심박 이벤트 감지
        if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
            pulse_count += 1  # 심박 이벤트 카운트
            print("High pulse detected!")  # 디버그용 메시지

        # 일정 시간마다 이메일로 심박수 데이터 전송
        interval = 60  # 60초마다 이메일 전송
        if pulse_count > 0 and pulse_count % interval == 0:
            send_mail("Heart Rate Data", f"Heart rate: {pulse_count} BPM")
            pulse_count = 0  # 카운트 초기화

        time.sleep(1)  # 1초마다 심박 이벤트 체크
except KeyboardInterrupt:
    GPIO.cleanup()
