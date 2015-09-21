#!/usr/bin/python3

from multiprocessing import Queue
import signal
import sys
from transmitter import Transmitter
from receiver import Receiver


__queue = None


def term_handler(signum, frame):
    __queue.put("SHUTDOWN")


if __name__ == '__main__':

    __queue = Queue()

    transmitter = Transmitter(__queue)
    receiver = Receiver(__queue)

    receiver.start()
    transmitter.start()

    signal.signal(signal.SIGTERM, term_handler)

    # Wait until transmitter terminates then kill receiver
    transmitter.join()
    sys.exit(0)
