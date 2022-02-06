#!/usr/bin/python
# OG Author : Matt Hawkins
# https://forums.raspberrypi.com/viewtopic.php?t=305455
# https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python
# --------------------------------------

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
from digitalio import DigitalInOut


class InvalidPinID(AttributeError):
    pass


class InvalidLineNumber(Exception):
    pass


class LCD:

    def _get_pin(self, pin: int) -> board.Pin:
        try:
            return getattr(board, f'GP{pin}')
        except AttributeError:
            raise InvalidPinID('Pin ID is not valid')

    def _register_pin(self, pin: int) -> DigitalInOut:
        return DigitalInOut(self._get_pin(pin))

    def _toggle_enable(self):
        time.sleep(self.e_delay)
        self.enable_pin.value = True
        time.sleep(self.e_pulse)
        self.enable_pin.value = False
        time.sleep(self.e_delay)

    def _send_byte(self, bits, mode: bool) -> None:
        ''' Send byte to data pins
            bits = data
            mode = True  for character
                    False for command
        '''
        self.register_select_pin.value = mode
        d4 = self.d4_pin
        d5 = self.d5_pin
        d6 = self.d6_pin
        d7 = self.d7_pin

        def reset_pin_values():
            for pin in (d4, d5, d6, d7):
                pin.value = False

        # High bits
        reset_pin_values()
        if bits & 0x10 == 0x10:
            d4.value = True
        if bits & 0x20 == 0x20:
            d5.value = True
        if bits & 0x40 == 0x40:
            d6.value = True
        if bits & 0x80 == 0x80:
            d7.value = True
        self._toggle_enable()

        # Low bits
        reset_pin_values()
        if bits & 0x01 == 0x01:
            d4.value = True
        if bits & 0x02 == 0x02:
            d5.value = True
        if bits & 0x04 == 0x04:
            d6.value = True
        if bits & 0x08 == 0x08:
            d7.value = True
        self._toggle_enable()

    def _initialize_display(self):
        # 110011 Initialize
        self._send_byte(0x33, self.as_cmd)
        # 110010 Initialize
        self._send_byte(0x32, self.as_cmd)
        # 000110 Cursor move direction
        self._send_byte(0x06, self.as_cmd)
        # 001100 Display On, Cursor Off, Blink Off
        self._send_byte(0x0C, self.as_cmd)
        # 101000 Data length, number of lines, font size
        self._send_byte(0x28, self.as_cmd)
        # 000001 Clear display
        self._send_byte(0x01, self.as_cmd)
        time.sleep(self.e_delay)

    def clear(self):
        self._send_byte(0x01, self.as_cmd)

    def show_line(self, message: str, line: int = 1):
        '''
            Sends single-line message to display
            params: message (str)
            params: line (int)
        '''
        # Send string to display
        if line == 1:
            line = self.line_1
        elif line == 2:
            line = self.line_2
        else:
            raise InvalidLineNumber(
                'This is a 16x2 display, right? Choose line 1 or 2')

        print(message)
        width = self.lcd_width
        self._send_byte(line, self.as_cmd)
        for character in message + (' ' * width)[:width+1]:  # len == 16 w/pad
            self._send_byte(ord(character), self.as_chr)

    def show(self, message: str) -> None:
        '''
          Sends multi-line message to display
          params: message (str)
        '''
        line_end = self.lcd_width + 1
        lines = (message[:line_end], message[line_end:])
        for line in lines:
            self.show_line(line)

    def __init__(self,
                 rs_pin: int,
                 e_pin: int,
                 d4_pin: int,
                 d5_pin: int,
                 d6_pin: int,
                 d7_pin: int) -> None:
        self.line_1 = 0x80   # LCD RAM address for the 1st line
        self.line_2 = 0xC0   # LCD RAM address for the 2nd line
        self.lcd_width = 16  # Maximum characters per line
        self.as_chr = 1
        self.as_cmd = 0
        self.e_pulse = 0.0005
        self.e_delay = 0.0005

        self.register_select_pin = self._register_pin(rs_pin)
        self.enable_pin = self._register_pin(e_pin)
        self.d4_pin = self._register_pin(d4_pin)
        self.d5_pin = self._register_pin(d5_pin)
        self.d6_pin = self._register_pin(d6_pin)
        self.d7_pin = self._register_pin(d7_pin)

        for pin in (self.register_select_pin,
                    self.enable_pin,
                    self.d4_pin,
                    self.d5_pin,
                    self.d6_pin,
                    self.d7_pin):
            pin.switch_to_output()

        self._initialize_display()


if __name__ == '__main__':

    try:
        display = LCD(7, 8, 10, 11, 12, 13)
        while True:
            display.show_line('abcdefghilmnopqrstuvwxyz', 1)
            display.show_line('ABCDEFGHIJKLMNOPQRSTUVWXYZ', 2)
            time.sleep(1)
            display.show('This is a multi-line test for my pico')
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        display.clear()
