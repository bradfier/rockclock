#!/usr/bin/python3

import threading
#from .transmitter import Transmitter
from .receiver import Receiver
#from queue import Empty
from .Adafruit_CharLCD import Adafruit_CharLCD as LCD

#Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Initialize the LCD using the pins above.
lcd = LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

class Display(threading.Thread):

    def __init__(self, counter):
        """
        Display Code.
        """
        threading.Thread.__init__(self)
#        self.work_queue = work_queue
        self._halt = threading.Event()
#        self.test = Receiver
#        self.conn = connection
        self.counter = counter

        times = self.counter
        lcd.home()
        lcd.message('    RockClock\n  Version 1.00')


    def run(self):
        while True:
            """
            Code to process status and display on screen
            """
 #           times2 = Receiver.getLength()
 #           print (" Display Thread run ", self.counter)


#            temp = []
#            remaining_space = self.buflength(temp)
#            print (remaining_space)

            timesTranmitted = 0

            # Print a two line message
            #if timesReceived > 0
#            lcd.clear()
            lcd.home()
#           lcd.message('Display  Running')
#            print("updating display")


            if self.stopped():
                return


    def stop(self):
        self._halt.set()

    def stopped(self):
        return self._halt.is_set()


    def buflength(self, buf):
        length = 0
        for item in buf:
            length += len(item)

        return length
