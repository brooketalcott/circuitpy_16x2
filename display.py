#!/usr/bin/python
# https://forums.raspberrypi.com/viewtopic.php?t=305455
# The wiring for the LCD is as follows:
# 1 : GND
# 2 : 5V
# 3 : Contrast (0-5V)*
# 4 : RS (Register Select)
# 5 : R/W (Read Write)       - GROUND THIS PIN
# 6 : Enable or Strobe
# 7 : Data Bit 0             - NOT USED
# 8 : Data Bit 1             - NOT USED
# 9 : Data Bit 2             - NOT USED
# 10: Data Bit 3             - NOT USED
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V**
# 16: LCD Backlight GND

import time
import board
from digitalio import DigitalInOut, Direction

# Define GPIO to LCD mapping
LCD_RS = DigitalInOut(board.GP7)
LCD_E = DigitalInOut(board.GP8)
LCD_D4 = DigitalInOut(board.GP10)
LCD_D5 = DigitalInOut(board.GP11)
LCD_D6 = DigitalInOut(board.GP12)
LCD_D7 = DigitalInOut(board.GP13)

for pin in [LCD_RS, LCD_E, LCD_D4, LCD_D5, LCD_D6, LCD_D7]:
    pin.direction = Direction.OUTPUT


# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = 1
LCD_CMD = 0
LCD_LINE_1 = 0x80  # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0  # LCD RAM address for the 2nd line

# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005


def main():

    # Initialise display
    lcd_init()

    while True:

        lcd_string("abcdefghijk", LCD_LINE_1)
        lcd_string("LMNOPQRSTUV", LCD_LINE_2)
        time.sleep(1)
        lcd_string("1234567891011", LCD_LINE_1)
        lcd_string("pico test", LCD_LINE_2)
        time.sleep(1)


def lcd_init():
    # Initialise display
    lcd_byte(0x33, LCD_CMD)  # 110011 Initialise
    lcd_byte(0x32, LCD_CMD)  # 110010 Initialise
    lcd_byte(0x06, LCD_CMD)  # 000110 Cursor move direction
    lcd_byte(0x0C, LCD_CMD)  # 001100 Display On,Cursor Off, Blink Off
    lcd_byte(0x28, LCD_CMD)  # 101000 Data length, number of lines, font size
    lcd_byte(0x01, LCD_CMD)  # 000001 Clear display
    time.sleep(E_DELAY)


def lcd_byte(bits, mode):
    # Send byte to data pins
    # bits = data
    # mode = True  for character
    #        False for command
    PinRS = LCD_RS
    PinRS.value = mode
    PinD4 = LCD_D4
    PinD5 = LCD_D5
    PinD6 = LCD_D6
    PinD7 = LCD_D7

    # High bits
    PinD4.value = False
    PinD5.value = False
    PinD6.value = False
    PinD7.value = False
    if bits & 0x10 == 0x10:
        PinD4.value = True
    if bits & 0x20 == 0x20:
        PinD5.value = True
    if bits & 0x40 == 0x40:
        PinD6.value = True
    if bits & 0x80 == 0x80:
        PinD7.value = True

    # Toggle 'Enable' pin
    lcd_toggle_enable()

    # Low bits
    PinD4.value = False
    PinD5.value = False
    PinD6.value = False
    PinD7.value = False
    if bits & 0x01 == 0x01:
        PinD4.value = True
    if bits & 0x02 == 0x02:
        PinD5.value = True
    if bits & 0x04 == 0x04:
        PinD6.value = True
    if bits & 0x08 == 0x08:
        PinD7.value = True

    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_toggle_enable():
    # Toggle enable
    PinE = LCD_E
    time.sleep(E_DELAY)
    PinE.value = True
    time.sleep(E_PULSE)
    PinE.value = False
    time.sleep(E_DELAY)


def lcd_string(message, line):
    # Send string to display

    MESSAGE_SPACE = LCD_WIDTH-len(message)
    i = 0
    print(message)
    while i < MESSAGE_SPACE:
        message = message + " "
        i += 1
    lcd_byte(line, LCD_CMD)
    for i in range(LCD_WIDTH):
        lcd_byte(ord(message[i]), LCD_CHR)


if __name__ == '__main__':

    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        lcd_byte(0x01, LCD_CMD)
        lcd_string("Goodbye!", LCD_LINE_1)
