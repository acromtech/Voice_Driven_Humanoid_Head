import sys
import time
from CanBusGsUsb import CanBusGsUsb


class ProtocolV3(CanBusGsUsb):
    # Attributes

    ERROR_POSITION = 0.1

    BASE_ADDR_ID = 0x140

    ADDR_READ_PID_PARAMETER_TO_RAM = 0x30
    ADDR_WRITE_PID_PARAMETER_TO_RAM = 0x31
    ADDR_WRITE_PID_PARAMETER_TO_ROM = 0x32

    ADDR_READ_ACCELERATION = 0x42
    ADDR_WRITE_ACCELERATION_TO_RAM = 0x43

    ADDR_READ_MULTITURN_ENCODER_POSITION = 0x60
    ADDR_READ_MULTITURN_ENCODER_ORIGINAL_POSITION = 0x61
    ADDR_READ_MULTITURN_ENCODER_ZERO_OFFSET = 0x62
    ADDR_WRITE_MULTITURN_ENCODER_VALUE_TO_ROM_AS_MOTOR_ZERO = 0x63
    ADDR_WRITE_MULTITURN_ENCODER_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO_POSITION = 0x64

    ADDR_READ_MULTITURN_ANGLE = 0x92
    ADDR_READ_MOTOR_STATUS_1_ERROR_FLAG = 0x9A
    ADDR_READ_MOTOR_STATUS_2 = 0x9C
    ADDR_READ_MOTOR_STATUS_3 = 0x9D

    ADDR_SHUTDOWN = 0x80
    ADDR_STOP = 0x81

    ADDR_TORQUE_CLOSED_LOOP_CONTROL = 0xA1
    ADDR_SPEED_CLOSED_LOOP_CONTROL = 0xA2
    ADDR_ABSOLUTE_POSITION_CLOSED_LOOP_CONTROL = 0xA4
    ADDR_INCREMENTAL_POSITION_CLOSED_LOOP_CONTROL = 0xA8

    ADDR_SYSTEM_OPERATING_MODE = 0x70
    ADDR_MOTOR_POWER_ACQUISITION = 0x71
    ADDR_SYSTEM_RESET = 0x76
    ADDR_SYSTEM_BRAKE_RELEASE = 0x77
    ADDR_SYSTEM_BRAKE_LOCK = 0x78

    ADDR_SYSTEM_RUNTIME_READ = 0xB1
    ADDR_SYSTEM_SOFTWARE_VERSION_DATE_READ = 0xB2
    ADDR_COMMUNICATION_INTERRUPTION_PROTECTION_TIME_SETTING = 0xB3
    ADDR_COMMUNICATION_BAUDRATE_SETTING = 0xB4

    ADDR_MULTI_MOTOR = 0x280
    ADDR_CANID_SETTING = 0x79
    ADDR_MOTION_MODE_CONTROL_COMMAND_CAN = 0x400
    ADDR_RS485ID_SETTING = 0x79

    MOTOR_STALL = 0x0002
    LOW_PRESSURE = 0x0004
    OVERVOLTAGE = 0x0008
    OVERCURRENT = 0x0010
    POWER_OVERRUN = 0x0040
    SPEEDING = 0x0100
    MOTOR_TEMP_OVER = 0x1000
    ENCODER_CALIB_ERROR = 0x2000

    def __init__(self, id: int, reducer_ratio: int, can_bus: CanBusGsUsb):
        self.id = id
        self.reducer_ratio = reducer_ratio
        self.can_bus = can_bus

    def read_pid_parameter_to_RAM(self, debug=None):
        """
        Reads the current PID parameters from RAM.

        Command Structure:
        - DATA[0]: Command byte (0x30)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x30)
        - DATA[1]: NULL byte
        - DATA[2]: Position loop Kp
        - DATA[3]: Position loop Ki
        - DATA[4]: Speed loop Kp
        - DATA[5]: Speed loop Ki
        - DATA[6]: Torque loop Kp
        - DATA[7]: Torque loop Ki

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - pid_parameters: Tuple containing the PID parameters in the order (current_loop_KP, current_loop_KI, speed_loop_KP, speed_loop_KI, position_loop_KP, position_loop_KI).
        """
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_PID_PARAMETER_TO_RAM,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )
        current_loop_KP = msg.data[2]
        current_loop_KI = msg.data[3]
        speed_loop_KP = msg.data[4]
        speed_loop_KI = msg.data[5]
        position_loop_KP = msg.data[6]
        position_loop_KI = msg.data[7]

        real_current_loop_KP = msg.data[2] * (
            3 / 256
        )  # assuming that the maximum value of the current loop set by the system is 3
        real_current_loop_KI = msg.data[3] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KP = msg.data[4] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KI = msg.data[5] * (
            0.01 / 256
        )  # assuming that the maximum value of the current loop is 0.01
        real_position_loop_KP = msg.data[6] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_position_loop_KI = msg.data[7] * (
            0.01 / 256
        )  # assuming that the maximum value of the current loop is 0.01

        # Print debug information if specified
        if debug:
            print(
                f"Current loop KP parameters (0-256): {current_loop_KP} \t real: {real_current_loop_KP}"
            )
            print(
                f"Current loop KI parameters (0-256): {current_loop_KI} \t real: {real_current_loop_KI}"
            )
            print(
                f"Speed loop KP parameters (0-256): {speed_loop_KP} \t real: {real_speed_loop_KP}"
            )
            print(
                f"Speed loop KI parameters (0-256): {speed_loop_KI} \t real: {real_speed_loop_KI}"
            )
            print(
                f"Position loop KP parameters (0-256): {position_loop_KP} \t real: {real_position_loop_KP}"
            )
            print(
                f"Position loop KI parameters (0-256): {position_loop_KI} \t real: {real_position_loop_KI}"
            )

        return (
            current_loop_KP,
            current_loop_KI,
            speed_loop_KP,
            speed_loop_KI,
            position_loop_KP,
            position_loop_KI,
        )

    def write_pid_parameter_to_RAM(
        self,
        current_loop_kp,
        current_loop_ki,
        speed_loop_kp,
        speed_loop_ki,
        position_loop_kp,
        position_loop_ki,
        debug=None,
    ):
        """
        Writes the PID parameters to RAM.

        Command Structure:
        - DATA[0]: Command byte (0x31)
        - DATA[1]: NULL byte
        - DATA[2]: Position loop Kp
        - DATA[3]: Position loop Ki
        - DATA[4]: Speed loop Kp
        - DATA[5]: Speed loop Ki
        - DATA[6]: Torque loop Kp
        - DATA[7]: Torque loop Ki

        Response Structure:
        - Same as the sent command.

        Parameters:
        - current_loop_kp: Current loop Kp parameter. (between 0-256)
        - current_loop_ki: Current loop Ki parameter. (between 0-256)
        - speed_loop_kp: Speed loop Kp parameter. (between 0-256)
        - speed_loop_ki: Speed loop Ki parameter. (between 0-256)
        - position_loop_kp: Position loop Kp parameter. (between 0-256)
        - position_loop_ki: Position loop Ki parameter. (between 0-256)
        - debug: Boolean flag indicating whether to print debug information. (True or False)

        Returns:
        - pid_parameters: Tuple containing the PID parameters in the order (current_loop_KP, current_loop_KI, speed_loop_KP, speed_loop_KI, position_loop_KP, position_loop_KI).
        """
        # Check if the parameters are of correct types
        if not all(
            isinstance(param, int)
            for param in [
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ]
        ):
            raise TypeError("PID parameters must be integers.")

        # Ensure the parameters are within the valid range
        if any(
            param < 0
            for param in [
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ]
        ):
            raise ValueError("PID parameters must be non-negative.")
        if any(
            param > 256
            for param in [
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ]
        ):
            raise ValueError("PID parameters can't be up than 256.")

        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_PID_PARAMETER_TO_RAM,
                0x00,
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ],
        )

        # Extract response data
        current_loop_KP = msg.data[2]
        current_loop_KI = msg.data[3]
        speed_loop_KP = msg.data[4]
        speed_loop_KI = msg.data[5]
        position_loop_KP = msg.data[6]
        position_loop_KI = msg.data[7]

        real_current_loop_KP = msg.data[2] * (
            3 / 256
        )  # assuming that the maximum value of the current loop set by the system is 3
        real_current_loop_KI = msg.data[3] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KP = msg.data[4] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KI = msg.data[5] * (
            0.01 / 256
        )  # assuming that the maximum value of the current loop is 0.01
        real_position_loop_KP = msg.data[6] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_position_loop_KI = msg.data[7] * (
            0.01 / 256
        )  # assuming that the maximum value of the current loop is 0.01

        # Print debug information if specified
        if debug:
            print(
                f"Current loop KP parameters set to: {current_loop_KP} \t real: {real_current_loop_KP}"
            )
            print(
                f"Current loop KI parameters set to: {current_loop_KI} \t real: {real_current_loop_KI}"
            )
            print(
                f"Speed loop KP parameters set to: {speed_loop_KP} \t real: {real_speed_loop_KP}"
            )
            print(
                f"Speed loop KI parameters set to: {speed_loop_KI} \t real: {real_speed_loop_KI}"
            )
            print(
                f"Position loop KP parameters set to: {position_loop_KP} \t real: {real_position_loop_KP}"
            )
            print(
                f"Position loop KI parameters set to: {position_loop_KI} \t real: {real_position_loop_KI}"
            )

        return (
            current_loop_KP,
            current_loop_KI,
            speed_loop_KP,
            speed_loop_KI,
            position_loop_KP,
            position_loop_KI,
        )

    def write_pid_parameter_to_ROM(
        self,
        current_loop_kp,
        current_loop_ki,
        speed_loop_kp,
        speed_loop_ki,
        position_loop_kp,
        position_loop_ki,
        debug=None,
    ):
        """
        Writes the PID parameters to ROM.

        Command Structure:
        - DATA[0]: Command byte (0x32)
        - DATA[1]: NULL byte
        - DATA[2]: Position loop Kp
        - DATA[3]: Position loop Ki
        - DATA[4]: Speed loop Kp
        - DATA[5]: Speed loop Ki
        - DATA[6]: Torque loop Kp
        - DATA[7]: Torque loop Ki

        Response Structure:
        - Same as the sent command.

        Parameters:
        - current_loop_kp: Current loop Kp parameter. (between 0-256)
        - current_loop_ki: Current loop Ki parameter. (between 0-256)
        - speed_loop_kp: Speed loop Kp parameter. (between 0-256)
        - speed_loop_ki: Speed loop Ki parameter. (between 0-256)
        - position_loop_kp: Position loop Kp parameter. (between 0-256)
        - position_loop_ki: Position loop Ki parameter. (between 0-256)
        - debug: Boolean flag indicating whether to print debug information. (True or False)

        Returns:
        - pid_parameters: Tuple containing the PID parameters in the order (current_loop_KP, current_loop_KI, speed_loop_KP, speed_loop_KI, position_loop_KP, position_loop_KI).
        """
        # Check if the parameters are of correct types
        if not all(
            isinstance(param, int)
            for param in [
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ]
        ):
            raise TypeError("PID parameters must be integers.")

        # Ensure the parameters are within the valid range
        if any(
            param < 0
            for param in [
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ]
        ):
            raise ValueError("PID parameters must be non-negative.")
        if any(
            param > 256
            for param in [
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ]
        ):
            raise ValueError("PID parameters can't be up than 256.")

        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_PID_PARAMETER_TO_ROM,
                0x00,
                current_loop_kp,
                current_loop_ki,
                speed_loop_kp,
                speed_loop_ki,
                position_loop_kp,
                position_loop_ki,
            ],
        )

        # Extract response data
        current_loop_KP = msg.data[2]
        current_loop_KI = msg.data[3]
        speed_loop_KP = msg.data[4]
        speed_loop_KI = msg.data[5]
        position_loop_KP = msg.data[6]
        position_loop_KI = msg.data[7]

        real_current_loop_KP = msg.data[2] * (
            3 / 256
        )  # assuming that the maximum value of the current loop set by the system is 3
        real_current_loop_KI = msg.data[3] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KP = msg.data[4] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KI = msg.data[5] * (
            0.01 / 256
        )  # assuming that the maximum value of the current loop is 0.01
        real_position_loop_KP = msg.data[6] * (
            0.1 / 256
        )  # assuming that the maximum value of the current loop is 0.1
        real_position_loop_KI = msg.data[7] * (
            0.01 / 256
        )  # assuming that the maximum value of the current loop is 0.01

        # Print debug information if specified
        if debug:
            print(
                f"Current loop KP parameters set to: {current_loop_KP} \t real: {real_current_loop_KP}"
            )
            print(
                f"Current loop KI parameters set to: {current_loop_KI} \t real: {real_current_loop_KI}"
            )
            print(
                f"Speed loop KP parameters set to: {speed_loop_KP} \t real: {real_speed_loop_KP}"
            )
            print(
                f"Speed loop KI parameters set to: {speed_loop_KI} \t real: {real_speed_loop_KI}"
            )
            print(
                f"Position loop KP parameters set to: {position_loop_KP} \t real: {real_position_loop_KP}"
            )
            print(
                f"Position loop KI parameters set to: {position_loop_KI} \t real: {real_position_loop_KI}"
            )

        return (
            current_loop_KP,
            current_loop_KI,
            speed_loop_KP,
            speed_loop_KI,
            position_loop_KP,
            position_loop_KI,
        )

    def read_acceleration(self, debug=None):
        """
        Reads motor acceleration data.

        Command Structure:
        - DATA[0]: Command byte (0x42)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0-3]: Command byte (0x42)
        - DATA[4]: Acceleration low byte 1 (LSB)
        - DATA[5]: Acceleration byte 2
        - DATA[6]: Acceleration byte 3
        - DATA[7]: Acceleration byte 4

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - acceleration_data: Motor acceleration data in degrees per second per second (dps/s).
        """
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
        acceleration_data = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )
        if debug:
            print(f"Acceleration: {acceleration_data} dps/s")
        return acceleration_data

    def write_acceleration_to_RAM(self, acceleration, debug=None):
        """
        Writes acceleration data to RAM.

        Command Structure:
        - DATA[0]: Command byte (0x43)
        - DATA[1]: NULL byte
        - DATA[2]: Position loop I parameter (0x00)
        - DATA[3]: Speed loop P parameter (0x00)
        - DATA[4-7]: Acceleration data (LSB to MSB)

        Response Structure:
        - Same as the host sent

        Parameters:
        - acceleration: Acceleration data to be written.(parameter range: 50-80000 dps/s)
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - acceleration: Acceleration data written.
        """
        # Ensure acceleration is within the valid range
        if acceleration < 50 or acceleration > 80000:
            # Raise a ValueError if acceleration is out of range
            raise ValueError(
                "Invalid acceleration value. Acceleration must be in the range [50, 80000]dps/s to be effective"
            )

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
        acceleration = (
            (msg.data[4] | msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        if debug:
            print("Acceleration set to ", acceleration)

        return acceleration

    def read_multiturn_encoder_position(self, debug=None):
        """
        Reads the encoder multi-turn position from the drive.

        Command Structure:
        - DATA[0]: Command byte (0x60)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x60)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Encoder position (uint32_t, multiturn encoder value range)

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
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

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
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Encoder original position (int32_t, value range)

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
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

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
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Encoder zero offset (int32_t, value range)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_zero_offset: Encoder multi-turn zero offset value.
        """
        # Send command to read encoder multi-turn zero offset value
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_READ_MULTITURN_ENCODER_ZERO_OFFSET,
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
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

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
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Encoder offset value (int32_t, value range)

        Parameters:
        - encoder_offset: Encoder zero offset value to write. (range: 0-4294967295)
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_offset: Encoder zero offset value.
        """

        # Ensure encoder_offset is within the valid range
        if encoder_offset < 0 or encoder_offset > 0xFFFFFFFF:  # 0xFFFFFFFF = 4294967295
            # Raise a ValueError if encoder_offset is out of range
            raise ValueError(
                "Invalid encoder_offset value. encoder_offset must be in the range [0, 4294967295]"
            )

        # Send command to write encoder zero offset value to ROM as motor zero
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_MULTITURN_ENCODER_VALUE_TO_ROM_AS_MOTOR_ZERO,
                0x00,
                0x00,
                0x00,
                (encoder_offset) & 0xFF,
                (encoder_offset >> 8) & 0xFF,
                (encoder_offset >> 16) & 0xFF,
                (encoder_offset >> 24) & 0xFF,
            ],
        )

        # Extract encoder offset value from the response
        encoder_offset = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

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

        Response Structure:
        - DATA[0]: Command byte (0x64)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Encoder offset bytes (uint32_t)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_offset: Encoder offset value.
        """
        # Send command to write current encoder position to ROM as motor zero
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_MULTITURN_ENCODER_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO_POSITION,
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
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[4] << 24)
        )

        # Print debug information if enabled
        if debug is not None:
            print(f"Multiturn encoder offset set to : {encoder_offset}")

        return encoder_offset

    def read_multiturn_encoder_angle(self, debug=None):
        """
        Reads the multi-turn angle of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x92)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x92)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: motor_angle (uint32_t) (0.01°/LSB)

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
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        ) * 0.01

        # Print debug information if enabled
        if debug is not None:
            print(f"Encoder multiturn angle: {motor_angle:.2f}°", end="\r")

        return motor_angle

    def read_motor_status_1_error_flag(self, debug=None):
        """
        Reads the current motor temperature, voltage, and error status flag.

        Command Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1]: Motor temperature (int8_t type, unit 1°C/LSB)
        - DATA[2-3]: NULL
        - DATA[4-5]: Voltage (int16_t type)
        - DATA[6-7]: Error State (int16_t type)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - voltage: Voltage in volts.
        - error_state: Error state flag indicating various motor states. (No error if the returned value is 0)
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
            if error_state & 0x0002:
                print("  - Motor stalled")
            if error_state & 0x0004:
                print("  - Low voltage")
            if error_state & 0x0008:
                print("  - Over-voltage")
            if error_state & 0x0010:
                print("  - Over-current")
            if error_state & 0x0040:
                print("  - Bus current error")
            if error_state & 0x0100:
                print("  - Overspeed")
            if error_state & 0x1000:
                print("  - Motor temperature is overheated")
            if error_state & 0x2000:
                print("  - Encoder calibration error")

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
        - DATA[2-3]: Torque current (int16_t type, 0.01A/LSB)
        - DATA[4-5]: Speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position low byte (int16_t type, 1°/LSB, max range: +-32767°)

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
        torque_current = (msg.data[2] | (msg.data[3] << 8)) * 0.01
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
        - DATA[2-3]: Phase A current (int16_t type, 0.01A/LSB)
        - DATA[4-5]: Phase B current (int16_t type, 0.01A/LSB)
        - DATA[6-7]: Phase C current (int16_t type, 0.01A/LSB)

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
        phase_A_current = (msg.data[2] | (msg.data[3] << 8)) * 0.01
        phase_B_current = (msg.data[4] | (msg.data[5] << 8)) * 0.01
        phase_C_current = (msg.data[6] | (msg.data[7] << 8)) * 0.01

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
        if debug and success == 1:
            print("motor_off: success")

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
        if debug and success == 1:
            print("motor_stop: success")

        return success

    def torque_closed_loop_control(self, torque, timeout=None, debug=None):
        """
        Control the torque current output of the motor.

        Command Structure:
        - DATA[0]: Command byte (0xA1)
        - DATA[1-3]: NULL bytes
        - DATA[4-5]: Torque current control value (int16_t type, 0.01A/LSB)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA1)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, 0.01A/LSB)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (int16_t type, 1°/LSB)

        Parameters:
        - torque: Desired torque value in amperes (range: -327.68 to 327.67).
        - timeout: Timeout value in seconds. If None, there is no timeout.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes.
        - motor_speed: Motor speed in degrees per second.
        - encoder_position: Encoder position value.
        - encoder_position_reducer: Encoder position value with the specific reducer ratio (encoder_position*6, encoder_position*8, ...)
        """
        # Ensure torque is within the valid range
        if torque < -327.68 or torque > 327.67:
            raise ValueError(
                "Invalid torque value. Torque must be in the range [-327.68, 327.67]A"
            )

        # Convert the torque value to the required range
        torque_current_raw = int(torque * 100)

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
        torque_current = (msg.data[2] | (msg.data[3] << 8)) * 0.01
        motor_speed = msg.data[4] | (msg.data[5] << 8)
        encoder_position = msg.data[6] | (msg.data[7] << 8)
        encoder_position_reducer = encoder_position * self.reducer_ratio

        # Record start time
        start_time = time()

        # Espionnage des données critiques du moteur en temps réel
        if debug and timeout is not None and timeout > 0:
            while True:
                # Read current motor angle from multiturn encoder
                motor_angle = self.read_multiturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Print debug information
                print("\033[F\033[K", end="")  # Clear previous debug message
                print(f"Motor temperature: {motor_temp}°C")
                print(f"Torque current: {torque_current:.2f}A")
                print(f"Motor speed: {motor_speed}dps")
                print(f"Motor angle: {motor_angle}°")

                # Exit loop when timeout occurs
                if time() - start_time > timeout:
                    break

        # Check if timeout occurred
        if timeout is not None and time() - start_time > timeout:
            raise TimeoutError("Timeout occurred while waiting for response")

        return (
            motor_temp,
            torque_current,
            motor_speed,
            encoder_position,
            encoder_position_reducer,
        )

    def speed_closed_loop_control(self, speed, timeout=None, debug=None):
        """
        Control the speed of the motor.

        Command Structure:
        - DATA[0]: Command byte (0xA2)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed control value (int32_t type, 0.01 dps/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA2)
        - DATA[1]: Motor temperature (int8_t type, 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, 0.01A/LSB)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (int16_t type, 1°/LSB)

        Parameters:
        - speed: Desired speed value in degrees per second (-327.68 to 327.67 dps).
        - timeout: Timeout value in seconds. If None, there is no timeout.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in degrees Celsius.
        - torque_current: Torque current in amperes.
        - motor_speed: Motor speed in degrees per second.
        - encoder_position: Encoder position value.
        - encoder_position_reducer: Encoder position value with the specific reducer ratio (encoder_position*6, encoder_position*8, ...)
        """
        # Ensure speed is within the valid range
        if speed < -327.68 or speed > 327.67:
            raise ValueError(
                "Invalid speed value. Speed must be in the range [-327.68, 327.67]A"
            )

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
        torque_current = (msg.data[2] | (msg.data[3] << 8)) * 0.01
        motor_speed = msg.data[4] | (msg.data[5] << 8)
        encoder_position = msg.data[6] | (msg.data[7] << 8)
        encoder_position_reducer = encoder_position * self.reducer_ratio

        # Record start time
        start_time = time()

        # Espionnage des données critiques du moteur en temps réel
        if debug and timeout is not None and timeout > 0:
            while True:
                # Read current motor angle from multiturn encoder
                motor_angle = self.read_multiturn_encoder_angle()

                # Read motor status (temperature, torque current, speed)
                motor_temp, torque_current, motor_speed, encoder_position = (
                    self.read_motor_status_2()
                )

                # Print debug information
                print("\033[F\033[K", end="")  # Clear previous debug message
                print(f"Motor temperature: {motor_temp}°C")
                print(f"Torque current: {torque_current:.2f}A")
                print(f"Motor speed: {motor_speed:.2f}dps")
                print(f"Motor angle: {motor_angle}°")

                # Exit loop when timeout occurs
                if time() - start_time > timeout:
                    break

        # Check if timeout occurred
        if timeout is not None and time() - start_time > timeout:
            raise TimeoutError("Timeout occurred while waiting for response")

        return (
            motor_temp,
            torque_current,
            motor_speed,
            encoder_position,
            encoder_position_reducer,
        )

    def absolute_position_closed_loop_control(
        self, max_speed, target_position, wait_for_completion=True, debug=None
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
        - DATA[2-3]: Torque current (int16_t type, 0.01A/LSB)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (int16_t type, 1°/LSB)

        Parameters:
        - max_speed: Maximum speed limit for motor rotation in degrees per second (-32768 to 32767).
        - target_position: Target position in degrees (-21474836.48 to 21474836.47°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature [°C].
        - torque_current: Torque current [A].
        - motor_speed: Motor speed [dps].
        - motor_angle: Current motor angle [°].

        Memo:
        1. The control value angleControl under this command is limited by the Max Angle value in the host computer.
        2. In this control mode, the maximum acceleration of the motor is limited by the Max Acceleration value in the host computer.
        3. In this control mode, the maximum torque current of the motor is limited by the Max TorqueCurrent value in the host computer.
        """
        # Ensure target_position is within the valid range
        if target_position < -21474836.48 or target_position > 21474836.47:
            # Raise a ValueError if target_position is out of range
            raise ValueError(
                "Invalid target position value. Target position must be in the range [-21474836.48, 21474836.47]°"
            )

        # Ensure max_speed is within the valid range
        if max_speed < -32768 or max_speed > 32767:
            # Raise a ValueError if max_speed is out of range
            raise ValueError(
                "Invalid max_speed value. max_speed must be in the range [-32768, 32767]"
            )

        # Convert target_position to multiples of 0.01 degree (0.01 degree/LSB)
        angle_control = int(target_position * 100)

        # Send command to control motor target_position with speed limit
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_ABSOLUTE_POSITION_CLOSED_LOOP_CONTROL,
                0x00,
                (max_speed >> 0) & 0xFF,
                (max_speed >> 8) & 0xFF,
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
                if (
                    abs(motor_angle - target_position) < self.ERROR_POSITION
                    and motor_speed == 0.0
                ):
                    break
        elif debug:
            # Print debug information if specified
            print("Debug information:")
            print(f"Initial position: {self.read_multiturn_encoder_angle()}°")
            print(f"Target position: {target_position}°")

        return motor_temp, torque_current, motor_speed, motor_angle

    def incremental_position_closed_loop_control(
        self, max_speed, target_position, wait_for_completion=True, debug=None
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
        - DATA[2-3]: Torque current (int16_t type, 0.01A/LSB)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (int16_t type, 1°/LSB)

        Parameters:
        - max_speed: Maximum speed limit for motor rotation in degrees per second (-32768 to 32767).
        - target_position: Target position in degrees (-21474836.48 to 21474836.47°).
        - wait_for_completion: Boolean flag indicating whether to wait for the motor to reach the target position.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature [°C].
        - torque_current: Torque current [A].
        - motor_speed: Motor speed [dps].
        - motor_angle: Current motor angle [°].
        """
        # Ensure target_position is within the valid range
        if target_position < -21474836.48 or target_position > 21474836.47:
            # Raise a ValueError if target_position is out of range
            raise ValueError(
                "Invalid target position value. Target position must be in the range [-21474836.48, 21474836.47]°"
            )

        # Ensure max_speed is within the valid range
        if max_speed < -32768 or max_speed > 32767:
            # Raise a ValueError if max_speed is out of range
            raise ValueError(
                "Invalid max_speed value. max_speed must be in the range [-32768, 32767]"
            )

        # Convert target_position to multiples of 0.01 degree (0.01 degree/LSB)
        angle_control = int(target_position * 100)

        # Send command to control motor target_position with specified angle control value and maximum speed limit
        self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_INCREMENTAL_POSITION_CLOSED_LOOP_CONTROL,
                0x00,
                (max_speed >> 0) & 0xFF,
                (max_speed >> 8) & 0xFF,
                (angle_control >> 0) & 0xFF,
                (angle_control >> 8) & 0xFF,
                (angle_control >> 16) & 0xFF,
                (angle_control >> 24) & 0xFF,
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
                    abs(initial_position + target_position - motor_angle)
                    < self.ERROR_POSITION
                    and motor_speed == 0.0
                ):
                    break

        return motor_temp, torque_current, motor_speed, motor_angle

    def read_operating_mode(self, debug=None):
        """
        This command reads the current motor running mode.

        Command Structure:
        - DATA[0]: Command byte (0x70)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x70)
        - DATA[1-6]: NULL bytes
        - DATA[7]: Motor running mode (uint8_t type)
            - 0x01: Current loop mode
            - 0x02: Speed loop mode
            - 0x03: Position loop mode

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - run_mode: Current motor running mode.
        """

        # Send command to read current motor running mode
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_SYSTEM_OPERATING_MODE,
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
            if run_mode == 0x01:
                print("Current loop mode")
            elif run_mode == 0x02:
                print("Current loop mode")
            elif run_mode == 0x03:
                print("Current loop mode")
            else:
                print("Error : Unknown motor running mode")

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
        - DATA[7-8]: Motor running power (uint16_t type, 0.1 watts/LSB)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_power: Current motor power in watts (uint16_t type).
        """

        # Send command to read current motor power
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_MOTOR_POWER_ACQUISITION,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract motor power from the response
        motor_power = (msg.data[6] << 0) | (msg.data[7] << 8) * 0.1

        # Print debug information if specified
        if debug:
            print(f"Motor running power: {motor_power} watts")

        return motor_power

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
            data=[
                self.ADDR_SYSTEM_BRAKE_RELEASE,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
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
            data=[
                self.ADDR_SYSTEM_BRAKE_LOCK,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Print debug information if specified
        if debug:
            print("System brake closing command sent.")

    def read_system_runtime(self, debug=None):
        """
        This command is used to obtain the system running time in ms.

        Command Structure:
        - DATA[0]: Command byte (0xB1)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xB1)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: SysRunTime (uint32_t type, 1ms/LSB)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Return:
        - run_time : system running time [ms]
        """
        # Send command to close the system brake
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_SYSTEM_RUNTIME_READ,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract runtime from the response
        run_time = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Print debug information if specified
        if debug:
            print(f"System runtime is {run_time}")

        return run_time

    def read_system_software_version_date(self, debug=None):
        """
        This command is used to get the update date of the system software version.

        Command Structure:
        - DATA[0]: Command byte (0xB2)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xB2)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: version_date (uint32_t type, 1ms/LSB)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Return:
        - version_date : update date of the system software version (format: [year][month][day])
        """
        # Send command to close the system brake
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_SYSTEM_SOFTWARE_VERSION_DATE_READ,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
            ],
        )

        # Extract runtime from the response
        version_date = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Print debug information if specified
        if debug:
            # Convertir l'entier en chaîne
            date_str = str(version_date)

            # Extraire l'année, le mois et le jour de la chaîne
            year = int(date_str[:4])
            month = int(date_str[4:6])
            day = int(date_str[6:8])

            print(f"System version date is: {year}-{month}-{day}")

        return version_date

    def set_communication_interruption_protection_time(
        self, can_receive_time, debug=None
    ):
        """
        This command is used to set the communication interruption protection time in ms.
        If the communication is interrupted for more than the set time, it will cut off the output brake lock.
        To run again, you need to establish stable and continuous communication first.

        Note: Writing 0 means that the communication interruption protection function is not enabled.

        Command Structure:
        - DATA[0]: Command byte (0xB3)
        - DATA[1-4]: NULL bytes
        - DATA[4-7]: can_receive_time (uint32_t, 1ms/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xB3)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: version_date (uint32_t type, 1ms/LSB)

        Parameters:
        - can_receive_time : time [ms] (range: 0-4294967295)
        - debug: Boolean flag indicating whether to print debug information.

        Return:
        - can_receive_time : receive communication interruption protection time in ms
        """
        # Send command
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_COMMUNICATION_INTERRUPTION_PROTECTION_TIME_SETTING,
                0x00,
                0x00,
                0x00,
                (can_receive_time >> 0) & 0xFF,
                (can_receive_time >> 8) & 0xFF,
                (can_receive_time >> 16) & 0xFF,
                (can_receive_time >> 24) & 0xFF,
            ],
        )

        # Extract runtime from the response
        can_receive_time = (
            msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        )

        # Print debug information if specified
        if debug:
            print(f"Communication interruption protection time: {can_receive_time}ms")

        return can_receive_time

    def set_communication_baudrate(self, baudrate_index, debug=None):
        """
        This instruction can set the communication baudrate of CAN and RS485bus.
        The parameters will be saved in ROM after setting, and will be saved after power off, and will run at the modified baudrate when powered on again.

        Command Structure:
        - DATA[0]: Command byte (0xB4)
        - DATA[1-4]: NULL bytes
        - DATA[4-7]: can_receive_time (uint8_t)

        Response Structure:
        - DATA[0]: Command byte (0xB4)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: version_date (uint32_t type, 1ms/LSB)

        Parameters:
        - baudrate_index (CAN):
            - 0 means 500Kbps baud rate,
            - 1 stands for 1Mbps baud rate
        - debug: Boolean flag indicating whether to print debug information.

        Return:
        - baudrate_value : value of the set baudrate (if value=0 -> Error)
        """
        # Send command
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_COMMUNICATION_BAUDRATE_SETTING,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                baudrate_index,
            ],
        )

        # Extract baudrate from the response
        if msg.data[7] == 0x00:
            baudrate_value = 500000
        elif msg.data[7] == 0x01:
            baudrate_value = 1000000
        else:
            baudrate_value = 0

        # Print debug information if specified
        if debug:
            if baudrate_value == 500000:
                print("Baudrate set to 500Kbps")
            elif baudrate_value == 1000000:
                print("Baudrate set to 1Mbps")
            else:
                print("Error : Unknown baudrate value")

        return baudrate_value

    ######## CHECK MULTI COMMAND CONTROL
    # 3. Multi-motor command (0x280 + command)
    # 3.1. Instruction description
    # The ID number is 280, which means that multiple motors correspond to the same command at the same time.
    # The content and function of the instruction are the same as those of the single-motor instruction.
    # For details, please refer to the single-motor instruction.

    def set_or_read_CAN_ID(self, read_write_flag, CAN_ID, debug=None):
        """
        This command is used to set and read CAN ID.

        Command Structure:
        - DATA[0]: Command byte (0x79)
        - DATA[1]: NULL byte
        - DATA[2]: Read and write flags (bool type, 1 for read, 0 for write)
        - DATA[3-6]: NULL byte
        - DATA[7]: CAN ID (uint8_t type)

        Response Structure:
        - DATA[0]: Command byte (0x79)
        - DATA[1]: NULL byte
        - DATA[2]: Read and write flags (bool type, 1 for read, 0 for write)
        - DATA[3-5]: NULL byte
        - DATA[6-7]: CAN ID (uint16_t type)

        Parameters:
        - read_write_flag: Read and write flags (bool type, 1 for read, 0 for write).
        - CAN_ID: CAN ID to set or read (uint16_t type, range 1-32).
        - debug: Boolean flag indicating whether to print debug information.

        Return:
        - CAN_ID : receive motor CAN ID
        """
        # Ensure CAN_ID is within the valid range [1, 32]
        if CAN_ID < 1 or CAN_ID > 32:
            raise ValueError(
                "Invalid CAN ID value. CAN ID must be in the range [1, 32]"
            )

        # Send command to set or read CAN ID
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_CANID_SETTING,
                0x00,
                read_write_flag,
                0x00,
                0x00,
                0x00,
                0x00,
                CAN_ID,
            ],
        )

        read_write_flag = msg.data[2]
        CAN_ID = msg.data[6] | (msg.data[7] << 8)

        # Print debug information if specified
        if debug:
            if read_write_flag:
                print(f"Reading CAN ID: {CAN_ID}")
            else:
                print(f"Setting CAN ID to: {CAN_ID}")

        return CAN_ID

    def motion_mode_control(self, p_des, v_des, t_ff, kp, kd, debug=None):
        """
        Motion command (0x400+ID)

        Function expression: IqRef = [kp*(p_des - p_fd_actual position) + kd*(v_des- v_fb_actual speed) + t_ff]*KT_torque coefficient;
        IqRef is the output current of the last given motor.

        Command Structure:
        - DATA[0]: p_des[8-15]
        - DATA[1]: p_des[0-7]
        - DATA[2]: v_des[4-11]
        - DATA[3]:
            - 0-3bit: v_des[0-3]
            - 4-7bit: kp[8-11]
        - DATA[4]: kp[0-7]
        - DATA[5]: kd[4-11]
        - DATA[6]:
            - 0-3bit: kd[0-3]
            - 4-7bit: t_ff[8-11]
        - DATA[7]: t_ff[0-7]

        Response Structure:
        - DATA[0]: p_des[8-15]
        - DATA[1]: p_des[0-7]
        - DATA[2]: v_des[4-11]
        - DATA[3]:
            - 0-3bit: v_des[0-3]
            - 4-7bit: kp[8-11]
        - DATA[4]: t_ff[0-7]
        - DATA[5-7]: NULL

        Parameters:
        - p_des (desired position) (-12.5 to 12.5 in rad) - 16bit range
        - v_des(desired velocity) (-45 to 45, in rad/s) - 12bit range
        - t_ff (feedforward torque) (-24 to 24, unit N-m) - 12bit range
        - kp (position deviation coefficient) (0 to 500) - 12bit range
        - kd (speed deviation coefficient) (0 to 5) - 12bit range

        Return:
        - p_des_resp: desired position response
        - v_des_resp: desired velocity response
        - t_ff_resp: feedforward torque response
        """
        # Ensure all parameters is within the valid range
        if p_des < -12.5 or p_des > 12.5:
            raise ValueError(
                "Invalid desired position value. Desired position must be in the range [-12.5, 12.5]rad"
            )
        if v_des < -45 or v_des > 45:
            raise ValueError(
                "Invalid desired velocity value. Desired velocity must be in the range [-45, 45]rad/s"
            )
        if t_ff < -24 or t_ff > 24:
            raise ValueError(
                "Invalid feedforward torque value. Feedforward torque must be in the range [-24, 24]N-m"
            )
        if kp < 0 or kp > 500:
            raise ValueError(
                "Invalid position deviation coefficient value. Position deviation coefficient must be in the range [0, 500]"
            )
        if kd < 0 or kd > 5:
            raise ValueError(
                "Invalid speed deviation coefficient value. Speed deviation coefficient must be in the range [0, 5]"
            )

        # Convert parameters to the appropriate format
        p_des_bytes = [(p_des >> 8) & 0xFF, p_des & 0xFF]
        v_des_bytes = [((v_des >> 4) & 0xF0) | ((kp >> 8) & 0x0F), kp & 0xFF]
        kp_bytes = [((kd >> 4) & 0xF0) | ((t_ff >> 8) & 0x0F), t_ff & 0xFF]

        # Send command
        msg = self.can_bus.sendMessage(
            id=0x400 + self.id,
            data=[self.ADDR_MOTION_MODE_CONTROL_COMMAND_CAN]
            + p_des_bytes
            + v_des_bytes
            + kp_bytes,
        )

        # Extract response data
        p_des_resp = (msg.data[0] << 8) | msg.data[1]
        v_des_resp = ((msg.data[2] & 0xF0) << 4) | (msg.data[3] & 0x0F)
        t_ff_resp = msg.data[4]

        # Print debug information if specified
        if debug:
            print(f"Desired position: {p_des_resp} rad")
            print(f"Desired velocity: {v_des_resp} rad/s")
            print(f"Feedforward torque: {t_ff_resp} N-m")

        return p_des_resp, v_des_resp, t_ff_resp
