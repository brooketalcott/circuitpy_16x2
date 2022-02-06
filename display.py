#!/usr/bin/python
#https://forums.raspberrypi.com/viewtopic.php?t=305455
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
 
#import
from machine import Pin
import utime
 
# Define GPIO to LCD mapping
LCD_RS = 7
LCD_E  = 8
LCD_D4 = 10
LCD_D5 = 11
LCD_D6 = 12
LCD_D7 = 13
 
# Define some device constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = 1
LCD_CMD = 0
 
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
 
def main():

  # Initialise display
  lcd_init()
  
 
  while True:
 
    # Send some test
    lcd_string("Pico Pi",LCD_LINE_1)
    lcd_string("16x2 LCD Test",LCD_LINE_2)
 
    utime.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("1234567890",LCD_LINE_1)
    lcd_string("abcdefghijklmnop",LCD_LINE_2)
 
    utime.sleep(3) # 3 second delay
 
    # Send some text
    lcd_string("qrstuvwxyz",LCD_LINE_1)
    lcd_string(":-)",LCD_LINE_2)
 
    utime.sleep(3)
 
    # Send some text
    lcd_string("Thomas Rippon",LCD_LINE_1)
    lcd_string("Learning Pico",LCD_LINE_2)
 
    utime.sleep(3)
 
def lcd_init():
  # Initialise display
  lcd_byte(0x33,LCD_CMD) # 110011 Initialise
  lcd_byte(0x32,LCD_CMD) # 110010 Initialise
  lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
  lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
  lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
  lcd_byte(0x01,LCD_CMD) # 000001 Clear display
  utime.sleep(E_DELAY)
 
def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command
  PinRS = Pin(LCD_RS, Pin.OUT)
  PinRS.value(mode)
  #Pin(LCD_RS, mode) # RS
  PinD4 = Pin(LCD_D4, Pin.OUT)
  PinD5 = Pin(LCD_D5, Pin.OUT)
  PinD6 = Pin(LCD_D6, Pin.OUT)
  PinD7 = Pin(LCD_D7, Pin.OUT)
  
  # High bits
  #Pin(LCD_D4, False)
  PinD4.value(0)
  #Pin(LCD_D5, False)
  PinD5.value(0)
  #Pin(LCD_D6, False)
  PinD6.value(0)
  #Pin(LCD_D7, False)
  PinD7.value(0)
  if bits&0x10==0x10:
    #Pin(LCD_D4, True)
    PinD4.value(1)
  if bits&0x20==0x20:
    #Pin(LCD_D5, True)
    PinD5.value(1)
  if bits&0x40==0x40:
    #Pin(LCD_D6, True)
    PinD6.value(1)
  if bits&0x80==0x80:
    #Pin(LCD_D7, True)
    PinD7.value(1)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
  # Low bits
  #Pin(LCD_D4, False)
  PinD4.value(0)
  #Pin(LCD_D5, False)
  PinD5.value(0)
  #Pin(LCD_D6, False)
  PinD6.value(0)
  #Pin(LCD_D7, False)
  PinD7.value(0)
  if bits&0x01==0x01:
    #Pin(LCD_D4, True)
    PinD4.value(1)
  if bits&0x02==0x02:
    #Pin(LCD_D5, True)
    PinD5.value(1)
  if bits&0x04==0x04:
    #Pin(LCD_D6, True)
    PinD6.value(1)
  if bits&0x08==0x08:
    #Pin(LCD_D7, True)
    PinD7.value(1)
 
  # Toggle 'Enable' pin
  lcd_toggle_enable()
 
def lcd_toggle_enable():
  # Toggle enable
  PinE = Pin(LCD_E, Pin.OUT)
  utime.sleep(E_DELAY)
  #Pin(LCD_E, True)
  PinE.value(1)
  utime.sleep(E_PULSE)
  #Pin(LCD_E, False)
  PinE.value(0)
  utime.sleep(E_DELAY)
 
def lcd_string(message,line):
  # Send string to display
 
  MESSAGE_SPACE = LCD_WIDTH-len(message)
  i=0
  print(message)
  while i<MESSAGE_SPACE:
      message = message + " "
      i+=1 
  lcd_byte(line, LCD_CMD)
  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)
 
if __name__ == '__main__':
 
  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1)