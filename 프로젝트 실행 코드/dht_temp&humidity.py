import time
import board
import adafruit_dht
from RPLCD.i2c import CharLCD

# DHT11 설정
dhtDevice = adafruit_dht.DHT11(board.D4)

# LCD 설정
# I2C 주소와 설정을 맞춰주세요
lcd = CharLCD('PCF8574', 0x27)

while True:
    try:
        # 온도와 습도 읽기
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity

        # 터미널에 출력
        print('Temperature: {:.1f}°C, Humidity: {:.1f}%'.format(temperature, humidity))
       
        # LCD에 출력
        lcd.clear()
        lcd.cursor_pos = (0,0)
        lcd.write_string('Temp: {:.1f}C'.format(temperature))
        lcd.cursor_pos = (1,0)
        lcd.write_string('Hum: {:.1f}%'.format(humidity))
    except RuntimeError as error:
        # 읽기 실패 시 오류 메시지 출력
        print(error.args[0])
        time.sleep(2)
        continue
    except Exception as error:
        # 기타 예외 처리
        dhtDevice.exit()
        lcd.close(clear=True)
        raise error

    time.sleep(2)