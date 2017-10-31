import threading

class Receiver(threading.Thread):

    def __init__(self, connection, work_queue):
        """
        Potentially also need to pass in stuff like which serial port
        to use, timeouts, etc.
        """
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self._halt = threading.Event()
        self.conn = connection
        self.counter = 0

    def run(self):
        while True:
            """
            Code to read a line from the clock serial and perhaps process
            it a bit (remove useless data, add an ID string or something)
            """
            item_from_serial = self.conn.readline().strip()
            if item_from_serial:
                self.work_queue.put(item_from_serial.decode())

                self.counter= self.counter + 1
                print("Received Data\n")
                print("No of times received = ", self.counter)


            if self.stopped():
                return

    def getLength(self):
        print("No of times received in the RX Calling Thread", self.counter)
        return self.counter


    def stop(self):
        self._halt.set()

    def stopped(self):
        return self._halt.is_set()
