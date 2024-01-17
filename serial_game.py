import serial.tools
import serial.tools.list_ports as list_ports


class serial_manager:
    def __init__(self, baud=115200, port="dev/tty.usbmodem11101", sleep=10):
        print("Attempting to open Serial connection")
        self.ardu = serial.Serial()
        self.ardu.baudrate = baud
        self.ardu.port = port
        self.ardu.open()
        self.serialConnected = False
        time.sleep(sleep)
        if self.ardu.is_open:
            print("Success!")
            self.serialConnected = True

    def output_to_serial(self, space, player):
        colorr = {1: {"r": 50, "g": 150, "b": 50}, 2: {"r": 200, "g": 100, "b": 0}}
        text = f"{space}, {colorr[player]['r']}, {colorr[player]['g']}, {colorr[player]['b']}"
        print(text)
        self.ardu.write(f"<setPixelColor, {text}>\0".encode())

    def clear_board_serial(self):
        colorr = {1: {"r": 0, "g": 0, "b": 0}}
        self.ardu.write(f"<s, {text}>\0".encode())
        for i in range(256):
            text = f"{i}, {colorr[1]['r']}, {colorr[1]['g']}, {colorr[1]['b']}"
            time.sleep(1)
            self.ardu.write(f"<setPixelColor, {text}>\0".encode())
