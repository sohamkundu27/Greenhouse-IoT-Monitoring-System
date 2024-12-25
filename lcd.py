import RPi.GPIO as GPIO
from time import sleep

# Define GPIO to LCD mapping
LCD_RS = 7   # Register Select pin
LCD_E = 8    # Enable pin
LCD_D4 = 25  # Data pin 4
LCD_D5 = 26  # Data pin 5
LCD_D6 = 19  # Data pin 6
LCD_D7 = 13  # Data pin 7

# LCD constants
LCD_WIDTH = 16  # Characters per line
LCD_CHR = True  # Send data
LCD_CMD = False  # Send command

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005

def lcd_init():
    """Initialize the LCD"""
    lcd_byte(0x33, LCD_CMD)  # Initialize
    lcd_byte(0x32, LCD_CMD)  # Set to 4-bit mode
    lcd_byte(0x28, LCD_CMD)  # 2 line, 5x7 matrix
    lcd_byte(0x0C, LCD_CMD)  # Display on, no cursor
    lcd_byte(0x06, LCD_CMD)  # Increment cursor
    lcd_byte(0x01, LCD_CMD)  # Clear display
    sleep(E_DELAY)

def lcd_byte(bits, mode):
    """Send byte to data pins"""
    GPIO.output(LCD_RS, mode)  # RS

    # High bits
    GPIO.output(LCD_D4, bool(bits & 0x10))
    GPIO.output(LCD_D5, bool(bits & 0x20))
    GPIO.output(LCD_D6, bool(bits & 0x40))
    GPIO.output(LCD_D7, bool(bits & 0x80))

    # Toggle enable
    lcd_toggle_enable()

    # Low bits
    GPIO.output(LCD_D4, bool(bits & 0x01))
    GPIO.output(LCD_D5, bool(bits & 0x02))
    GPIO.output(LCD_D6, bool(bits & 0x04))
    GPIO.output(LCD_D7, bool(bits & 0x08))

    # Toggle enable
    lcd_toggle_enable()

def lcd_toggle_enable():
    """Toggle the enable pin"""
    sleep(E_DELAY)
    GPIO.output(LCD_E, True)
    sleep(E_PULSE)
    GPIO.output(LCD_E, False)
    sleep(E_DELAY)

def lcd_string(message, line):
    """Display string on LCD"""
    if line == 1:
        lcd_byte(0x80, LCD_CMD)
    elif line == 2:
        lcd_byte(0xC0, LCD_CMD)

    for char in message.ljust(LCD_WIDTH, " "):
        lcd_byte(ord(char), LCD_CHR)

def main():
    """Main function"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    lcd_init()

    try:
        while True:
            # Clear the first line before updating
            lcd_string(" " * LCD_WIDTH, 1)
            lcd_string("STATUS: ONLINE", 1)
            sleep(100)
    except KeyboardInterrupt:
        lcd_byte(0x01, LCD_CMD)  # Clear the LCD
        GPIO.cleanup()

if __name__ == "__main__":
    main()
