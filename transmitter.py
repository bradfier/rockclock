from multiprocessing import Process
import signal


class Transmitter(Process):

    def __init__(self, work_queue):
        Process.__init__(self)

        self.work_queue = work_queue
        self.transmit_buffer = list()

        signal.signal(signal.SIGALRM, self.alarm_handler)

    def alarm_handler(self, *args):
        self.work_queue.put("SEND")
        print("Signaling transmit")
        signal.alarm(0)

    def transmit(self, buf):
        """
        In here we should call whatever is required to batch the times
        from the clock into a transmission block, and send it to the
        modem.
        """
        for line in buf:
            print(line)

        del buf[:]

    def run(self):
        while True:
            item = self.work_queue.get()

            if item == "SEND":
                self.transmit(self.transmit_buffer)
                continue
            elif item == "SHUTDOWN":
                self.transmit(self.transmit_buffer)
                print("TERMINATING")
                return
            else:
                self.transmit_buffer.append(item)
                if len(self.transmit_buffer) > 3:
                    self.transmit(self.transmit_buffer)
                    continue

                signal.alarm(180)
