from multiprocessing import Process
import time
# Some serial library will need to be loaded


class Receiver(Process):

    def __init__(self, work_queue):
        """
        Potentially also need to pass in stuff like which serial port
        to use, timeouts, etc.
        """
        Process.__init__(self)
        self.daemon = True
        self.work_queue = work_queue

    def run(self):
        while True:
            """
            Code to read a line from the clock serial and perhaps process
            it a bit (remove useless data, add an ID string or something)
            """
            item_from_serial = None  # Dummy
            self.work_queue.put(item_from_serial)

            time.sleep(30)  # Dummy delay
