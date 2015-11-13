import threading
# Some serial library will need to be loaded


class Receiver(threading.Thread):

    def __init__(self, connection, work_queue):
        """
        Potentially also need to pass in stuff like which serial port
        to use, timeouts, etc.
        """
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self._stop = threading.Event()
        self.conn = connection

    def run(self):
        while True:
            """
            Code to read a line from the clock serial and perhaps process
            it a bit (remove useless data, add an ID string or something)
            """
            try:
                item_from_serial = self.conn.readline().strip()
                self.work_queue.put(item_from_serial)

            except Exception:
                if self.stopped():
                    return
                else:
                    continue

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()
