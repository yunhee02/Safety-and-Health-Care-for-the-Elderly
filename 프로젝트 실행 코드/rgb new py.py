import smbus2
import time

# I2C 버스 설정
bus = smbus2.SMBus(1)

# TCS34725 I2C 주소
TCS34725_DEFAULT_ADDRESS = 0x29

# TCS34725 Register Set
TCS34725_COMMAND_BIT = 0x80
TCS34725_REG_ENABLE = 0x00  # Enables states and interrupts
TCS34725_REG_ATIME = 0x01  # RGBC integration time
TCS34725_REG_WTIME = 0x03  # Wait time
TCS34725_REG_CONFIG = 0x0D  # Configuration register
TCS34725_REG_CONTROL = 0x0F  # Control register
TCS34725_REG_CDATAL = 0x14  # Clear/IR channel low data register
TCS34725_REG_CDATAH = 0x15  # Clear/IR channel high data register
TCS34725_REG_RDATAL = 0x16  # Red ADC low data register
TCS34725_REG_RDATAH = 0x17  # Red ADC high data register
TCS34725_REG_GDATAL = 0x18  # Green ADC low data register
TCS34725_REG_GDATAH = 0x19  # Green ADC high data register
TCS34725_REG_BDATAL = 0x1A  # Blue ADC low data register
TCS34725_REG_BDATAH = 0x1B  # Blue ADC high data register

# TCS34725 Enable Register Configuration
TCS34725_REG_ENABLE_SAI = 0x40  # Sleep After Interrupt
TCS34725_REG_ENABLE_AIEN = 0x10  # ALS Interrupt Enable
TCS34725_REG_ENABLE_WEN = 0x08  # Wait Enable
TCS34725_REG_ENABLE_AEN = 0x02  # ADC Enable
TCS34725_REG_ENABLE_PON = 0x01  # Power ON

# TCS34725 Time Register Configuration
TCS34725_REG_ATIME_700 = 0x00  # Atime = 700 ms, Cycles = 256

# TCS34725 Gain Configuration
TCS34725_REG_CONTROL_AGAIN_1 = 0x00  # 1x Gain

class TCS34725:
    def __init__(self):
        self.enable_selection()
        self.time_selection()
        self.gain_selection()
   
    def enable_selection(self):
        """Select the ENABLE register configuration from the given provided values"""
        ENABLE_CONFIGURATION = (TCS34725_REG_ENABLE_AEN | TCS34725_REG_ENABLE_PON)
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_ENABLE | TCS34725_COMMAND_BIT, ENABLE_CONFIGURATION)
   
    def time_selection(self):
        """Select the ATIME register configuration from the given provided values"""
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_ATIME | TCS34725_COMMAND_BIT, TCS34725_REG_ATIME_700)
   
    def gain_selection(self):
        """Select the gain register configuration from the given provided values"""
        bus.write_byte_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_CONTROL | TCS34725_COMMAND_BIT, TCS34725_REG_CONTROL_AGAIN_1)

    def read_luminance(self):
        """Read data back from TCS34725_REG_CDATAL(0x94), 8 bytes, with TCS34725_COMMAND_BIT, (0x80)
        cData LSB, cData MSB, Red LSB, Red MSB, Green LSB, Green MSB, Blue LSB, Blue MSB"""
        data = bus.read_i2c_block_data(TCS34725_DEFAULT_ADDRESS, TCS34725_REG_CDATAL | TCS34725_COMMAND_BIT, 8)
       
        # Convert the data
        cData = (data[1] << 8) + data[0]
        red = (data[3] << 8) + data[2]
        green = (data[5] << 8) + data[4]
        blue = (data[7] << 8) + data[6]
       
        # Calculate luminance
        luminance = (-0.32466 * red) + (1.57837 * green) + (-0.73191 * blue)
       
        # 결과 확인 및 출력
        print("Clear Data Color Luminance : %d lux" % (cData))
        print("Red Color Luminance : %d lux" % (red))
        print("Green Color Luminance : %d lux" % (green))
        print("Blue Color Luminance : %d lux" % (blue))
        print("Ambient Light Luminance : %.2f lux" % (luminance))
        print(" ***************************************************** ")
       
        # 빨간색이 높을 때
        if red > green and red > blue:
            return "Red"
        # 초록색이 높을 때
        elif green > red and green > blue:
            return "Green"
        # 파란색이 높을 때
        elif blue > red and blue > green:
            return "Blue"
        else:
            return "Unknown"

# TCS34725 클래스 인스턴스 생성
tcs34725 = TCS34725()

while True:
    result = tcs34725.read_luminance()
    print("Detected Color:", result)
    time.sleep(1)
