#!/usr/bin/python3

import signal
import queue
from transmitter import Transmitter
from receiver import Receiver

import serial


_queue = None


def term_handler(signum, frame):
    _queue.put("SHUTDOWN")


if __name__ == '__main__':

    _queue = queue.Queue()

    clock_conn = serial.Serial("/dev/ttyUSB0", 9600, timeout=2)

    transmitter = Transmitter(_queue)
    receiver = Receiver(clock_conn, _queue)

    receiver.start()
    transmitter.start()

    signal.signal(signal.SIGTERM, term_handler)

    # Wait until transmitter terminates then kill receiver
    transmitter.join()
    receiver.stop()
