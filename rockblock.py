# Copyright 2015 Richard Bradfield <bradfirj@fstab.me>
#
# This file is part of Rockclock.
#
#    Rockclock is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Rockclock is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Rockclock.  If not, see <http://www.gnu.org/licenses/>.
#
# Adapted from Makersnake's pyRockBlock repo (APLv2), available at:
# https://github.com/MakerSnake/pyRockBlock

import serial
import time


# Wrapper to quickly test the connection hasn't gone away
def connected(func):
    def wrapper(self, *args, **kwargs):
        if (self.conn is None or self.conn.isOpen() is False):
            raise RockBlockException("Lost connection to RockBlock")
        return func(self, *args, **kwargs)

    return wrapper


class RockBlockException(Exception):
    pass


class RockBlockSignalException(Exception):
    pass


class RockBlock(object):

    def __init__(self, handle, retries=5, timeout=10):
        self.handle = handle
        self.retries = retries
        self.timeout = timeout

        try:
            self.conn = serial.Serial(self.handle, 19200, timeout=self.timeout)

            # Allow 60s for initial startup
            # self.conn.timeout = 60
            self.ping()

            if not self.ping():
                self.conn.close()
                raise RockBlockException()

            self.conn.timeout = self.timeout

        except (Exception):
            raise RockBlockException()

    @connected
    def ping(self):
        self._command("AT")

        if self.conn.readline().strip() == b'AT':
            if self.conn.readline().strip() == b'OK':
                return True

        return False

    @connected
    def send_message(self, msg):

        for r in range(self.retries):
            if self.get_signal_strength() < 2:
                print("Waiting for signal.")
                time.sleep(10)
                continue

            if not self._queue_msg(msg):
                raise RockBlockException()

            if not self._initiate_session():
                print("Transmission failure")
                time.sleep(10)
                continue

            return True

        print("Retries exhausted")
        return False

    @connected
    def get_signal_strength(self):
        self._command("AT+CSQ")

        # Signal acquisition can take a _long_ time
        self.conn.timeout = 30

        if self.conn.readline().strip() == b"AT+CSQ":
            response = self.conn.readline().strip()
            self.conn.timeout = self.timeout

            if response.find(b"+CSQ") >= 0:
                self.conn.readline()  # OK
                self.conn.readline()  # Blank

                if len(response) == 6:
                    return int(response[5:])

        raise RockBlockException()

    def _command(self, string):
        command = string + '\r'
        self.conn.write(command.encode("ASCII"))

    # "isNetworkTimeValid" in the MakerSnake code
    # Waits until the SBD modem has synchronised its internal clock
    @connected
    def _time_sync(self, attempts=5, delay=3):
        while attempts != 0:
            self._command("AT-MSSTM")

            if self.conn.readline().strip() == b'AT-MSSTM':
                response = self.conn.readline().strip()

                if response.find(b'-MSSTM') == 0:
                    self.conn.readline()  # Blank
                    self.conn.readline()  # OK

                    if len(response) == 16:
                        return True

            attempts -= 1
            time.sleep(delay)

        return False

    @connected
    def _queue_msg(self, msg):
        encoded_message = msg.encode("ASCII")

        length = len(encoded_message)

        if length > 340:
            raise RockBlockException("Message too long")

        command = "AT+SBDWB=" + str(length)
        self._command(command)

        if self.conn.readline().strip() == command.encode("ASCII"):
            if self.conn.readline().strip() == b'READY':
                checksum = 0

                for char in encoded_message:
                    checksum = checksum + char

                self.conn.write(encoded_message)

                self.conn.write(chr(checksum >> 8).encode())
                self.conn.write(chr(checksum & 0xFF).encode())

                self.conn.readline().strip()

                result = False

                if self.conn.readline().strip() == b'0':
                    result = True

                self.conn.readline()  # Blank
                self.conn.readline()  # OK

                return result

        return False

    @connected
    def _initiate_session(self):
        command = "AT+SBDIX"
        self._command(command)

        if self.conn.readline().strip() == command.encode("ASCII"):
            response = self.conn.readline().strip()
            response = response.decode("ASCII")

            if "+SBDIX:" in response:
                self.conn.readline()
                self.conn.readline()

                response = response.replace("+SBDIX: ", "")

                parts = response.split(",")
                moStatus = int(parts[0])
                # moMsn = int(parts[1])
                # mtStatus = int(parts[2])
                # mtMsn = int(parts[3])
                # mtLength = int(parts[4])
                # mtQueued = int(parts[5])

                if moStatus <= 4:

                    # Clear buffer

                    return True

        return False
