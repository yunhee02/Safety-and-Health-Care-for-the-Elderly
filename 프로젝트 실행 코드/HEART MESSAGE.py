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

# 리스트를 사용하여 심박수 데이터 저장
heart_rate_data = []

def send_mail(subject, body):
    message = f"Subject: {subject}\n\n{body}"
   
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

try:
    while True:
        # 심박수 측정 및 데이터 저장
        if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
            # 측정된 심박수 값을 리스트에 추가
            heart_rate_data.append("High")  # 실제로는 측정된 값을 사용
            print("High pulse detected!")  # 디버그용 메시지

        # 일정 시간마다 이메일로 데이터 전송
        if len(heart_rate_data) >= 10:  # 데이터를 10개씩 모아서 전송
            data_to_send = ", ".join(heart_rate_data)
            send_mail("Heart Rate Data", f"Heart rate data: {data_to_send}")
            # 전송한 데이터는 초기화
            heart_rate_data = []

        time.sleep(1)  # 심박수 측정 주기 (예: 1초마다)
except KeyboardInterrupt:
    GPIO.cleanup()                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             