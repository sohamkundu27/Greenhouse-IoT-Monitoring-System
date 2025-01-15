#include <wiringPi.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h> // For usleep() micro second level delays

// GPIO pin configuration
#define LCD_RS 7  // Register Select pin
#define LCD_E 8   // Enable pin
#define LCD_D4 25 // Data pin 4
#define LCD_D5 26 // Data pin 5
#define LCD_D6 19 // Data pin 6
#define LCD_D7 13 // Data pin 7

// LCD constants
#define LCD_WIDTH 16 // Maximum characters per line
#define LCD_CHR 1    // Sending data
#define LCD_CMD 0    // Sending command
#define E_PULSE 500  // Enable pulse duration in microseconds
#define E_DELAY 500  // Delay between operations in microseconds

// Function declarations
void lcd_init();
void lcd_byte(int bits, int mode);
void lcd_toggle_enable();
void lcd_string(const char *message, int line);

int main()
{
    // Initialize WiringPi
    if (wiringPiSetup() == -1)
    {
        printf("WiringPi setup failed. Exiting...\n");
        return 1;
    }

    // Set GPIO pins as output
    pinMode(LCD_RS, OUTPUT);
    pinMode(LCD_E, OUTPUT);
    pinMode(LCD_D4, OUTPUT);
    pinMode(LCD_D5, OUTPUT);
    pinMode(LCD_D6, OUTPUT);
    pinMode(LCD_D7, OUTPUT);

    // Initialize the LCD
    lcd_init();

    // Display messages
    lcd_string("Temp: 72F", 1);     // Line 1
    lcd_string("Humidity: 45%", 2); // Line 2

    delay(5000); // Keep the message on the screen for 5 seconds

    return 0;
}

// Function to initialize the LCD
void lcd_init()
{
    lcd_byte(0x33, LCD_CMD); // Initialize
    lcd_byte(0x32, LCD_CMD); // Set to 4-bit mode
    lcd_byte(0x28, LCD_CMD); // 2 lines, 5x7 matrix
    lcd_byte(0x0C, LCD_CMD); // Display on, no cursor
    lcd_byte(0x06, LCD_CMD); // Increment cursor
    lcd_byte(0x01, LCD_CMD); // Clear display
    usleep(E_DELAY);
}

// Function to send a byte to the LCD
void lcd_byte(int bits, int mode)
{
    // Set mode (command or data)
    digitalWrite(LCD_RS, mode);

    // Send high nibble
    digitalWrite(LCD_D4, (bits & 0x10) == 0x10);
    digitalWrite(LCD_D5, (bits & 0x20) == 0x20);
    digitalWrite(LCD_D6, (bits & 0x40) == 0x40);
    digitalWrite(LCD_D7, (bits & 0x80) == 0x80);
    lcd_toggle_enable();

    // Send low nibble
    digitalWrite(LCD_D4, (bits & 0x01) == 0x01);
    digitalWrite(LCD_D5, (bits & 0x02) == 0x02);
    digitalWrite(LCD_D6, (bits & 0x04) == 0x04);
    digitalWrite(LCD_D7, (bits & 0x08) == 0x08);
    lcd_toggle_enable();
}

// Function to toggle the enable pin
void lcd_toggle_enable()
{
    usleep(E_DELAY);
    digitalWrite(LCD_E, 1);
    usleep(E_PULSE);
    digitalWrite(LCD_E, 0);
    usleep(E_DELAY);
}

// Function to display a string on the LCD
void lcd_string(const char *message, int line)
{
    if (line == 1)
    {
        lcd_byte(0x80, LCD_CMD); // Line 1
    }
    else if (line == 2)
    {
        lcd_byte(0xC0, LCD_CMD); // Line 2
    }

    // Send each character
    for (int i = 0; i < LCD_WIDTH && message[i] != '\0'; i++)
    {
        lcd_byte(message[i], LCD_CHR);
    }
}