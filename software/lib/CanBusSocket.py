"""
Class to interface with a CAN bus using the SocketCAN interface.

Dependencies:
- string: Python built-in module for string operations.
- time: Python built-in module for time-related functions.
- can: Python library for interfacing with Controller Area Network (CAN) bus interfaces.
  Install with: pip install python-can
- os: Python built-in module for interacting with the operating system.

Usage:
1. Create an instance of CanBusSocket by providing the channel, bustype, and bitrate.
2. Optionally, set up the device with the setup method.
3. Send messages using sendMessage method.
4. Optionally, shut down the device with the shutdown method.
"""

import os
import time
import can


class CanBusSocket:
    def __init__(
        self, channel: str = "can0", bustype: str = "socketcan", bitrate: int = 1000000
    ):
        """
        Initialize the CanBusSocket instance with channel, bustype, and bitrate.

        Parameters:
            channel (str): CAN bus channel.
            bustype (str): Type of CAN bus interface.
            bitrate (int): Bitrate for the CAN bus communication.
        """
        self.channel = channel
        self.bustype = bustype
        self.bitrate = bitrate

    def set_channel(self, channel):
        """
        Set the channel.

        Parameters:
            channel (str): CAN bus channel.
        """
        self.channel = channel

    def set_bitrate(self, bitrate):
        """
        Set the bitrate.

        Parameters:
            bitrate (int): Bitrate for CAN communication.
        """
        self.bitrate = bitrate

    def setup(self):
        """
        Set up the CAN bus socket.
        """
        os.system(f"sudo ifconfig {self.channel} down")
        os.system(f"sudo ip link set {self.channel} type can bitrate {self.bitrate}")
        os.system(f"sudo ifconfig {self.channel} txqueuelen {self.bitrate}")
        os.system(f"sudo ifconfig {self.channel} up")

    def shutdown(self):
        """
        Shut down the CAN bus socket.
        """
        os.system(f"sudo ifconfig {self.channel} down")

    def sendMessage(self, id, data):
        """
        Send a CAN message.

        Parameters:
            id: Message ID.
            data: Message data.
        """
        self.bus = can.interface.Bus(channel=self.channel, bustype=self.bustype)
        msg = can.Message(id, data)
        self.bus.send(msg)
        time.sleep(0.001)
        print("Send frame: ", msg, "\n")
        while True:
            msg = self.bus.recv(10.0)
            if msg is None:
                print("No message was received")
            else:
                print(f"Received frame: \n{msg}\n")
                return msg
