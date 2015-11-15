#!/usr/bin/python3

import signal
import queue
from transmitter import Transmitter
from receiver import Receiver
from rockblock import RockBlock

import serial


_queue = None
transmitter = None
receiver = None


def term_handler(signum, frame):
    transmitter.stop()


if __name__ == '__main__':

    _queue = queue.Queue()

    clock_conn = serial.Serial("/dev/ttyUSB0", 9600, timeout=2)
    rb = RockBlock("/dev/ttyAMA0")

    transmitter = Transmitter(rb, _queue)
    receiver = Receiver(clock_conn, _queue)

    receiver.start()
    transmitter.start()

    signal.signal(signal.SIGTERM, term_handler)

    # Wait until transmitter terminates then kill receiver
    transmitter.join()
    receiver.stop()
