#!/usr/bin/python3

import signal
import queue
from .receiver import Receiver
from .transmitter import Transmitter
from .rockblock import RockBlock
#from .Adafruit_CharLCD import Adafruit_CharLCD as LCD
from .display import Display




import serial



# Raspberry Pi pin configuration:
#lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
#lcd_en        = 24
#lcd_d4        = 23
#lcd_d5        = 17
#lcd_d6        = 21
#lcd_d7        = 22
#lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
#lcd_columns = 16
#lcd_rows    = 2

# Initialize the LCD using the pins above.
#lcd = LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
#                           lcd_columns, lcd_rows, lcd_backlight)


# Print a two line message
#lcd.message('    RockClock\n  Version 1.00')


_queue = None
transmitter = None
receiver = None
display = None


def term_handler(signum, frame):
    global transmitter
    transmitter.stop()


def main():
    global transmitter

    _queue = queue.Queue()

    clock_conn = serial.Serial("/dev/ttyUSB0", 9600, timeout=2)
    print("Clock connection acquired on /dev/ttyUSB0")
    rb = RockBlock("/dev/ttyAMA0")

    transmitter = Transmitter(rb, _queue)
    receiver = Receiver(clock_conn, _queue)

    receiver.start()
    transmitter.start()

    display = Display(receiver)

    display.start()

    signal.signal(signal.SIGTERM, term_handler)

    # Wait until transmitter terminates then kill receiver
    transmitter.join()
    receiver.stop()
    display.stop()
