import serial
import numpy as np


class LED_Matrix(serial.Serial):
    def __init__(
        self,
        port=None,
        baudrate=9600,
        bytesize=8,
        parity="N",
        stopbits=1,
        timeout=None,
        xonxoff=False,
        rtscts=False,
        write_timeout=None,
        dsrdtr=False,
        inter_byte_timeout=None,
        rows=None,
        cols=None,
    ):
        super().__init__(
            port,
            baudrate,
            bytesize,
            parity,
            stopbits,
            timeout,
            xonxoff,
            rtscts,
            write_timeout,
            dsrdtr,
            inter_byte_timeout,
        )
        self.rows = rows
        self.cols = cols

    def reconnect(self):
        while self.serialConnected == False:
            self.open()
            if self.is_open:
                self.serialConnected = True
                return True
            else:
                self.close()
                print(f"{self.reAttempts=}, {self.arduin}")
                self.reAttempts = self.reAttempts - 1
            if reAttempts <= -1:
                print(f"Failed to connect")
                self.serialConnect = False
                return False

    def to_bitmap(self, array=None):
        sub = ""
        for i in array:
            sub += str(np.flip(i))
        sub = sub.replace("2", "1")
        sub = sub.replace(" ", ",")
        sub = sub.replace("][", "],[")
        sub = "[" + sub + "]"
        sub = sub.replace("[", "{")
        sub = sub.replace("]", "}")
        return sub

    def output_to_serial(self, row, col, board):
        prefix = "A"
        self.write(f"{prefix}-{row}-{col}-{board}\n".encode())


if __name__ == "__main__":
    print("Arduino Time")
