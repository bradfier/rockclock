import threading
import time
from .rockblock import RockBlockSignalException, RockBlockException
from queue import Empty


class Transmitter(threading.Thread):

    def __init__(self, rockblock, work_queue):
        threading.Thread.__init__(self)

        self.work_queue = work_queue
        self.transmit_buffer = list()
        self.rockblock = rockblock
        self._halt = threading.Event()
        self.last_time = time.monotonic()
        self._transmit = threading.Event()

    def transmit(self):
        """
        In here we should call whatever is required to batch the times
        from the clock into a transmission block, and send it to the
        modem.
        """

        temp = []
        while len(self.transmit_buffer) > 0:
            remaining_space = 338 - self.buflength(temp)

            if remaining_space > (len(self.transmit_buffer[0]) + 1):
                temp.append(self.transmit_buffer.pop(0))

        if len(temp) > 0:
            data = "\n".join(temp)
            try:
                print("Transmitting data:")
                print(data)
                result = self.rockblock.send_message(data)

                if not result:
                    print("Transmission error, backing off.")
                    self.transmit_buffer = temp + self.transmit_buffer
                    time.sleep(30)
                    return

            except RockBlockSignalException:
                print("Low signal, backing off.")
                self.transmit_buffer = temp + self.transmit_buffer
                time.sleep(30)
                return
            except RockBlockException:
                print("Transmission error")
                self.transmit_buffer = temp + self.transmit_buffer
                time.sleep(30)
                return

        self._transmit.clear()

    def run(self):
        while True:
            item = None
            try:
                item = self.work_queue.get(timeout=2)
            except(Empty):
                pass

            if item:
                self.transmit_buffer.append(item)
                self.last_time = time.monotonic()

            delta = time.monotonic() - self.last_time

            if self.work_queue.empty() and len(self.transmit_buffer) > 0:
                if (delta > 30) or (len(self.transmit_buffer) > 1):
                    self._transmit.set()

            if self._transmit.is_set() and self.work_queue.empty():
                self.transmit()

            if self.stopped():
                while len(self.transmit_buffer) > 0:
                    self.transmit()
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
