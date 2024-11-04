import smbus
import RPi.GPIO as GPIO
import time

# Define GPIO pin for pulse sensor
pulse_pin = 17

# Define I2C address and LCD size
lcd_i2c_address = 0x27
lcd_columns = 16
lcd_rows = 2

# Initialize I2C bus
bus = smbus.SMBus(1)  # Use /dev/i2c-1

# Function to send commands to LCD
def lcd_byte(bits, mode):
    bits_high = mode | (bits & 0xF0) | 0x08  # High bits
    bits_low = mode | ((bits << 4) & 0xF0) | 0x08  # Low bits

    # Write high bits
    bus.write_byte(lcd_i2c_address, bits_high)
    lcd_toggle_enable(bits_high)

    # Write low bits
    bus.write_byte(lcd_i2c_address, bits_low)
    lcd_toggle_enable(bits_low)

# Function to toggle Enable
def lcd_toggle_enable(bits):
    time.sleep(0.0005)
    bus.write_byte(lcd_i2c_address, (bits | 0x04))
    time.sleep(0.0005)
    bus.write_byte(lcd_i2c_address, (bits & ~0x04))
    time.sleep(0.0005)

# Function to initialize LCD
def lcd_init():
    lcd_byte(0x33, 0) # 110011 Initialise
    lcd_byte(0x32, 0) # 110010 Initialise
    lcd_byte(0x06, 0) # 000110 Cursor move direction
    lcd_byte(0x0C, 0) # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, 0) # 101000 Data length, number of lines, font size
    lcd_byte(0x01, 0) # 000001 Clear display
    time.sleep(0.0005)

# Function to clear LCD
def lcd_clear():
    lcd_byte(0x01, 0) # 000001 Clear display
    time.sleep(0.0005)

# Function to send string to LCD
def lcd_string(message, line):
    message = message.ljust(lcd_columns, " ")
    lcd_byte(line, 0)
    for i in range(lcd_columns):
        lcd_byte(ord(message[i]), 1)

# Main function
def main():
    last_time = 0
    pulse_count = 0
    interval = 10  # 10 seconds

    # Initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pulse_pin, GPIO.IN)

    # Initialize LCD
    lcd_init()

    while True:
        current_time = time.time()

        # Measure heart rate every 60 seconds
        if current_time - last_time >= interval:
            bpm = pulse_count   # Calculate BPM
            print("Heart Rate:", bpm, "BPM")

            lcd_clear()
            lcd_string("Heart Rate:", 0x80)
            lcd_string(str(bpm) + " BPM", 0xC0)

            # Reset pulse count and update last time
            pulse_count = 0
            last_time = current_time

        # Read pulse sensor value
        pulse_value = GPIO.input(pulse_pin)
        if pulse_value == GPIO.HIGH:
            pulse_count += 1
            time.sleep(0.05)  # Debouncing delay

if __name__ == "__main__":
    main()
