# CircuitPy_16x2
## 16x2 display module for circutpython on RaspberryPi Pico

I was looking to use a 16x2 LCD screen with my raspberry pico and like lordrippon I was looking for a simple wiring setup and lacked a backpack for my pico. 

A few of my pico project components are using circutpython instead of microPython though so some of the modules needed to be replaced for compatability

And why not see if I can't make this API a little easier to use?

credit: 
- https://forums.raspberrypi.com/viewtopic.php?t=305455
- https://www.raspberrypi-spy.co.uk/2012/07/16x2-lcd-module-control-using-python
- https://forums.raspberrypi.com/viewtopic.php?p=96361#p96361


### Usage
Copy display.py into the lib folder on your pico then in your code.py or main.py:
```
import display


lcd = display.LCD(7,8,10,11,12,13)
```

or 

```
import display
lcd = display.LCD(rs_pin=7, e_pin=8, d4_pin=10, d5_pin=11, d6_pin=12, d7_pin=13)
```

then send your messages where desired

```
import display

lcd = display.LCD(7,8,10,11,12,13)

lcd.show('Hi Mom! This is a multiline message')

lcd.show_line('Or I can',1)
lcd.show_line('pick and choose',2)
```
