from CanBusGsUsb import CanBusGsUsb
import sys


class ProtocolV2(CanBusGsUsb):
    # Attributes
    BASE_ADDR_ID = 0x140

    ADDR_READ_POSITION_LOOP_KP = 0x30
    ADDR_READ_POSITION_LOOP_KI = 0x31
    ADDR_READ_SPEED_LOOP_KP = 0x32
    ADDR_READ_SPEED_LOOP_KI = 0x33
    ADDR_READ_CURRENT_LOOP_KP = 0x34
    ADDR_READ_CURRENT_LOOP_KI = 0x35

    ADDR_WRITE_POSITION_LOOP_KP_TO_RAM = 0x36
    ADDR_WRITE_POSITION_LOOP_KI_TO_RAM = 0x37
    ADDR_WRITE_SPEED_LOOP_KP_TO_RAM = 0x38
    ADDR_WRITE_SPEED_LOOP_KI_TO_RAM = 0x39
    ADDR_WRITE_CURRENT_LOOP_KP_TO_RAM = 0x3A
    ADDR_WRITE_CURRENT_LOOP_KI_TO_RAM = 0x3B

    ADDR_WRITE_POSITION_LOOP_KP_TO_ROM = 0x3C
    ADDR_WRITE_POSITION_LOOP_KI_TO_ROM = 0x3D
    ADDR_WRITE_SPEED_LOOP_KP_TO_ROM = 0x3E
    ADDR_WRITE_SPEED_LOOP_KI_TO_ROM = 0x3F
    ADDR_WRITE_CURRENT_LOOP_KP_TO_ROM = 0x40
    ADDR_WRITE_CURRENT_LOOP_KI_TO_ROM = 0x41

    ADDR_READ_ACCELERATION = 0x42
    ADDR_WRITE_ACCELERATION_TO_RAM = 0x43

    ADDR_READ_MULTITURN_ENCODER_POSITION = 0x60
    ADDR_READ_MULTITURN_ENCODER_ORIGINAL_POSITION = 0x61
    ADDR_READ_MULTITURN_ENCODER_OFFSET = 0x62
    ADDR_WRITE_MULTITURN_ENCODER_VALUES_TO_ROM_AS_MOTOR_ZERO = 0x63
    ADDR_WRITE_MULTITURN_ENCODER_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO = 0x64

    ADDR_READ_SINGLETURN_ENCODER_DATA = 0x90
    ADDR_WRITE_ENCODER_VALUES_TO_ROM_AS_MOTOR_ZERO = 0x91
    ADDR_WRITE_SINGLETURN_ENCODER_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO = 0x19
    ADDR_READ_MULTITURN_ANGLE = 0x92
    ADDR_READ_SINGLE_CIRCLE_ANGLE = 0x94

    ADDR_READ_MOTOR_STATUS_1_ERROR_FLAG = 0x9A
    ADDR_READ_MOTOR_STATUS_2 = 0x9C
    ADDR_READ_MOTOR_STATUS_3 = 0x9D

    ADDR_MOTOR_OFF = 0x80
    ADDR_STOP = 0x81
    ADDR_RUNNING = 0x88

    ADDR_TORQUE_CLOSED_LOOP_CONTROL = 0xA1
    ADDR_SPEED_CLOSED_LOOP_CONTROL = 0xA2
    ADDR_POSITION_MULTITURN_CLOSED_LOOP_CONTROL = 0xA3
    ADDR_POSITION_MULTITURN_SPEED_CLOSED_LOOP_CONTROL = 0xA4
    ADDR_POSITION_SINGLETURN_DIRECTION_CLOSED_LOOP_CONTROL = 0xA5
    ADDR_POSITION_SINGLETURN_SPEED_DIRECTION_CLOSED_LOOP_CONTROL = 0xA6
    ADDR_POSITION_MULTITURN_INCREMENTAL_CLOSED_LOOP_CONTROL = 0xA7
    ADDR_POSITION_MULTITURN_INCREMENTAL_SPEED_CLOSED_LOOP_CONTROL = 0xA8

    ADDR_READ_RUNNING_MODE = 0x70
    ADDR_READ_POWER_VALUE = 0x71
    ADDR_READ_BATTERY_VOLTAGE = 0x72
    ADDR_FEEDFORWARD_SETTING = 0x73
    ADDR_SYSTEM_RESET = 0x76
    ADDR_BRAKE_OPENING = 0x77
    ADDR_BRAKE_CLOSE = 0x78
    ADDR_CAN_ID_SETTING_AND_READING = 0x79

    def __init__(self, id: int, reducer_ratio: int, can_bus: CanBusGsUsb):
        self.id = id
        self.reducer_ratio = reducer_ratio
        self.can_bus = can_bus

    def read_position_loop_Kp(self, debug=None):
        """
        Reads the current Position loop KP parameters from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x30)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x30)
        - DATA[1-4]: Position loop Kp parameters (Q24 format, converted from float)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - position_loop_KP: Position loop KP parameters (float).
        """
        # Send command to read the current Position loop KP parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_POSITION_LOOP_KP,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract Position loop KP parameters from the response and convert from Q24 to float
        position_loop_KP_q24 = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        position_loop_KP = (
            position_loop_KP_q24 / 16777216.0
        )  # Conversion from Q24 to float

        # Print debug information if enabled
        if debug:
            print(f"Position loop KP parameters: {position_loop_KP}")

        return position_loop_KP

    def read_position_loop_Ki(self, debug=None):
        """
        Reads the current Position loop Ki parameters from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x31)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x31)
        - DATA[1-4]: Position loop Ki parameters (Q24 format, converted from float)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - position_loop_KI: Position loop Ki parameters (float).
        """
        # Send command to read the current Position loop Ki parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_POSITION_LOOP_KI,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract Position loop Ki parameters from the response and convert from Q24 to float
        position_loop_KI_q24 = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        position_loop_KI = (
            position_loop_KI_q24 / 16777216.0
        )  # Conversion from Q24 to float

        # Print debug information if enabled
        if debug:
            print(f"Position loop KI parameters: {position_loop_KI}")

        return position_loop_KI

    def read_speed_loop_Kp(self, debug=None):
        """
        Reads the current Speed loop KP parameters from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x32)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x32)
        - DATA[1-4]: Speed loop KP parameters (Q24 format, converted from float)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - speed_loop_KP: Speed loop KP parameters (float).
        """
        # Send command to read the current Speed loop KP parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_SPEED_LOOP_KP,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract Speed loop KP parameters from the response and convert from Q24 to float
        speed_loop_KP_q24 = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        speed_loop_KP = speed_loop_KP_q24 / 16777216.0  # Conversion from Q24 to float

        # Print debug information if enabled
        if debug:
            print(f"Speed loop KP parameters: {speed_loop_KP}")

        return speed_loop_KP

    def read_speed_loop_Ki(self, debug=None):
        """
        Reads the current Speed loop Ki parameters from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x33)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x33)
        - DATA[1-4]: Speed loop Ki parameters (Q24 format, converted from float)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - speed_loop_KI: Speed loop Ki parameters (float).
        """
        # Send command to read the current Speed loop Ki parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_SPEED_LOOP_KI,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract Speed loop Ki parameters from the response and convert from Q24 to float
        speed_loop_KI_q24 = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        speed_loop_KI = speed_loop_KI_q24 / 16777216.0  # Conversion from Q24 to float

        # Print debug information if enabled
        if debug:
            print(f"Speed loop KI parameters: {speed_loop_KI}")

        return speed_loop_KI

    def read_current_loop_Kp(self, debug=None):
        """
        Reads the current Current loop Kp parameters from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x34)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x34)
        - DATA[1-4]: Current loop Kp parameters (Q24 format, converted from float)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_loop_KP: Current loop Kp parameters (float).
        """
        # Send command to read the current Current loop Kp parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_CURRENT_LOOP_KP,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract Current loop Kp parameters from the response and convert from Q24 to float
        current_loop_KP_q24 = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        current_loop_KP = (
            current_loop_KP_q24 / 16777216.0
        )  # Conversion from Q24 to float

        # Print debug information if enabled
        if debug:
            print(f"Current loop KP parameters: {current_loop_KP}")

        return current_loop_KP

    def read_current_loop_Ki(self, debug=None):
        """
        Reads the current Current loop Ki parameters from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x35)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x35)
        - DATA[1-4]: Current loop Ki parameters (Q24 format, converted from float)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_loop_KI: Current loop Ki parameters (float).
        """
        # Send command to read the current Current loop Ki parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_CURRENT_LOOP_KI,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract Current loop Ki parameters from the response and convert from Q24 to float
        current_loop_KI_q24 = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        current_loop_KI = (
            current_loop_KI_q24 / 16777216.0
        )  # Conversion from Q24 to float

        # Print debug information if enabled
        if debug:
            print(f"Current loop KI parameters: {current_loop_KI}")

        return current_loop_KI

    def write_position_loop_Kp_to_RAM(self, position_loop_kp, debug=None):
        """
        Writes the Kp parameters of the position loop to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x36)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Position loop Kp parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - position_loop_kp: Position loop Kp parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - position_loop_kp_confirmed: Position loop Kp parameters (float) as confirmed by the drive.
        """
        # Convert position_loop_kp from float to Q24 format
        position_loop_kp_q24 = int(position_loop_kp * 16777216)

        # Send command to write the Kp parameters of the position loop to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_POSITION_LOOP_KP_TO_RAM,
                0x00,
                0x00,
                0x00,
                (position_loop_kp_q24 >> 0) & 0xFF,
                (position_loop_kp_q24 >> 8) & 0xFF,
                (position_loop_kp_q24 >> 16) & 0xFF,
                (position_loop_kp_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Position loop Kp parameters from the response
        position_loop_kp_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed position_loop_kp from Q24 format to float
        position_loop_kp_confirmed_float = position_loop_kp_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Position loop Kp set to ", position_loop_kp_confirmed_float)

        return position_loop_kp_confirmed_float

    def write_position_loop_Ki_to_RAM(self, position_loop_ki, debug=None):
        """
        Writes the Ki parameters of the position loop to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x37)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Position loop Ki parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - position_loop_ki: Position loop Ki parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - position_loop_ki_confirmed: Position loop Ki parameters (float) as confirmed by the drive.
        """
        # Convert position_loop_ki from float to Q24 format
        position_loop_ki_q24 = int(position_loop_ki * 16777216)

        # Send command to write the Ki parameters of the position loop to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_POSITION_LOOP_KI_TO_RAM,
                0x00,
                0x00,
                0x00,
                (position_loop_ki_q24 >> 0) & 0xFF,
                (position_loop_ki_q24 >> 8) & 0xFF,
                (position_loop_ki_q24 >> 16) & 0xFF,
                (position_loop_ki_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Position loop Ki parameters from the response
        position_loop_ki_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed position_loop_ki from Q24 format to float
        position_loop_ki_confirmed_float = position_loop_ki_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Position loop Ki set to ", position_loop_ki_confirmed_float)

        return position_loop_ki_confirmed_float

    def write_speed_loop_Kp_to_RAM(self, speed_loop_kp, debug=None):
        """
        Writes the Kp parameters of the speed loop to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x38)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed loop Kp parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - speed_loop_kp: Speed loop Kp parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - speed_loop_kp_confirmed: Speed loop Kp parameters (float) as confirmed by the drive.
        """
        # Convert speed_loop_kp from float to Q24 format
        speed_loop_kp_q24 = int(speed_loop_kp * 16777216)

        # Send command to write the Kp parameters of the speed loop to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SPEED_LOOP_KP_TO_RAM,
                0x00,
                0x00,
                0x00,
                (speed_loop_kp_q24 >> 0) & 0xFF,
                (speed_loop_kp_q24 >> 8) & 0xFF,
                (speed_loop_kp_q24 >> 16) & 0xFF,
                (speed_loop_kp_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Speed loop Kp parameters from the response
        speed_loop_kp_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed speed_loop_kp from Q24 format to float
        speed_loop_kp_confirmed_float = speed_loop_kp_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Speed loop Kp set to ", speed_loop_kp_confirmed_float)

        return speed_loop_kp_confirmed_float

    def write_speed_loop_Ki_to_RAM(self, speed_loop_ki, debug=None):
        """
        Writes the Ki parameters of the speed loop to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x39)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed loop Ki parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - speed_loop_ki: Speed loop Ki parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - speed_loop_ki_confirmed: Speed loop Ki parameters (float) as confirmed by the drive.
        """
        # Convert speed_loop_ki from float to Q24 format
        speed_loop_ki_q24 = int(speed_loop_ki * 16777216)

        # Send command to write the Ki parameters of the speed loop to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SPEED_LOOP_KI_TO_RAM,
                0x00,
                0x00,
                0x00,
                (speed_loop_ki_q24 >> 0) & 0xFF,
                (speed_loop_ki_q24 >> 8) & 0xFF,
                (speed_loop_ki_q24 >> 16) & 0xFF,
                (speed_loop_ki_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Speed loop Ki parameters from the response
        speed_loop_ki_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed speed_loop_ki from Q24 format to float
        speed_loop_ki_confirmed_float = speed_loop_ki_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Speed loop Ki set to ", speed_loop_ki_confirmed_float)

        return speed_loop_ki_confirmed_float

    def write_current_loop_Kp_to_RAM(self, current_loop_kp, debug=None):
        """
        Writes the Kp parameters of the current loop to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x3A)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Current loop Kp parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - current_loop_kp: Current loop Kp parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_loop_kp_confirmed: Current loop Kp parameters (float) as confirmed by the drive.
        """
        # Convert current_loop_kp from float to Q24 format
        current_loop_kp_q24 = int(current_loop_kp * 16777216)

        # Send command to write the Kp parameters of the current loop to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_CURRENT_LOOP_KP_TO_RAM,
                0x00,
                0x00,
                0x00,
                (current_loop_kp_q24 >> 0) & 0xFF,
                (current_loop_kp_q24 >> 8) & 0xFF,
                (current_loop_kp_q24 >> 16) & 0xFF,
                (current_loop_kp_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Current loop Kp parameters from the response
        current_loop_kp_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed current_loop_kp from Q24 format to float
        current_loop_kp_confirmed_float = current_loop_kp_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Current loop Kp set to ", current_loop_kp_confirmed_float)

        return current_loop_kp_confirmed_float

    def write_current_loop_Ki_to_RAM(self, current_loop_ki, debug=None):
        """
        Writes the Ki parameters of the current loop to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x3B)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Current loop Ki parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - current_loop_ki: Current loop Ki parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_loop_ki_confirmed: Current loop Ki parameters (float) as confirmed by the drive.
        """
        # Convert current_loop_ki from float to Q24 format
        current_loop_ki_q24 = int(current_loop_ki * 16777216)

        # Send command to write the Ki parameters of the current loop to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_CURRENT_LOOP_KI_TO_RAM,
                0x00,
                0x00,
                0x00,
                (current_loop_ki_q24 >> 0) & 0xFF,
                (current_loop_ki_q24 >> 8) & 0xFF,
                (current_loop_ki_q24 >> 16) & 0xFF,
                (current_loop_ki_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Current loop Ki parameters from the response
        current_loop_ki_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed current_loop_ki from Q24 format to float
        current_loop_ki_confirmed_float = current_loop_ki_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Current loop Ki set to ", current_loop_ki_confirmed_float)

        return current_loop_ki_confirmed_float

    def write_position_loop_Kp_to_ROM(self, position_loop_kp, debug=None):
        """
        Writes the Kp parameters of the position loop to the ROM.

        Command Structure:
        - DATA[0]: Command byte (0x3C)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Position loop Kp parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - position_loop_kp: Position loop Kp parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - position_loop_kp_confirmed: Position loop Kp parameters (float) as confirmed by the drive.
        """
        # Convert position_loop_kp from float to Q24 format
        position_loop_kp_q24 = int(position_loop_kp * 16777216)

        # Send command to write the Kp parameters of the position loop to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_POSITION_LOOP_KP_TO_ROM,
                0x00,
                0x00,
                0x00,
                (position_loop_kp_q24 >> 0) & 0xFF,
                (position_loop_kp_q24 >> 8) & 0xFF,
                (position_loop_kp_q24 >> 16) & 0xFF,
                (position_loop_kp_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Position loop Kp parameters from the response
        position_loop_kp_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed position_loop_kp from Q24 format to float
        position_loop_kp_confirmed_float = position_loop_kp_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Position loop Kp set to ", position_loop_kp_confirmed_float)

        return position_loop_kp_confirmed_float

    def write_position_loop_Ki_to_ROM(self, position_loop_ki, debug=None):
        """
        Writes the Ki parameters of the position loop to the ROM.

        Command Structure:
        - DATA[0]: Command byte (0x3D)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Position loop Ki parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - position_loop_ki: Position loop Ki parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - position_loop_ki_confirmed: Position loop Ki parameters (float) as confirmed by the drive.
        """
        # Convert position_loop_ki from float to Q24 format
        position_loop_ki_q24 = int(position_loop_ki * 16777216)

        # Send command to write the Ki parameters of the position loop to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_POSITION_LOOP_KI_TO_ROM,
                0x00,
                0x00,
                0x00,
                (position_loop_ki_q24 >> 0) & 0xFF,
                (position_loop_ki_q24 >> 8) & 0xFF,
                (position_loop_ki_q24 >> 16) & 0xFF,
                (position_loop_ki_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Position loop Ki parameters from the response
        position_loop_ki_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed position_loop_ki from Q24 format to float
        position_loop_ki_confirmed_float = position_loop_ki_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Position loop Ki set to ", position_loop_ki_confirmed_float)

        return position_loop_ki_confirmed_float

    def write_speed_loop_Kp_to_ROM(self, speed_loop_kp, debug=None):
        """
        Writes the Kp parameters of the speed loop to the ROM.

        Command Structure:
        - DATA[0]: Command byte (0x3E)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed loop Kp parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - speed_loop_kp: Speed loop Kp parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - speed_loop_kp_confirmed: Speed loop Kp parameters (float) as confirmed by the drive.
        """
        # Convert speed_loop_kp from float to Q24 format
        speed_loop_kp_q24 = int(speed_loop_kp * 16777216)

        # Send command to write the Kp parameters of the speed loop to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SPEED_LOOP_KP_TO_ROM,
                0x00,
                0x00,
                0x00,
                (speed_loop_kp_q24 >> 0) & 0xFF,
                (speed_loop_kp_q24 >> 8) & 0xFF,
                (speed_loop_kp_q24 >> 16) & 0xFF,
                (speed_loop_kp_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Speed loop Kp parameters from the response
        speed_loop_kp_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed speed_loop_kp from Q24 format to float
        speed_loop_kp_confirmed_float = speed_loop_kp_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Speed loop Kp set to ", speed_loop_kp_confirmed_float)

        return speed_loop_kp_confirmed_float

    def write_speed_loop_Ki_to_ROM(self, speed_loop_ki, debug=None):
        """
        Writes the Ki parameters of the speed loop to the ROM.

        Command Structure:
        - DATA[0]: Command byte (0x3F)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed loop Ki parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - speed_loop_ki: Speed loop Ki parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - speed_loop_ki_confirmed: Speed loop Ki parameters (float) as confirmed by the drive.
        """
        # Convert speed_loop_ki from float to Q24 format
        speed_loop_ki_q24 = int(speed_loop_ki * 16777216)

        # Send command to write the Ki parameters of the speed loop to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SPEED_LOOP_KI_TO_ROM,
                0x00,
                0x00,
                0x00,
                (speed_loop_ki_q24 >> 0) & 0xFF,
                (speed_loop_ki_q24 >> 8) & 0xFF,
                (speed_loop_ki_q24 >> 16) & 0xFF,
                (speed_loop_ki_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Speed loop Ki parameters from the response
        speed_loop_ki_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed speed_loop_ki from Q24 format to float
        speed_loop_ki_confirmed_float = speed_loop_ki_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Speed loop Ki set to ", speed_loop_ki_confirmed_float)

        return speed_loop_ki_confirmed_float

    def write_current_loop_Kp_to_ROM(self, current_loop_kp, debug=None):
        """
        Writes the Kp parameters of the current loop to the ROM.

        Command Structure:
        - DATA[0]: Command byte (0x40)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Current loop Kp parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - current_loop_kp: Current loop Kp parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_loop_kp_confirmed: Current loop Kp parameters (float) as confirmed by the drive.
        """
        # Convert current_loop_kp from float to Q24 format
        current_loop_kp_q24 = int(current_loop_kp * 16777216)

        # Send command to write the Kp parameters of the current loop to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_CURRENT_LOOP_KP_TO_ROM,
                0x00,
                0x00,
                0x00,
                (current_loop_kp_q24 >> 0) & 0xFF,
                (current_loop_kp_q24 >> 8) & 0xFF,
                (current_loop_kp_q24 >> 16) & 0xFF,
                (current_loop_kp_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Current loop Kp parameters from the response
        current_loop_kp_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed current_loop_kp from Q24 format to float
        current_loop_kp_confirmed_float = current_loop_kp_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Current loop Kp set to ", current_loop_kp_confirmed_float)

        return current_loop_kp_confirmed_float

    def write_current_loop_Ki_to_ROM(self, current_loop_ki, debug=None):
        """
        Writes the Ki parameters of the current loop to the ROM.

        Command Structure:
        - DATA[0]: Command byte (0x41)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Current loop Ki parameters (Q24 format)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - current_loop_ki: Current loop Ki parameters (float).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_loop_ki_confirmed: Current loop Ki parameters (float) as confirmed by the drive.
        """
        # Convert current_loop_ki from float to Q24 format
        current_loop_ki_q24 = int(current_loop_ki * 16777216)

        # Send command to write the Ki parameters of the current loop to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_CURRENT_LOOP_KI_TO_ROM,
                0x00,
                0x00,
                0x00,
                (current_loop_ki_q24 >> 0) & 0xFF,
                (current_loop_ki_q24 >> 8) & 0xFF,
                (current_loop_ki_q24 >> 16) & 0xFF,
                (current_loop_ki_q24 >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of Current loop Ki parameters from the response
        current_loop_ki_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Convert confirmed current_loop_ki from Q24 format to float
        current_loop_ki_confirmed_float = current_loop_ki_confirmed / 16777216.0

        # Print debug information if enabled
        if debug:
            print("Current loop Ki set to ", current_loop_ki_confirmed_float)

        return current_loop_ki_confirmed_float

    def read_acceleration(self, debug=None):
        """
        Reads motor acceleration data from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x42)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x42)
        - DATA[1-4]: Acceleration data (int32_t, range 0-10000, in dps/s)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - acceleration: Motor acceleration data in dps/s.
        """
        # Send command to read motor acceleration data
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_ACCELERATION,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract acceleration data from the response
        acceleration = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Print debug information if enabled
        if debug:
            print(f"Acceleration: {acceleration} dps/s")

        return acceleration

    def write_acceleration_to_RAM(self, acceleration, debug=None):
        """
        Writes acceleration data to the RAM.

        Command Structure:
        - DATA[0]: Command byte (0x43)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Acceleration data (int32_t, range 0-10000, in dps/s)

        Response Structure:
        - DATA[0-7]: Same as the received command

        Parameters:
        - acceleration: Acceleration data to write (int32_t, range 0-10000, in dps/s).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - acceleration: Acceleration data as confirmed by the drive.
        """
        # Send command to write acceleration data to the RAM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_ACCELERATION_TO_RAM,
                0x00,
                0x00,
                0x00,
                (acceleration >> 0) & 0xFF,
                (acceleration >> 8) & 0xFF,
                (acceleration >> 16) & 0xFF,
                (acceleration >> 24) & 0xFF,
            ],
        )

        # Extract confirmation of acceleration data from the response
        acceleration_confirmed = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Print debug information if enabled
        if debug:
            print("Acceleration set to ", acceleration_confirmed)

        return acceleration_confirmed

    def read_multiturn_encoder_position(self, debug=None):
        """
        Reads the encoder multi-turn position from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x60)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x60)
        - DATA[1-6]: Encoder position (int64_t, multiturn encoder value range)
        - DATA[7]: Encoder position positive or negative flag bit (1 for negative, 0 for positive)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_position: Encoder multi-turn position.
        """
        # Send command to read encoder multi-turn position
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MULTITURN_ENCODER_POSITION,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract encoder position data from the response
        encoder_position = (
            msg.data[1]
            | (msg.data[2] << 8)
            | (msg.data[3] << 16)
            | (msg.data[4] << 24)
            | (msg.data[5] << 32)
            | (msg.data[6] << 40)
        )

        # Check if encoder position is negative
        if msg.data[7] != 0:
            encoder_position = -encoder_position

        # Print debug information if enabled
        if debug is not None:
            print(f"Multiturn encoder position: {encoder_position}")

        return encoder_position

    def read_multiturn_encoder_original_position(self, debug=None):
        """
        Reads the encoder multi-turn original position from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x61)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x61)
        - DATA[1-6]: Encoder original position (int64_t, value range)
        - DATA[7]: Encoder original position positive or negative flag bit (1 for negative, 0 for positive)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_raw: Encoder multi-turn original position.
        """
        # Send command to read encoder multi-turn original position
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MULTITURN_ENCODER_ORIGINAL_POSITION,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract encoder original position data from the response
        encoder_raw = (
            msg.data[1]
            | (msg.data[2] << 8)
            | (msg.data[3] << 16)
            | (msg.data[4] << 24)
            | (msg.data[5] << 32)
            | (msg.data[6] << 40)
        )

        # Check if encoder original position is negative
        if msg.data[7] != 0:
            encoder_raw = -encoder_raw

        # Print debug information if enabled
        if debug is not None:
            print(f"Multiturn encoder original position : {encoder_raw}")

        return encoder_raw

    def read_multiturn_encoder_zero_offset(self, debug=None):
        """
        Reads the encoder multi-turn zero offset value from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x62)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x62)
        - DATA[1-6]: Encoder zero offset (int64_t, value range)
        - DATA[7]: Encoder zero offset positive or negative flag bit (1 for negative, 0 for positive)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_zero_offset: Encoder multi-turn zero offset value.
        """
        # Send command to read encoder multi-turn zero offset value
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MULTITURN_ENCODER_OFFSET,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract encoder zero offset value from the response
        encoder_zero_offset = (
            msg.data[1]
            | (msg.data[2] << 8)
            | (msg.data[3] << 16)
            | (msg.data[4] << 24)
            | (msg.data[5] << 32)
            | (msg.data[6] << 40)
        )

        # Check if encoder zero offset is negative
        if msg.data[7] != 0:
            encoder_zero_offset = -encoder_zero_offset

        # Print debug information if enabled
        if debug is not None:
            print(f"Multiturn encoder zero offset : {encoder_zero_offset}")

        return encoder_zero_offset

    def write_multiturn_encoder_value_position_to_ROM_as_motor_zero(
        self, encoder_offset, debug=None
    ):
        """
        Writes the encoder zero offset value to ROM as motor zero.

        Command Structure:
        - DATA[0]: Command byte (0x63)
        - DATA[1-6]: Encoder offset value (int64_t, value range)
        - DATA[7]: Encoder offset positive or negative flag bit (1 for negative, 0 for positive)

        Parameters:
        - encoder_offset: Encoder zero offset value to write.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_offset: Encoder zero offset value.
        """
        # Determine if the encoder offset is negative
        is_negative = 1 if encoder_offset < 0 else 0

        # Convert encoder offset to absolute value
        encoder_offset = abs(encoder_offset)

        # Send command to write encoder zero offset value to ROM as motor zero
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_MULTITURN_ENCODER_VALUES_TO_ROM_AS_MOTOR_ZERO,
                (encoder_offset >> 0) & 0xFF,
                (encoder_offset >> 8) & 0xFF,
                (encoder_offset >> 16) & 0xFF,
                (encoder_offset >> 24) & 0xFF,
                (encoder_offset >> 32) & 0xFF,
                (encoder_offset >> 40) & 0xFF,
                is_negative,
            ],
        )

        # Extract encoder offset value from the response
        encoder_offset = (
            msg.data[1]
            | (msg.data[2] << 8)
            | (msg.data[3] << 16)
            | (msg.data[4] << 24)
            | (msg.data[5] << 32)
            | (msg.data[6] << 40)
        )

        # Check if encoder offset is negative
        if msg.data[7] != 0:
            encoder_offset = -encoder_offset

        # Print debug information if enabled
        if debug is not None:
            print(f"Multiturn encoder offset set to : {encoder_offset}")

        return encoder_offset

    def write_multiturn_encoder_current_position_to_ROM_as_motor_zero(self, debug=None):
        """
        Write the current encoder position of the motor as the initial position to the ROM.

        Notice:
        1. This command needs to be re-powered to take effect.
        2. This command will write the zero position to the ROM of the drive. Multiple writes will affect the life of the chip. Frequent use is not recommended.

        Command Structure:
        - DATA[0]: Command byte (0x64)
        - DATA[1-7]: NULL bytes

        Drive reply (one frame):
        The motor replies to the host after receiving the command, and the data of encoder offset is the 0 offset value.

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_offset: Encoder offset value.
        """
        # Send command to write current encoder position to ROM as motor zero
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_MULTITURN_ENCODER_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract encoder offset value from the response
        encoder_offset = (
            msg.data[1]
            | (msg.data[2] << 8)
            | (msg.data[3] << 16)
            | (msg.data[4] << 24)
            | (msg.data[5] << 32)
            | (msg.data[6] << 40)
            | (msg.data[7] << 48)
        )

        # Check if encoder offset is negative
        if msg.data[7] != 0:
            encoder_offset = -encoder_offset

        # Print debug information if enabled
        if debug is not None:
            print(f"Multiturn encoder offset set to : {encoder_offset}")

        return encoder_offset

    def read_singleturn_encoder_data(self, debug=None):
        """
        Reads the current position of the single-turn encoder, original position, and encoder offset from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x90)
        - DATA[1-7]: NULL bytes

        Drive reply (one frame):
        The motor responds to the host after receiving the command.
        The frame data contains the following parameters:
        1. Encoder position (int16_t type, value range: 0~65535), which is the value of the original position of the encoder minus the zero offset of the encoder.
        2. Encoder's original position (uint16_t type, value range: 0~65535).
        3. Encoder offset (uint16_t type, value range: 0~65535), this point is regarded as the zero point of the motor angle.

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_position: Current motor position in degrees.
        - original_position: Original motor position in degrees.
        - encoder_offset: Encoder offset in degrees.
        """
        # Send command to read single-turn encoder data
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_SINGLETURN_ENCODER_DATA,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract data from the response
        current_position = (msg.data[2] | (msg.data[3] << 8)) * (360 / 65535)
        original_position = (msg.data[4] | (msg.data[5] << 8)) * (360 / 65535)
        encoder_offset = (msg.data[6] | (msg.data[7] << 8)) * (360 / 65535)

        # Print debug information if enabled
        if debug is not None:
            print(f"Motor position: {current_position} degrees")
            print(f"Motor original position: {original_position} degrees")
            print(f"Motor offset: {encoder_offset} degrees")

        return current_position, original_position, encoder_offset

    def write_encoder_value_to_ROM_as_motor_zero(self, offset, debug=None):
        """
        Sets the encoder zero offset to the specified value and writes it to ROM.

        Command Structure:
        - DATA[0]: Command byte (0x91)
        - DATA[1-5]: NULL bytes
        - DATA[6]: Encoder zero offset low byte
        - DATA[7]: Encoder zero offset high byte

        Drive reply (one frame):
        The motor responds to the host after receiving the command, and the frame data is the same as the host sent.

        Parameters:
        - offset: Encoder offset value to be written (uint16_t type, value range: 0~65535).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - new_encoder_offset: Updated encoder offset value after writing to ROM.
        """
        # Send command to set the encoder zero offset
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_ENCODER_VALUES_TO_ROM_AS_MOTOR_ZERO,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                offset & 0xFF,
                (offset >> 8) & 0xFF,
            ],
        )

        # Extract the new encoder offset from the response
        new_encoder_offset = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if enabled
        if debug is not None:
            print(f"Encoder offset set to {new_encoder_offset}")

        return new_encoder_offset

    def write_singleturn_encoder_current_position_to_ROM_as_motor_zero(
        self, debug=None
    ):
        """
        Writes the current encoder position of the motor as the initial position to the ROM.

        Notice:
        1. This command needs to be re-powered to take effect.
        2. This command will write the zero point to the ROM of the drive. Multiple writes will reduce the life of the chip. Frequent use is not recommended.

        Command Structure:
        - DATA[0]: Command byte (0x19)
        - DATA[1-7]: NULL bytes

        Drive reply (one frame):
        The motor responds to the host after receiving the command, and the encoderOffset in the data is the zero offset value.

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_offset: Encoder zero offset value written to ROM.
        """
        # Send command to write the current encoder position as the initial position to the ROM
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SINGLETURN_ENCODER_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract the encoder zero offset from the response
        encoder_offset = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if enabled
        if debug is not None:
            print(f"Initial position set to {encoder_offset}")

        return encoder_offset

    def read_multiturn_encoder_angle(self, debug=None):
        """
        Reads the multi-turn angle of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x92)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x92)
        - DATA[1-6]: Motor Angle (int64_t type, valid data is 6 bytes), the seventh byte represents positive and negative, where 0 is positive and 1 is negative, unit 0.01°/LSB

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_angle: Motor angle in degrees.
        """
        # Send command to read the multi-turn angle of the motor
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MULTITURN_ANGLE,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract motor angle data from the response
        motor_angle = (
            msg.data[1]
            | (msg.data[2] << 8)
            | (msg.data[3] << 16)
            | (msg.data[4] << 24)
            | (msg.data[5] << 32)
            | (msg.data[6] << 40)
        ) * 0.01

        # Check if the motor angle is negative and adjust if necessary
        if msg.data[7] != 0:
            motor_angle = -motor_angle

        # Print debug information if enabled
        if debug is not None:
            print(f"Encoder multiturn angle: {motor_angle:.2f}°", end="\r")

        return motor_angle

    def read_singleturn_encoder_angle(self, debug=None):
        """
        Reads the single circle angle of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x94)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x94)
        - DATA[6]: Single angle low byte (uint8_t type)
        - DATA[7]: Single angle high byte (uint8_t type)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - circle_angle: Single circle angle of the motor in degrees.
        """
        # Send command to read the single circle angle of the motor
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_SINGLE_CIRCLE_ANGLE,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract single circle angle data from the response
        circle_angle = (msg.data[6] | (msg.data[7] << 8)) * 0.01

        # Print debug information if enabled
        if debug is not None:
            print(f"Encoder singleturn position: {circle_angle:.2f}°", end="\r")

        return circle_angle

    def read_motor_status_1_error_flag(self, debug=None):
        """
        Reads the current motor temperature, voltage, and error status flag.

        Command Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1]: Motor temperature (int8_t type, unit 1°C/LSB)
        - DATA[2]: NULL
        - DATA[3]: NULL
        - DATA[4]: Voltage low byte (uint8_t type)
        - DATA[5]: Voltage high byte (uint8_t type)
        - DATA[6]: Error State low byte (uint8_t type)
        - DATA[7]: Error State high byte (uint8_t type)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - voltage: Voltage in volts.
        - error_state: Error state flag indicating various motor states.
        """
        # Send command to read motor status and error flag
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MOTOR_STATUS_1_ERROR_FLAG,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract motor temperature, voltage, and error state from the response
        motor_temp = msg.data[1]
        voltage = (msg.data[3] | (msg.data[4] << 8)) * 0.1
        error_state = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if enabled
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Voltage: {voltage}V")
            print("Error States:")
            if error_state & 0x0001:
                print("  - Hardware over-current")
            if error_state & 0x0002:
                print("  - Motor stalled")
            if error_state & 0x0004:
                print("  - Low voltage")
            if error_state & 0x0008:
                print("  - Over-voltage")
            if error_state & 0x0010:
                print("  - Over-current")
            if error_state & 0x0020:
                print("  - Brake opening failed")
            if error_state & 0x0040:
                print("  - Bus current error")
            if error_state & 0x0080:
                print("  - Battery voltage error")
            if error_state & 0x0100:
                print("  - Overspeed")
            if error_state & 0x0200:
                print("  - Position loop exceeded error")
            if error_state & 0x0400:
                print("  - VDD error")
            if error_state & 0x0800:
                print("  - DSP internal sensor temperature is overheated")
            if error_state & 0x1000:
                print("  - Motor temperature is overheated")
            if error_state & 0x2000:
                print("  - Encoder calibration error")
            if error_state & 0x00F0:
                print("  - PID parameter write ROM protection, non-safe operation")
            if error_state & 0x00F1:
                print(
                    "  - Encoder value is written into ROM protection, non-safe operation"
                )
            if error_state & 0x00F2:
                print("  - Three-loop switching operation error, non-safe operation")
            if error_state & 0x00F3:
                print("  - Motor brake is not open")
            if error_state & 0x00F4:
                print("  - Motor write ROM protection, non-safe operation")

        return motor_temp, voltage, error_state

    def read_motor_status_2(self, debug=None):
        """
        Reads the current temperature, voltage, speed, and encoder position of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x9C)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9C)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte (int8_t type)
        - DATA[3]: Torque current high byte (int8_t type)
        - DATA[4]: Speed low byte (int8_t type)
        - DATA[5]: Speed high byte (int8_t type)
        - DATA[6]: Encoder position low byte (int8_t type)
        - DATA[7]: Encoder position high byte (int8_t type)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes.
        - motor_speed: Motor speed in degrees per second.
        - encoder_position: Encoder position value.
        """
        # Send command to read motor status and parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MOTOR_STATUS_2,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract motor parameters from the response
        motor_temp = msg.data[1]
        torque_current = msg.data[2] | (msg.data[3] << 8)
        motor_speed = msg.data[4] | (msg.data[5] << 8)
        encoder_position = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if enabled
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Encoder position: {encoder_position}")

        return motor_temp, torque_current, motor_speed, encoder_position

    def read_motor_status_3(self, debug=None):
        """
        Reads the current temperature and phase current data of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x9D)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9D)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Phase A current low byte (int8_t type)
        - DATA[3]: Phase A current high byte (int8_t type)
        - DATA[4]: Phase B current low byte (int8_t type)
        - DATA[5]: Phase B current high byte (int8_t type)
        - DATA[6]: Phase C current low byte (int8_t type)
        - DATA[7]: Phase C current high byte (int8_t type)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - phase_A_current: Phase A current in amperes.
        - phase_B_current: Phase B current in amperes.
        - phase_C_current: Phase C current in amperes.
        """
        # Send command to read motor status and parameters
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MOTOR_STATUS_3,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract motor parameters from the response
        motor_temp = msg.data[1]

        # Calculate phase A current
        phase_A_current = (msg.data[2] | (msg.data[3] << 8)) * (1 / 64)

        # Calculate phase B current
        phase_B_current = (msg.data[4] | (msg.data[5] << 8)) * (1 / 64)

        # Calculate phase C current
        phase_C_current = (msg.data[6] | (msg.data[7] << 8)) * (1 / 64)

        # Print debug information if enabled
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Phase A current: {phase_A_current}A")
            print(f"Phase B current: {phase_B_current}A")
            print(f"Phase C current: {phase_C_current}A")

        return motor_temp, phase_A_current, phase_B_current, phase_C_current

    def motor_off(self, debug=None):
        """
        Turn off the motor, and clear the running state of the motor and the previously received control commands at the same time.

        Command Structure:
        - DATA[0]: Command byte (0x80)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - The motor responds to the host after receiving the command, the frame data is the same as that sent by the host.

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - success: 1 if the motor was successfully turned off, 0 otherwise.
        """
        # Send command to turn off the motor
        msg = self.can_bus.sendMessage(
            self.BASE_ADDR_ID + self.id,
            [self.ADDR_MOTOR_OFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Check if the response matches the sent command
        success = (
            1
            if msg.can_id == self.BASE_ADDR_ID + self.id
            and all(data == 0x00 for data in msg.data[1:])
            else 0
        )

        return success

    def stop(self, debug=None):
        """
        Stop the motor, but do not clear the running state of the motor and the previously received control commands.

        Command Structure:
        - DATA[0]: Command byte (0x81)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - The motor responds to the host after receiving the command, the frame data is the same as that sent by the host.

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - success: 1 if the motor was successfully stopped, 0 otherwise.
        """
        # Send command to stop the motor
        msg = self.can_bus.sendMessage(
            self.BASE_ADDR_ID + self.id,
            [self.ADDR_STOP, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Check if the response matches the sent command
        success = (
            1
            if msg.can_id == self.BASE_ADDR_ID + self.id
            and all(data == 0x00 for data in msg.data[1:])
            else 0
        )

        return success

    def running(self, debug=None):
        """
        Resume motor operation from the motor stop command (recover the control mode before the stop).

        Command Structure:
        - DATA[0]: Command byte (0x88)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - The motor responds to the host after receiving the command, the frame data is the same as that sent by the host.

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - success: 1 if the motor resumed operation successfully, 0 otherwise.
        """
        # Send command to resume motor operation
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[self.ADDR_RUNNING, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Check if the response matches the sent command
        success = (
            1
            if msg.can_id == self.BASE_ADDR_ID + self.id
            and all(data == 0x00 for data in msg.data[1:])
            else 0
        )

        return success

    def torque_closed_loop_control(self, torque, debug=None):
        """
        Control the torque current output of the motor.

        Command Structure:
        - DATA[0]: Command byte (0xA1)
        - DATA[1-3]: NULL bytes
        - DATA[4-5]: Torque current control value (int16_t type, Range: -2048~2048, corresponding to the actual torque current range: -33A~33A)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA1)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, Range: -2048~2048, corresponding to the actual torque current range: -33A~33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 16-bit encoder value range: 0~65535)

        Parameters:
        - torque: Desired torque value in amperes (-33 to 33 A).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes.
        - motor_speed: Motor speed in degrees per second.
        - encoder_position: Encoder position value.
        """
        # Ensure that the torque value is within the acceptable range
        if torque > 33:
            torque = 33
        elif torque < -33:
            torque = -33

        # Convert the torque value to the required range
        torque_current_raw = int(torque * (2048 / 33))

        # Send command to control torque current output
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_TORQUE_CLOSED_LOOP_CONTROL,
                0x00,
                0x00,
                0x00,
                (torque_current_raw >> 0) & 0xFF,
                (torque_current_raw >> 8) & 0xFF,
                0x00,
                0x00,
            ],
        )

        # Extract motor parameters from the response
        motor_temp = msg.data[1]
        torque_current_raw = msg.data[2] | (msg.data[3] << 8)
        torque_current = torque_current_raw * (33 / 2048)  # Convert to amperes
        motor_speed = msg.data[4] | (msg.data[5] << 8)
        encoder_position = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if enabled
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current value (-33~33A): {torque_current:.2f}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor position value (0~16383): {encoder_position}")

        return motor_temp, torque_current, motor_speed, encoder_position

    def speed_closed_loop_control(self, speed, debug=None):
        """
        Control the speed of the motor.

        Command Structure:
        - DATA[0]: Command byte (0xA2)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed control value (int32_t type, corresponding to the actual speed of 0.01 dps/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA2)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, Range: -2048~2048, corresponding to the actual torque current range: -33A~33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 16-bit encoder value range: 0~65535)

        Parameters:
        - speed: Desired speed value in degrees per second (-327.68 to 327.67 dps).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes.
        - motor_speed: Motor speed in degrees per second.
        - encoder_position: Encoder position value.
        """
        # Ensure that the speed value is within the acceptable range
        if speed > 327.67:
            speed = 327.67
        elif speed < -327.68:
            speed = -327.68

        # Convert the speed value to the required range
        speed_control_raw = int(speed * 100)

        # Send command to control motor speed
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_SPEED_CLOSED_LOOP_CONTROL,
                0x00,
                0x00,
                0x00,
                (speed_control_raw >> 0) & 0xFF,
                (speed_control_raw >> 8) & 0xFF,
                (speed_control_raw >> 16) & 0xFF,
                (speed_control_raw >> 24) & 0xFF,
            ],
        )

        # Extract motor parameters from the response
        motor_temp = msg.data[1]
        torque_current_raw = msg.data[2] | (msg.data[3] << 8)
        torque_current = torque_current_raw * (33 / 2048)  # Convert to amperes
        motor_speed = msg.data[4] | (msg.data[5] << 8)
        encoder_position = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if enabled
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current value (-33~33A): {torque_current:.2f}A")
            print(f"Motor speed: {motor_speed:.2f}dps")
            print(f"Motor position value (0~65535): {encoder_position}")

        return motor_temp, torque_current, motor_speed, encoder_position

    def position_closed_loop_control_1(
        self, target_position, wait_for_completion=True, debug=None
    ):
        """
        Control the position of the motor (multi-turn angle).

        Command Structure:
        - DATA[0]: Command byte (0xA3)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Position control value

        Response Structure:
        - DATA[0]: Command byte (0xA3)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte
        - DATA[3]: Torque current high byte
        - DATA[4]: Motor speed low byte
        - DATA[5]: Motor speed high byte
        - DATA[6]: Encoder position low byte
        - DATA[7]: Encoder position high byte

        Parameters:
        - target_position: Multiturn target position in degrees (0 to 42949672.95°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes (-33A to +33A).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Memo:
        1. The control value angleControl under this command is limited by the Max Angle value in the host computer of debugging software.
        2. The maximum speed of the motor under this command is limited by the Max Speed value in the upper computer of debugging software.
        3. In this control mode, the maximum acceleration of the motor is limited by the Max Acceleration value in the host computer of debugging software.
        4. In this control mode, the maximum torque current of the motor is limited by the Max Torque Current value in the host computer of debugging software.
        """

        # Convert angleControl to multiples of 0.01 degree (0.01 degree/LSB)
        target_position = int(target_position * 100)

        # Ensure target_position is within the valid range [0, 0xFFFFFFFF] (int32_t)
        if target_position < 0 or target_position > 0xFFFFFFFF:
            # Raise a ValueError if target_position is out of range
            raise ValueError(
                "Invalid target position value. Target position must be in the range [0, 42949672.95]°"
            )

        # Send command to control motor target_position
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_POSITION_MULTITURN_CLOSED_LOOP_CONTROL,
                0x00,
                0x00,
                0x00,
                (target_position >> 0) & 0xFF,
                (target_position >> 8) & 0xFF,
                (target_position >> 16) & 0xFF,
                (target_position >> 24) & 0xFF,
            ],
        )

        # Wait for motor to reach target position if specified
        if wait_for_completion:
            while True:
                # Read current motor angle from multiturn encoder
                motor_angle = self.read_multiturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Clear previous debug messages
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the line

                # Print debug information
                if debug:
                    print(f"Motor temperature: {motor_temp}°C")
                    print(f"Torque current: {torque_current}A")
                    print(f"Motor speed: {motor_speed}dps")
                    print(f"Motor angle: {motor_angle}°")

                # Exit loop when motor reaches target position and speed is zero
                if abs(motor_angle - target_position) < 0.1 and motor_speed == 0.0:
                    break
        elif debug:
            # Print debug information if specified
            print("Debug information:")
            print(f"Initial position: {self.read_multiturn_encoder_angle()}°")
            print(f"Target position: {target_position}°")

        return motor_temp, torque_current, motor_speed, motor_angle

    def position_closed_loop_control_2(
        self, speed, target_position, wait_for_completion=True, debug=None
    ):
        """
        Control the position of the motor (multi-turn angle) with speed limit.

        Command Structure:
        - DATA[0]: Command byte (0xA4)
        - DATA[1]: NULL byte
        - DATA[2-3]: Speed limit (uint16_t type, 1dps/LSB)
        - DATA[4-7]: Position control value (int32_t type, 0.01 degree/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA4)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte
        - DATA[3]: Torque current high byte
        - DATA[4]: Motor speed low byte
        - DATA[5]: Motor speed high byte
        - DATA[6]: Encoder position low byte
        - DATA[7]: Encoder position high byte

        Parameters:
        - speed: Maximum speed limit for motor rotation in degrees per second (0 to 65535dps).
        - target_position: Target position in degrees (0 to 42949672.95°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes (-33A to +33A).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Memo:
        1. The control value angleControl under this command is limited by the Max Angle value in the host computer.
        2. In this control mode, the maximum acceleration of the motor is limited by the Max Acceleration value in the host computer.
        3. In this control mode, the maximum torque current of the motor is limited by the Max TorqueCurrent value in the host computer.
        """
        # Convert angleControl to multiples of 0.01 degree (0.01 degree/LSB)
        target_position = int(target_position * 100)

        # Ensure target_position is within the valid range [0, 0xFFFFFFFF] (int32_t)
        if target_position < 0 or target_position > 0xFFFFFFFF:
            # Raise a ValueError if target_position is out of range
            raise ValueError(
                "Invalid target position value. Target position must be in the range [0, 42949672.95]°"
            )

        # Ensure speed is within the valid range [0, 65535]
        if speed < 0 or speed > 0xFFFF:
            # Raise a ValueError if speed is out of range
            raise ValueError(
                "Invalid speed value. Speed must be in the range [0, 65535]"
            )

        # Convert target_position to multiples of 0.01 degree (0.01 degree/LSB)
        angle_control = int(target_position * 100)

        # Send command to control motor target_position with speed limit
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_POSITION_MULTITURN_SPEED_CLOSED_LOOP_CONTROL,
                0x00,
                (speed >> 0) & 0xFF,
                (speed >> 8) & 0xFF,
                (angle_control >> 0) & 0xFF,
                (angle_control >> 8) & 0xFF,
                (angle_control >> 16) & 0xFF,
                (angle_control >> 24) & 0xFF,
            ],
        )

        # Wait for motor to reach target position if specified
        if wait_for_completion:
            while True:
                # Read current motor angle from multiturn encoder
                motor_angle = self.read_multiturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Clear previous debug messages
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the line

                # Print debug information
                if debug:
                    print(f"Motor temperature: {motor_temp}°C")
                    print(f"Torque current: {torque_current}A")
                    print(f"Motor speed: {motor_speed}dps")
                    print(f"Motor angle: {motor_angle}°")

                # Exit loop when motor reaches target position and speed is zero
                if abs(motor_angle - target_position) < 0.1 and motor_speed == 0.0:
                    break
        elif debug:
            # Print debug information if specified
            print("Debug information:")
            print(f"Initial position: {self.read_multiturn_encoder_angle()}°")
            print(f"Target position: {target_position}°")

        return motor_temp, torque_current, motor_speed, motor_angle

    def position_closed_loop_control_3(
        self, direction, position, wait_for_completion=True, debug=None
    ):
        """
        Control the position of the motor (single-turn angle) with specified rotation direction.

        Command Structure:
        - DATA[0]: Command byte (0xA5)
        - DATA[1]: Rotation direction byte (spinDirection)
        - DATA[2-3]: NULL bytes
        - DATA[4-5]: Position control value (uint16_t type, 0.01 degree/LSB)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA5)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte
        - DATA[3]: Torque current high byte
        - DATA[4]: Motor speed low byte
        - DATA[5]: Motor speed high byte
        - DATA[6]: Encoder position low byte
        - DATA[7]: Encoder position high byte

        Parameters:
        - direction: Rotation direction of the motor (0x00 for clockwise, 0x01 for counterclockwise).
        - position: Target position in degrees (0 to 360°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes (-33A to +33A).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Memo:
        1. The maximum speed of the motor under this command is limited by the Max Speed value in the host computer.
        2. In this control mode, the maximum acceleration of the motor is limited by the Max Acceleration value in the host computer.
        3. In this control mode, the maximum torque current of the motor is limited by the Max TorqueCurrent value in the host computer.
        """

        # Ensure position is within the valid range [0, 360]
        if position < 0 or position > 360:
            # Raise a ValueError if position is out of range
            raise ValueError(
                "Invalid position value. Position must be in the range [0, 360]"
            )

        # Ensure direction is either 0x00 or 0x01
        if direction not in [0x00, 0x01]:
            # Raise a ValueError if direction is incorrect
            raise ValueError(
                "Invalid direction value. Direction must be 0x00 (clockwise) or 0x01 (counterclockwise)"
            )

        # Convert position to multiples of 0.01 degree (0.01 degree/LSB)
        angle_control = int(position * 100)

        # Send command to control motor position with specified direction
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_POSITION_SINGLETURN_DIRECTION_CLOSED_LOOP_CONTROL,
                direction & 0xFF,
                0x00,
                0x00,
                (angle_control >> 0) & 0xFF,
                (angle_control >> 8) & 0xFF,
                0x00,
                0x00,
            ],
        )

        # Wait for motor to reach target position if specified
        if wait_for_completion:
            while True:
                # Read current motor angle from single-turn encoder
                motor_angle = self.read_singleturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Clear previous debug messages
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the line

                # Print debug information
                if debug:
                    print(f"Motor temperature: {motor_temp}°C")
                    print(f"Torque current: {torque_current}A")
                    print(f"Motor speed: {motor_speed}dps")
                    print(f"Motor angle: {motor_angle}°")

                # Exit loop when motor reaches target position and speed is zero
                if abs(motor_angle - position) < 0.1 and motor_speed == 0.0:
                    break
        elif debug:
            # Print debug information if specified
            print("Debug information:")
            print(f"Initial position: {self.read_singleturn_encoder_angle()}°")
            print(f"Target position: {position}°")

        return motor_temp, torque_current, motor_speed, motor_angle

    def position_closed_loop_control_4(
        self, speed, direction, position, wait_for_completion=True, debug=None
    ):
        """
        Control the position of the motor (single-turn angle) with specified rotation direction and speed limit.

        Command Structure:
        - DATA[0]: Command byte (0xA6)
        - DATA[1]: Rotation direction byte (spinDirection)
        - DATA[2-3]: Speed limit (uint16_t type, 1dps/LSB)
        - DATA[4-5]: Position control value (uint16_t type, 0.01 degree/LSB)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA6)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte
        - DATA[3]: Torque current high byte
        - DATA[4]: Motor speed low byte
        - DATA[5]: Motor speed high byte
        - DATA[6]: Encoder position low byte
        - DATA[7]: Encoder position high byte

        Parameters:
        - speed: Maximum speed limit for motor rotation in degrees per second (dps).
        - direction: Rotation direction of the motor (0x00 for clockwise, 0x01 for counterclockwise).
        - position: Target position in degrees (0 to 360°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes (-33A to +33A).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Memo:
        1. In this control mode, the maximum acceleration of the motor is limited by the Max Acceleration value in the host computer.
        2. In this control mode, the maximum torque current of the motor is limited by the Max TorqueCurrent value in the host computer.
        """

        # Ensure position is within the valid range [0, 360]
        if position < 0 or position > 360:
            # Raise a ValueError if position is out of range
            raise ValueError(
                "Invalid position value. Position must be in the range [0, 360]"
            )

        # Ensure speed is within the valid range [0, 65535]
        if speed < 0 or speed > 0xFFFF:
            # Raise a ValueError if speed is out of range
            raise ValueError(
                "Invalid speed value. Speed must be in the range [0, 65535]"
            )

        # Ensure direction is either 0x00 or 0x01
        if direction not in [0x00, 0x01]:
            # Raise a ValueError if direction is incorrect
            raise ValueError(
                "Invalid direction value. Direction must be 0x00 (clockwise) or 0x01 (counterclockwise)"
            )

        # Convert position to multiples of 0.01 degree (0.01 degree/LSB)
        angle_control = int(position * 100)

        # Send command to control motor position with specified direction and speed limit
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_POSITION_SINGLETURN_SPEED_DIRECTION_CLOSED_LOOP_CONTROL,
                direction & 0xFF,
                (speed >> 0) & 0xFF,
                (speed >> 8) & 0xFF,
                (angle_control >> 0) & 0xFF,
                (angle_control >> 8) & 0xFF,
                0x00,
                0x00,
            ],
        )

        # Wait for motor to reach target position if specified
        if wait_for_completion:
            while True:
                # Read current motor angle from single-turn encoder
                motor_angle = self.read_singleturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Clear previous debug messages
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the line

                # Print debug information
                if debug:
                    print(f"Motor temperature: {motor_temp}°C")
                    print(f"Torque current: {torque_current}A")
                    print(f"Motor speed: {motor_speed}dps")
                    print(f"Motor angle: {motor_angle}°")

                # Exit loop when motor reaches target position and speed is zero
                if abs(motor_angle - position) < 0.1 and motor_speed == 0.0:
                    break
        elif debug:
            # Print debug information if specified
            print("Debug information:")
            print(f"Initial position: {self.read_singleturn_encoder_angle()}°")
            print(f"Target position: {position}°")

        return motor_temp, torque_current, motor_speed, motor_angle

    def position_closed_loop_control_5(
        self, target_position, wait_for_completion=True, debug=None
    ):
        """
        Control the incremental position of the motor (multi-turn angle) with specified angle control value.

        Command Structure:
        - DATA[0]: Command byte (0xA7)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Angle control value (int32_t type, 0.01 degree/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA7)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte
        - DATA[3]: Torque current high byte
        - DATA[4]: Motor speed low byte
        - DATA[5]: Motor speed high byte
        - DATA[6]: Encoder position low byte
        - DATA[7]: Encoder position high byte

        Parameters:
        - target_position: Incremental position control value in degrees (0 to 42949672.95°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes (-33A to +33A).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.
        """

        # Convert target_position to multiples of 0.01 degree (0.01 degree/LSB)
        target_position = int(target_position * 100)

        # Ensure target_position is within the valid range [0, 0xFFFFFFFF] (int32_t)
        if target_position < 0 or target_position > 0xFFFFFFFF:
            # Raise a ValueError if position is out of range
            raise ValueError(
                "Invalid position value. Position must be in the range [0, 42949672.95]°"
            )

        # Get initial motor target_position
        initial_position = self.read_multiturn_encoder_angle()

        # Send command to control motor position with specified angle control value
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_POSITION_MULTITURN_INCREMENTAL_CLOSED_LOOP_CONTROL,
                0x00,
                0x00,
                0x00,
                (target_position >> 0) & 0xFF,
                (target_position >> 8) & 0xFF,
                (target_position >> 16) & 0xFF,
                (target_position >> 24) & 0xFF,
            ],
        )

        # Wait for motor to reach target position if specified
        if wait_for_completion:
            while True:
                # Read current motor angle from multiturn encoder
                motor_angle = self.read_multiturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Clear previous debug messages
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the line

                # Print debug information
                if debug:
                    print(f"Motor temperature: {motor_temp}°C")
                    print(f"Torque current: {torque_current}A")
                    print(f"Motor speed: {motor_speed}dps")
                    print(f"Motor angle: {motor_angle}°")

                # Exit loop when motor reaches target position and speed is zero
                if (
                    abs(initial_position + target_position - motor_angle) < 0.1
                    and motor_speed == 0.0
                ):
                    break

        return motor_temp, torque_current, motor_speed, motor_angle

    def position_closed_loop_control_6(
        self, maxSpeed, target_position, wait_for_completion=True, debug=None
    ):
        """
        Control the incremental position (multi-turn angle) of the motor with specified angle control value and maximum speed limit.

        Command Structure:
        - DATA[0]: Command byte (0xA8)
        - DATA[1]: NULL byte (0x00)
        - DATA[2-3]: Maximum speed limit (uint16_t type, 1dps/LSB)
        - DATA[4-7]: Angle control value (int32_t type, 0.01 degree/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA8)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2]: Torque current low byte
        - DATA[3]: Torque current high byte
        - DATA[4]: Motor speed low byte
        - DATA[5]: Motor speed high byte
        - DATA[6]: Encoder position low byte
        - DATA[7]: Encoder position high byte

        Parameters:
        - maxSpeed: Maximum speed limit for motor rotation in degrees per second (0 to 65535dps).
        - target_position: Incremental position control value in degrees (0 to 42949672.95°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes (-33A to +33A).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.
        """
        # Convert angleControl to multiples of 0.01 degree (0.01 degree/LSB)
        target_position = int(target_position * 100)

        # Ensure target_position is within the valid range [0, 0xFFFFFFFF] (int32_t)
        if target_position < 0 or target_position > 0xFFFFFFFF:
            # Raise a ValueError if target_position is out of range
            raise ValueError(
                "Invalid target position value. Target position must be in the range [0, 42949672.95]°"
            )

        # Ensure maxSpeed is within the valid range [0, 0xFFFF] (uint16_t)
        if maxSpeed < 0 or maxSpeed > 0xFFFF:
            # Raise a ValueError if maxSpeed is out of range
            raise ValueError(
                "Invalid maxSpeed value. MaxSpeed must be in the range [0, 65535]dps"
            )

        # Send command to control motor target_position with specified angle control value and maximum speed limit
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_POSITION_MULTITURN_INCREMENTAL_SPEED_CLOSED_LOOP_CONTROL,
                0x00,
                (maxSpeed >> 0) & 0xFF,
                (maxSpeed >> 8) & 0xFF,
                (target_position >> 0) & 0xFF,
                (target_position >> 8) & 0xFF,
                (target_position >> 16) & 0xFF,
                (target_position >> 24) & 0xFF,
            ],
        )

        # Wait for motor to reach target position if specified
        if wait_for_completion:
            # Get initial motor position
            initial_position = self.read_multiturn_encoder_angle()

            while True:
                # Read current motor angle from multiturn encoder
                motor_angle = self.read_multiturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Clear previous debug messages
                sys.stdout.write("\033[F")  # Move cursor up one line
                sys.stdout.write("\033[K")  # Clear the line

                # Print debug information
                if debug:
                    print(f"Motor temperature: {motor_temp}°C")
                    print(f"Torque current: {torque_current}A")
                    print(f"Motor speed: {motor_speed}dps")
                    print(f"Motor angle: {motor_angle}°")

                # Exit loop when motor reaches target position and speed is zero
                if (
                    abs(initial_position + target_position - motor_angle) < 0.1
                    and motor_speed == 0.0
                ):
                    break

        return motor_temp, torque_current, motor_speed, motor_angle

    def read_running_mode(self, debug=None):
        """
        This command reads the current motor running mode.

        Command Structure:
        - DATA[0]: Command byte (0x70)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x70)
        - DATA[1-6]: NULL bytes
        - DATA[7]: Motor running mode (uint8_t type)
            - 0x00: Current loop mode
            - 0x01: Speed loop mode
            - 0x02: Position loop mode
            - 0xFF: Power-on initialization state, not in three-ring mode

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - run_mode: Current motor running mode.
        """

        # Send command to read current motor running mode
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_RUNNING_MODE,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract motor running mode from the response
        run_mode = msg.data[7]

        # Print debug information if specified
        if debug:
            print(f"Motor running mode: {run_mode}")

        return run_mode

    def read_current_power_value(self, debug=None):
        """
        This command reads the current motor power.

        Command Structure:
        - DATA[0]: Command byte (0x71)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x71)
        - DATA[1-6]: NULL bytes
        - DATA[7-8]: Motor running power (uint16_t type)
            - Unit: watts
            - Resolution: 0.1 watts/LSB

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_power: Current motor power in watts (uint16_t type).
        """

        # Send command to read current motor power
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[self.ADDR_READ_POWER_VALUE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Extract motor power from the response
        motor_power = (msg.data[6] << 0) | (msg.data[7] << 8) * 0.1

        # Print debug information if specified
        if debug:
            print(f"Motor running power: {motor_power} watts")

        return motor_power

    def read_battery_voltage_value(self, debug=None):
        """
        This command reads the current auxiliary battery voltage.

        Command Structure:
        - DATA[0]: Command byte (0x72)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x72)
        - DATA[1-6]: NULL bytes
        - DATA[7]: High battery voltage (uint8_t type)
            - Unit: volts
            - Resolution: 0.1 volts/LSB

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - battery_voltage: Current auxiliary battery voltage in volts (uint8_t type).
        """

        # Send command to read current auxiliary battery voltage
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_BATTERY_VOLTAGE,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract battery voltage from the response
        battery_voltage = msg.data[7] * 0.1

        # Print debug information if specified
        if debug:
            print(f"Auxiliary battery voltage: {battery_voltage} volts")

        return battery_voltage

    def set_feedforward_setting(self, TF_current, encoder_position, debug=None):
        """
        This command sets the current feedforward current size and the encoder position.

        Command Structure:
        - DATA[0]: Command byte (0x73)
        - DATA[1]: NULL byte (0x00)
        - DATA[2-3]: TF feedforward current value (int16_t type, unit A, zoomed in 100 times in current mode)
        - DATA[4-7]: Encoder position (int32_t type)

        Response Structure:
        - DATA[0]: Torque current low byte
        - DATA[1]: Torque current high byte
        - DATA[2]: Motor speed low byte
        - DATA[3]: Motor speed high byte
        - DATA[4-7]: Encoder position (int32_t type)

        Parameters:
        - TF_current: TF feedforward current value of the motor (-327.68 to 327.67A).
        - encoder_position: Encoder position multi-turn encoder (int32_t type).
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - torque_current: Motor torque current (int16_t type, zoomed in 100 times in current mode, such as 10 corresponds to 0.1A).
        - motor_speed: Motor speed in degrees per second (int16_t type, 1dps/LSB).
        - encoder_position: Encoder position multi-turn encoder (int32_t type).
        """
        TF_current = int(TF_current * 100)  # Convert TF_current to int16_t type
        # Ensure TF_current is within the valid range [-32768, 32767]
        if TF_current < -32768 or TF_current > 32767:
            raise ValueError(
                "Invalid TF feedforward current value. TF feedforward current must be in the range [-32768, 32767]"
            )

        # Ensure encoder_position is within the valid range [-2147483648, 2147483647]
        if encoder_position < -2147483648 or encoder_position > 2147483647:
            raise ValueError(
                "Invalid encoder position value. Encoder position must be in the range [-2147483648, 2147483647]"
            )

        # Send command to set feedforward setting
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_FEEDFORWARD_SETTING,
                0x00,
                (TF_current >> 0) & 0xFF,
                (TF_current >> 8) & 0xFF,
                (encoder_position >> 0) & 0xFF,
                (encoder_position >> 8) & 0xFF,
                (encoder_position >> 16) & 0xFF,
                (encoder_position >> 24) & 0xFF,
            ],
        )

        # Read response
        torque_current = (
            (msg.data[0] << 0) | (msg.data[1] << 8)
        ) / 100  # Correcting the scaling
        motor_speed = (msg.data[2] << 0) | (msg.data[3] << 8)
        encoder_position = (
            (msg.data[4] << 0)
            | (msg.data[5] << 8)
            | (msg.data[6] << 16)
            | (msg.data[7] << 24)
        )

        # Print debug information if specified
        if debug:
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Encoder position: {encoder_position}")

        return torque_current, motor_speed, encoder_position

    def system_reset(self, debug=None):
        """
        This command is used to reset the system software.

        Command Structure:
        - DATA[0]: Command byte (0x76)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - Same as the command structure

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.
        """
        # Send command to reset the system software
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[self.ADDR_SYSTEM_RESET, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Print debug information if specified
        if debug:
            print("System reset command sent.")

    def open_system_brake(self, debug=None):
        """
        This command is used to open the system brake.

        Command Structure:
        - DATA[0]: Command byte (0x77)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - Same as the command structure

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.
        """
        # Send command to open the system brake
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[self.ADDR_BRAKE_OPENING, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Print debug information if specified
        if debug:
            print("System brake opening command sent.")

    def close_system_brake(self, debug=None):
        """
        This command is used to close the system brake.

        Command Structure:
        - DATA[0]: Command byte (0x78)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - Same as the command structure

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.
        """
        # Send command to close the system brake
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[self.ADDR_BRAKE_CLOSE, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        )

        # Print debug information if specified
        if debug:
            print("System brake closing command sent.")

    def set_or_read_CAN_ID(self, read_write_flag, CAN_ID, debug=None):
        """
        This command is used to set and read CAN ID.

        Command Structure:
        - DATA[0]: Command byte (0x79)
        - DATA[1]: NULL byte (0x00)
        - DATA[2]: Read and write flags (bool type, 1 for read, 0 for write)
        - DATA[3]: NULL byte (0x00)
        - DATA[4-7]: CAN ID (uint16_t type)

        Response Structure:
        - Same as the command structure

        Parameters:
        - read_write_flag: Read and write flags (bool type, 1 for read, 0 for write).
        - CAN_ID: CAN ID to set or read (uint16_t type, range 1-32).
        - debug: Boolean flag indicating whether to print debug information.
        """
        # Ensure CAN_ID is within the valid range [1, 32]
        if CAN_ID < 1 or CAN_ID > 32:
            raise ValueError(
                "Invalid CAN ID value. CAN ID must be in the range [1, 32]"
            )

        # Send command to set or read CAN ID
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_CAN_ID_SETTING_AND_READING,
                0x00,
                read_write_flag,
                0x00,
                (CAN_ID >> 0) & 0xFF,
                (CAN_ID >> 8) & 0xFF,
                0x00,
                0x00,
            ],
        )

        # Print debug information if specified
        if debug:
            if read_write_flag:
                print(f"Reading CAN ID: {CAN_ID}")
            else:
                print(f"Setting CAN ID to: {CAN_ID}")

    def multiple_motor_torque_closed_loop(self, debug=None):
        """ "
        The format of the message used to send commands to multiple motors at the same time, as followed:
        Identifier : 0x280
        Frame format : DATA
        Frame type : standard frame
        DLC : 8byte
        The host simultaneously send this command to control the torque current output up to 4 motors.
        Thecontrol value iqControl is int16_t type, the value range is -2000~2000, corresponding to the actual torquecurrent range -32A~32A
        (The bus current and the actual torque of the motor vary from motor tomotor).
        The motor ID should be set to #1~#4, and cannot be repeated, corresponding to the 4 torquecurrentsinthe frame data.

        Data field Description Data
        DATA[0] Torque current 1 control value low byte DATA[0] = *(uint8_t *)(&iqControl_1)
        DATA[1] Torque current 1 control value high byte DATA[1] = *((uint8_t *)(&iqControl_1)+1)
        DATA[2] Torque current 2 control value low byte DATA[2] = *(uint8_t *)(&iqControl_2)
        DATA[3] Torque current 2 control value high byte DATA[3] = *((uint8_t *)(&iqControl_2)+1)
        DATA[4] Torque current 3 control value low byte DATA[4] = *(uint8_t *)(&iqControl_3)
        DATA[5] Torque current 3 control value high byte DATA[5] = *((uint8_t *)(&iqControl_3)+1)
        DATA[6] Torque current 4 control value low byte DATA[6] = *(uint8_t *)(&iqControl_4)
        DATA[7] Torque current 4 control value high byte DATA[7] = *((uint8_t *)(&iqControl_4)+1)

        Driver reply (one frame)
        The message format of each motor reply command is as follows:
        Identifier : 0x140 + ID(1~4)
        Frame format : DATA
        Frame type : standard frame
        DLC : 8byte
        Each motor reply according to the ID from small to large, and the reply data of each motor isthesame as the single motor torque closed-loop control command reply data.
        """
