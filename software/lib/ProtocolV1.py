from CanBusGsUsb import CanBusGsUsb

class ProtocolV1(CanBusGsUsb):
    # Attributes
    BASE_ADDR_ID = 0x140

    ADDR_READ_PID_PARAMETER_TO_RAM = 0x30
    ADDR_WRITE_PID_PARAMETER_TO_RAM = 0x31
    ADDR_WRITE_PID_PARAMETER_TO_ROM = 0x32
    ADDR_READ_ACCELERATION = 0x33
    ADDR_WRITE_ACCELERATION_TO_RAM = 0x34

    ADDR_SHUTDOWN = 0x80
    ADDR_STOP = 0x81
    ADDR_RUNNING = 0x88

    ADDR_READ_ENCODER_DATA = 0x90
    ADDR_WRITE_ENCODER_OFFSET = 0x91
    ADDR_WRITE_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO_POSITION = 0x19
    ADDR_READ_MULTITURN_ENCODER_POSITION = 0x92
    ADDR_READ_SINGLETURN_ENCODER_POSITION = 0x94

    ADDR_READ_MOTOR_STATUS_1_ERROR_FLAG = 0x9A
    ADDR_READ_CLEAR_MOTOR_ERROR_FLAG = 0x9B
    ADDR_READ_MOTOR_STATUS_2 = 0x9C
    ADDR_READ_MOTOR_STATUS_3 = 0x9D

    ADDR_TORQUE_CLOSED_LOOP_CONTROL = 0xA1
    ADDR_SPEED_CLOSED_LOOP_CONTROL = 0xA2
    ADDR_WRITE_POSITION_MULTITURN_CLOSED_LOOP_CONTROL = 0xA3
    ADDR_WRITE_POSITION_MULTITURN_SPEED_CLOSED_LOOP_CONTROL = 0xA4
    ADDR_WRITE_SINGLETURN_DIRECTION_CLOSED_LOOP_CONTROL = 0xA5
    ADDR_WRITE_SINGLETURN_SPEED_DIRECTION_CLOSED_LOOP_CONTROL = 0xA6

    MOTOR_STALL = 0x0002
    LOW_PRESSURE = 0x0004
    OVERVOLTAGE = 0x0008
    OVERCURRENT = 0x0010
    POWER_OVERRUN = 0x0040
    SPEEDING = 0x0100
    MOTOR_TEMP_OVER = 0x1000
    ENCODER_CALIB_ERROR = 0x2000

    def __init__(self,id:int,reducer_ratio:int,can_bus:CanBusGsUsb):
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
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_PID_PARAMETER_TO_RAM, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        current_loop_KP = msg.data[2]
        current_loop_KI = msg.data[3]
        speed_loop_KP = msg.data[4]
        speed_loop_KI = msg.data[5]
        position_loop_KP = msg.data[6]
        position_loop_KI = msg.data[7]

        real_current_loop_KP = msg.data[2] * (3/256) # assuming that the maximum value of the current loop set by the system is 3
        real_current_loop_KI = msg.data[3] * (0.1/256) # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KP = msg.data[4] * (0.1/256) # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KI = msg.data[5] * (0.01/256)  # assuming that the maximum value of the current loop is 0.01
        real_position_loop_KP = msg.data[6] * (0.1/256)  # assuming that the maximum value of the current loop is 0.1
        real_position_loop_KI = msg.data[7] * (0.01/256)  # assuming that the maximum value of the current loop is 0.01

        # Print debug information if specified
        if debug:
            print(f"Current loop KP parameters (0-256): {current_loop_KP} \t real: {real_current_loop_KP}")
            print(f"Current loop KI parameters (0-256): {current_loop_KI} \t real: {real_current_loop_KI}")
            print(f"Speed loop KP parameters (0-256): {speed_loop_KP} \t real: {real_speed_loop_KP}")
            print(f"Speed loop KI parameters (0-256): {speed_loop_KI} \t real: {real_speed_loop_KI}")
            print(f"Position loop KP parameters (0-256): {position_loop_KP} \t real: {real_position_loop_KP}")
            print(f"Position loop KI parameters (0-256): {position_loop_KI} \t real: {real_position_loop_KI}")

        return current_loop_KP, current_loop_KI, speed_loop_KP, speed_loop_KI, position_loop_KP, position_loop_KI

    def write_pid_parameter_to_RAM(self, current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki, debug=None):
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
        if not all(isinstance(param, int) for param in [current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki]):
            raise TypeError("PID parameters must be integers.")

        # Ensure the parameters are within the valid range
        if any(param < 0 for param in [current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki]):
            raise ValueError("PID parameters must be non-negative.")
        if any(param > 256 for param in [current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki]):
                raise ValueError("PID parameters can't be up than 256.")
        
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_WRITE_PID_PARAMETER_TO_RAM, 0x00, current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki])

        # Extract response data
        current_loop_KP = msg.data[2]
        current_loop_KI = msg.data[3]
        speed_loop_KP = msg.data[4]
        speed_loop_KI = msg.data[5]
        position_loop_KP = msg.data[6]
        position_loop_KI = msg.data[7]

        real_current_loop_KP = msg.data[2] * (3/256) # assuming that the maximum value of the current loop set by the system is 3
        real_current_loop_KI = msg.data[3] * (0.1/256) # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KP = msg.data[4] * (0.1/256) # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KI = msg.data[5] * (0.01/256)  # assuming that the maximum value of the current loop is 0.01
        real_position_loop_KP = msg.data[6] * (0.1/256)  # assuming that the maximum value of the current loop is 0.1
        real_position_loop_KI = msg.data[7] * (0.01/256)  # assuming that the maximum value of the current loop is 0.01

        # Print debug information if specified
        if debug:
            print(f"Current loop KP parameters set to: {current_loop_KP} \t real: {real_current_loop_KP}")
            print(f"Current loop KI parameters set to: {current_loop_KI} \t real: {real_current_loop_KI}")
            print(f"Speed loop KP parameters set to: {speed_loop_KP} \t real: {real_speed_loop_KP}")
            print(f"Speed loop KI parameters set to: {speed_loop_KI} \t real: {real_speed_loop_KI}")
            print(f"Position loop KP parameters set to: {position_loop_KP} \t real: {real_position_loop_KP}")
            print(f"Position loop KI parameters set to: {position_loop_KI} \t real: {real_position_loop_KI}")

        return current_loop_KP, current_loop_KI, speed_loop_KP, speed_loop_KI, position_loop_KP, position_loop_KI
	
    def write_pid_parameter_to_ROM(self, current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki, debug=None):
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
        if not all(isinstance(param, int) for param in [current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki]):
            raise TypeError("PID parameters must be integers.")

        # Ensure the parameters are within the valid range
        if any(param < 0 for param in [current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki]):
            raise ValueError("PID parameters must be non-negative.")
        if any(param > 256 for param in [current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki]):
                raise ValueError("PID parameters can't be up than 256.")
    
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_WRITE_PID_PARAMETER_TO_ROM, 0x00, current_loop_kp, current_loop_ki, speed_loop_kp, speed_loop_ki, position_loop_kp, position_loop_ki])
        
        # Extract response data
        current_loop_KP = msg.data[2]
        current_loop_KI = msg.data[3]
        speed_loop_KP = msg.data[4]
        speed_loop_KI = msg.data[5]
        position_loop_KP = msg.data[6]
        position_loop_KI = msg.data[7]

        real_current_loop_KP = msg.data[2] * (3/256) # assuming that the maximum value of the current loop set by the system is 3
        real_current_loop_KI = msg.data[3] * (0.1/256) # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KP = msg.data[4] * (0.1/256) # assuming that the maximum value of the current loop is 0.1
        real_speed_loop_KI = msg.data[5] * (0.01/256)  # assuming that the maximum value of the current loop is 0.01
        real_position_loop_KP = msg.data[6] * (0.1/256)  # assuming that the maximum value of the current loop is 0.1
        real_position_loop_KI = msg.data[7] * (0.01/256)  # assuming that the maximum value of the current loop is 0.01

        # Print debug information if specified
        if debug:
            print(f"Current loop KP parameters set to: {current_loop_KP} \t real: {real_current_loop_KP}")
            print(f"Current loop KI parameters set to: {current_loop_KI} \t real: {real_current_loop_KI}")
            print(f"Speed loop KP parameters set to: {speed_loop_KP} \t real: {real_speed_loop_KP}")
            print(f"Speed loop KI parameters set to: {speed_loop_KI} \t real: {real_speed_loop_KI}")
            print(f"Position loop KP parameters set to: {position_loop_KP} \t real: {real_position_loop_KP}")
            print(f"Position loop KI parameters set to: {position_loop_KI} \t real: {real_position_loop_KI}")

        return current_loop_KP, current_loop_KI, speed_loop_KP, speed_loop_KI, position_loop_KP, position_loop_KI

    def read_acceleration(self, debug=None):
        """
        Reads motor acceleration data.

        Command Structure:
        - DATA[0]: Command byte (0x33)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x33)
        - DATA[1]: NULL byte
        - DATA[2]: Position loop P parameter (0x00)
        - DATA[3]: Position loop I parameter (0x00)
        - DATA[4]: Speed loop P parameter (LSB)
        - DATA[5]: Speed loop P parameter (MSB)
        - DATA[6]: Torque loop P parameter (Byte 2)
        - DATA[7]: Torque loop P parameter (Byte 3)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - acceleration_data: Motor acceleration data in degrees per second per second (dps/s).
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_ACCELERATION, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        acceleration_data = (msg.data[4] | (msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24))
        if debug:
            print(f"Acceleration: {acceleration_data} dps/s")
        return acceleration_data

    def write_acceleration_to_RAM(self, acceleration, debug=None):
        """
        Writes acceleration data to RAM.

        Command Structure:
        - DATA[0]: Command byte (0x34)
        - DATA[1]: NULL byte
        - DATA[2]: Position loop I parameter (0x00)
        - DATA[3]: Speed loop P parameter (0x00)
        - DATA[4-7]: Acceleration data (LSB to MSB)

        Response Structure:
        - Same as the host sent

        Parameters:
        - acceleration: Acceleration data to be written. Should be a uint32_t.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - acceleration: Acceleration data written.
        """
        # Ensure acceleration is within the valid range [0, 0xFFFFFFFF] (uint32_t)
        if acceleration < 0 or acceleration > 0xFFFFFFFF:
            # Raise a ValueError if acceleration is out of range
            raise ValueError("Invalid acceleration value. Acceleration must be in the range [0, 4294967295]dps/s")

        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_WRITE_ACCELERATION_TO_RAM, 0x00, 0x00, 0x00, (acceleration >> 0) & 0xFF,(acceleration >> 8) & 0xFF,(acceleration >> 16) & 0xFF,(acceleration >> 24) & 0xFF])
        acceleration = (msg.data[4] | msg.data[5] << 8) | (msg.data[6] << 16) | (msg.data[7] << 24)
        
        if debug:
            print("Acceleration set to ", acceleration)
        
        return acceleration

    def read_encoder_data(self, debug=None):
        """
        Reads the current position of the encoder.

        Command Structure:
        - DATA[0]: Command byte (0x90)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x90)
        - DATA[1-2]: Encoder position (LSB to MSB)
        - DATA[3-4]: Encoder original position (LSB to MSB)
        - DATA[5-6]: Encoder offset (LSB to MSB)
        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - current_position: Current position of the encoder.
        - original_position: Original position of the encoder.
        - encoder_offset: Offset of the encoder.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_ENCODER_DATA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        
        # Extracting encoder data from the response
        current_position = (msg.data[2] | (msg.data[3] << 8)) * (360 / 65535)
        original_position = (msg.data[4] | (msg.data[5] << 8)) * (360 / 65535)
        encoder_offset = (msg.data[6] | (msg.data[7] << 8)) * (360 / 65535)
        
        # Print debug information if specified
        if debug:
            print(f"Motor position: {current_position}")
            print(f"Motor original position: {original_position}")
            print(f"Motor offset: {encoder_offset}")
        
        return current_position, original_position, encoder_offset
	
    def write_encoder_offset(self, offset, debug=None):
        """
        Sets the encoder offset.

        Command Structure:
        - DATA[0]: Command byte (0x91)
        - DATA[1-5]: NULL bytes
        - DATA[6]: Encoder offset (LSB)
        - DATA[7]: Encoder offset (MSB)

        Response Structure:
        - DATA[0]: Command byte (0x91)
        - DATA[1-7]: Same as request (echoed)

        Parameters:
        - offset: Encoder offset to be set. Should be an integer.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - new_encoder_offset: The new encoder offset.
        """
        # Ensure offset is within the valid range [0, 65535] (uint16_t)
        if not isinstance(offset, int) or offset < 0 or offset > 65535:
            # Raise a ValueError if offset is out of range or not an integer
            raise ValueError("Invalid encoder offset value. Offset must be an integer in the range [0, 65535]")
        
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_WRITE_ENCODER_OFFSET, 0x00, 0x00, 0x00, 0x00, 0x00, (offset) & 0xFF, ((offset) & 0xFF00) >> 8])
        new_encoder_offset = (msg.data[6] | (msg.data[7] << 8))
        
        # Print debug information if specified
        if debug:
            print(f"Encoder offset set to {new_encoder_offset}")
        
        return new_encoder_offset
	
    def write_current_position_to_ROM_as_motor_zero_position(self, debug=None):
        """
        Writes the current position to ROM as the motor zero position.

        Notice:
        - This command needs to be powered on again to take effect.
        - Multiple writes will affect the chip life, so it's not recommended to use it frequently.

        Command Structure:
        - DATA[0]: Command byte (0x19)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x19)
        - DATA[1-5]: NULL bytes
        - DATA[6]: Encoder offset (LSB)
        - DATA[7]: Encoder offset (MSB)
        
        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - encoder_offset: The encoder offset.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_WRITE_CURRENT_POSITION_TO_ROM_AS_MOTOR_ZERO_POSITION, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        encoder_offset = (msg.data[6] | (msg.data[7] << 8))
        
        # Print debug information if specified
        if debug:
            print(f"Initial position set to {encoder_offset}")
        
        return encoder_offset
	
    def read_multiturn_encoder_position(self, debug=None):
        """
        Reads the multi-turn angle of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x92)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x92)
        - DATA[1-7]: Angle bytes (LSB to MSB)

        Parameters:
        - motor_angle: Motor angle in degrees (float), positive value indicates clockwise cumulative angle,
                        negative value indicates counterclockwise cumulative angle, unit: 0.01 ° / LSB.

        Returns:
        - motor_angle: Motor angle in degrees (float).
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_MULTITURN_ENCODER_POSITION, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        motor_angle = (msg.data[1] | (msg.data[2] << 8) | (msg.data[3] << 16) | (msg.data[4] << 24) | (msg.data[5] << 32) | (msg.data[6] << 40) | (msg.data[7] << 48)) * 0.01
        if debug !=None : print(f"Encoder multiturn position: {motor_angle:.2f}°",end='\r')
        return motor_angle
	
    def read_singleturn_encoder_position(self, debug=None):
        """
        Reads the single circle angle of the motor.

        Command Structure:
        - DATA[0]: Command byte (0x94)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x94)
        - DATA[1-2]: Single angle bytes (LSB to MSB)

        Parameters:
        - circle_angle: Circle angle of the motor in degrees (float), starting from the encoder zero point, increased by clockwise rotation,
                        and returning to zero when it reaches zero again, the unit is 0.01°/LSB.

        Returns:
        - circle_angle: Circle angle of the motor in degrees (float).
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_SINGLETURN_ENCODER_POSITION, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        circle_angle = (msg.data[6] | (msg.data[7] << 8)) * 0.01
        if debug != None: print(f"Encoder singleturn position: {circle_angle:.2f}°",end='\r')
        return circle_angle

    def motor_off(self, debug=None): 
        """
        Turns off the motor, clearing the motor operating status and previously received control commands.

        Command Structure:
        - DATA[0]: Command byte (0x80)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x80)
        - DATA[1-7]: NULL bytes

        Returns:
        - status: Integer indicating success (1) or failure (0) of the motor off command.
        """
        msg = self.can_bus.sendMessage(self.BASE_ADDR_ID + self.id, [self.ADDR_SHUTDOWN, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        if msg.can_id == self.BASE_ADDR_ID + self.id and msg.data[0]==self.ADDR_SHUTDOWN and msg.data[1]==0x00 and msg.data[2]==0x00 and msg.data[3]==0x00 and msg.data[4]==0x00 and msg.data[5]==0x00 and msg.data[6]==0x00 and msg.data[7]==0x00 : return 1
        else : return 0

    def stop(self, debug=None):
        """
        Stops the motor, but does not clear the motor operating state and previously received control commands.

        Command Structure:
        - DATA[0]: Command byte (0x81)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x81)
        - DATA[1-7]: NULL bytes

        Returns:
        - status: Integer indicating success (1) or failure (0) of the stop command.
        """
        msg = self.can_bus.sendMessage(self.BASE_ADDR_ID + self.id, [self.ADDR_STOP, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        if msg.can_id == self.BASE_ADDR_ID + self.id and msg.data[0]==self.ADDR_STOP and msg.data[1]==0x00 and msg.data[2]==0x00 and msg.data[3]==0x00 and msg.data[4]==0x00 and msg.data[5]==0x00 and msg.data[6]==0x00 and msg.data[7]==0x00 : return 1
        else : return 0
	
    def running(self, debug=None):
        """
        Resumes motor operation from a motor stop command (Recovers control mode before stopping the motor).

        Command Structure:
        - DATA[0]: Command byte (0x88)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x88)
        - DATA[1-7]: NULL bytes

        Returns:
        - status: Integer indicating success (1) or failure (0) of the running command.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_RUNNING, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        if msg.can_id == self.BASE_ADDR_ID + self.id and msg.data[0]==self.ADDR_RUNNING and msg.data[1]==0x00 and msg.data[2]==0x00 and msg.data[3]==0x00 and msg.data[4]==0x00 and msg.data[5]==0x00 and msg.data[6]==0x00 and msg.data[7]==0x00 : return 1
        else : return 0

    def read_motor_status_1_error_flag(self, debug=None):
        """
        Reads the motor's error status, temperature, voltage, and other information.

        Command Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2]: NULL byte
        - DATA[3-4]: Voltage (uint16_t type, unit 0.1V/LSB)
        - DATA[5-6]: NULL bytes
        - DATA[7]: Error State (uint8_t type, each bit represents a different motor state)

        Memo:
        Error State:
        - Bit 0: Voltage status (0: Normal, 1: Low voltage protection)
        - Bit 3: Temperature status (0: Normal, 1: Over-temperature protection)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - voltage: Voltage in volts.
        - error_state: Error state bitmask.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_MOTOR_STATUS_1_ERROR_FLAG, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        motor_temp = msg.data[1]
        voltage = (msg.data[3] | (msg.data[4] << 8)) * 0.1
        error_state = msg.data[6] | (msg.data[7] << 8)
        if debug != None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Voltage: {voltage}V")
            if error_state == 0x00:
                print("Voltage status: OK")
                print("Temperature status: OK")
            else:
                if error_state & self.LOW_PRESSURE:         print("Voltage status: low voltage protection")
                if error_state & self.OVERVOLTAGE:          print("Voltage status: overvoltage protection")
                if error_state & self.OVERCURRENT:          print("Voltage status: overcurrent protection")
                if error_state & self.POWER_OVERRUN:        print("Voltage status: power overrun")
                if error_state & self.SPEEDING:             print("Voltage status: speeding")
                if error_state & self.MOTOR_TEMP_OVER:      print("Temperature status: over temperature protection")
                if error_state & self.ENCODER_CALIB_ERROR:  print("Error status: encoder calibration error")
        return motor_temp,voltage,error_state
	
    def read_clear_motor_error_flag(self, debug=None):
        """
        Clears the error status of the current motor and retrieves motor information.

        Command Structure:
        - DATA[0]: Command byte (0x9B)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9A)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2]: NULL byte
        - DATA[3-4]: Voltage (uint16_t type, unit 0.1V/LSB)
        - DATA[5-6]: NULL bytes
        - DATA[7]: Error State (uint8_t type, each bit represents a different motor state)

        Memo:
        - The error flag cannot be cleared when the motor status does not return to normal.
        - Error State:
            - Bit 0: Voltage status (0: Normal, 1: Low voltage protection)
            - Bit 3: Temperature status (0: Normal, 1: Over-temperature protection)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - voltage: Voltage in volts.
        - error_state: Error state bitmask.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_CLEAR_MOTOR_ERROR_FLAG, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        motor_temp = msg.data[1]
        voltage = (msg.data[3] | (msg.data[4] << 8)) * 0.1
        error_state = msg.data[6] | (msg.data[7] << 8)
        if debug != None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Voltage: {voltage}V")
            if error_state == 0x00:
                print("Voltage status: OK")
                print("Temperature status: OK")
            else:
                if error_state & self.LOW_PRESSURE:print("Voltage status: low voltage protection")
                if error_state & self.OVERVOLTAGE:print("Voltage status: overvoltage protection")
                if error_state & self.OVERCURRENT:print("Voltage status: overcurrent protection")
                if error_state & self.POWER_OVERRUN:print("Voltage status: power overrun")
                if error_state & self.SPEEDING:print("Voltage status: speeding")
                if error_state & self.MOTOR_TEMP_OVER:print("Temperature status: over temperature protection")
                if error_state & self.ENCODER_CALIB_ERROR:print("Error status: encoder calibration error")
        return motor_temp, voltage, error_state
	
    def read_motor_status_2(self, debug=None):
        """
        Reads motor temperature, voltage, speed, and encoder position.

        Command Structure:
        - DATA[0]: Command byte (0x9C)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9C)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, Range: -2048~2048, real torque current range: -33A~33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14bit encoder value range 0~16383)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current in Amperes.
        - motor_speed: Motor speed in degrees per second (dps).
        - encoder_position: Encoder position value.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_MOTOR_STATUS_2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        motor_temp = msg.data[1]
        torque_current = (msg.data[2] | (msg.data[3] << 8))
        motor_speed = (msg.data[4] | (msg.data[5] << 8))
        encoder_position = (msg.data[6] | (msg.data[7] << 8))
        if debug!=None :
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Encoder position: {encoder_position}")
        return motor_temp, torque_current, motor_speed, encoder_position
    
    def read_motor_status_3(self, debug=None):
        """
        Reads motor status 3, which includes phase current data.

        Command Structure:
        - DATA[0]: Command byte (0x9D)
        - DATA[1-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0x9D)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Phase A current (int16_t type, 1A/64LSB)
        - DATA[4-5]: Phase B current (int16_t type, 1A/64LSB)
        - DATA[6-7]: Phase C current (int16_t type, 1A/64LSB)

        Parameters:
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - phase_A_current: Phase A current in Amperes.
        - phase_B_current: Phase B current in Amperes.
        - phase_C_current: Phase C current in Amperes.
        """
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_READ_MOTOR_STATUS_3, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
        motor_temp = msg.data[1]
        phase_A_current = (msg.data[2] | (msg.data[3] << 8)) * 0.01
        phase_B_current = (msg.data[4] | (msg.data[5] << 8)) * 0.01
        phase_C_current = (msg.data[6] | (msg.data[7] << 8)) * 0.01
        if debug!=None :
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Phase A current: {phase_A_current}A")
            print(f"Phase B current: {phase_B_current}A")
            print(f"Phase C current: {phase_C_current}A")
        return motor_temp, phase_A_current, phase_B_current, phase_C_current

    def torque_closed_loop_control(self, torque, debug=None):
        """
        Controls the torque current output of the motor.

        Parameters:
        - torque: Torque current value to set, in Amperes.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current value in Amperes (-2048 to 2048).
        - motor_speed: Motor speed in degrees per second.
        - encoder_position: Encoder position value.

        Command Structure:
        - DATA[0]: Command byte (0xA1)
        - DATA[1-3]: NULL bytes
        - DATA[4-5]: Torque current control value (int16_t type, -2000 to 2000, corresponds to -32A to 32A)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA1)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, -2048 to 2048, real torque current range: -33A to 33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14-bit encoder value range 0 to 16383)
        """
        torque = int(torque * 100)
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_TORQUE_CLOSED_LOOP_CONTROL, 0x00, 0x00, 0x00, (torque >> 0) & 0xFF, (torque >> 8) & 0xFF, 0x00, 0x00])
        motor_temp = msg.data[1]
        torque_current = (msg.data[2] | (msg.data[3] << 8))
        motor_speed = (msg.data[4] | (msg.data[5] << 8))
        encoder_position = (msg.data[6] | (msg.data[7] << 8))
        if debug!=None :
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current value (-2048~2048): {torque_current}")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor position value (0~16383): {encoder_position}")
        return motor_temp, torque_current, motor_speed, encoder_position

    def speed_closed_loop_control(self, speed, debug=None):
        """
        Controls the speed of the motor.

        Parameters:
        - speed: Speed control value to set, in degrees per second (dps).
        - debug: Boolean flag indicating whether to print debug information.

        Command Structure:
        - DATA[0]: Command byte (0xA2)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Speed control value (int32_t type, corresponds to actual speed of 0.01dps/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA2)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, -2048 to 2048, real torque current range: -33A to 33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14-bit encoder value range 0 to 16383)

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current value in Amperes (-2048 to 2048).
        - motor_speed: Motor speed in degrees per second (dps).
        - encoder_position: Encoder position value.
        """
        speed = int(speed * 100)
        msg = self.can_bus.sendMessage(id=self.BASE_ADDR_ID + self.id, data=[self.ADDR_SPEED_CLOSED_LOOP_CONTROL, 0x00, 0x00, 0x00, (speed >> 0) & 0xFF, (speed >> 8) & 0xFF, (speed >> 16) & 0xFF, (speed >> 24) & 0xFF])
        motor_temp = msg.data[1]
        torque_current = (msg.data[2] | (msg.data[3] << 8))
        motor_speed = (msg.data[4] | (msg.data[5] << 8))
        encoder_position = (msg.data[6] | (msg.data[7] << 8))
        if debug!=None :
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current value (-2048~2048): {torque_current}")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor position value (0~16383): {encoder_position}")
        return motor_temp, torque_current, motor_speed, encoder_position

    def position_closed_loop_control_1(self, position, debug=None):
        """
        Controls the position of the motor in multi-turn angle.

        Parameters:
        - position: Target position to set, in degrees.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current value in Amperes (-2048 to 2048).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Command Structure:
        - DATA[0]: Command byte (0xA3)
        - DATA[1-3]: NULL bytes
        - DATA[4-7]: Position control value (int32_t type, actual position is 0.01degree/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA3)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, -2048 to 2048, real torque current range: -33A to 33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14-bit encoder value range 0 to 16383)
        """
        position_control = int(position * 100)
        max_position = 2**32  # Maximum value for uint32_t
        tolerance = 0.2  # Tolerance in degrees

        # Send position control command to the motor
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_POSITION_MULTITURN_CLOSED_LOOP_CONTROL, 0x00, 0x00, 0x00,
                (position_control >> 0) & 0xFF, 
                (position_control >> 8) & 0xFF,
                (position_control >> 16) & 0xFF, 
                (position_control >> 24) & 0xFF
            ]
        )

        while True:
            # Read the current motor angle and status
            motor_angle = self.read_multiturn_encoder_position(debug=True)
            motor_temp, torque_current, motor_speed, encoder_position = self.read_motor_status_2()

            # Handle overflow case (motor_angle near max_position and position near 0)
            if position == 0:
                # Adjust motor_angle for overflow
                if motor_angle > max_position - tolerance:
                    motor_angle = motor_angle - max_position

            # Check if the motor is within the target range and stopped
            if abs(motor_angle - position) < tolerance and motor_speed == 0.0:
                break

        # Optionally print debug information
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor angle: {motor_angle}°")

        return motor_temp, torque_current, motor_speed, motor_angle


    def position_closed_loop_control_2(self, speed, position, debug=None):
        """
        Controls the position of the motor (multi-turn angle) with speed limit.

        Parameters:
        - speed: Maximum speed limit in degrees per second (dps).
        - position: Target position to set, in degrees.
        - debug: Boolean flag indicating whether to print debug information.
        
        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current value in Amperes (-2048 to 2048).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Command Structure:
        - DATA[0]: Command byte (0xA4)
        - DATA[1]: NULL byte
        - DATA[2-3]: Speed limit (uint16_t type, actual speed of 1dps/LSB)
        - DATA[4-7]: Position control value (int32_t type, actual position is 0.01degree/LSB)

        Response Structure:
        - DATA[0]: Command byte (0xA4)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, -2048 to 2048, real torque current range: -33A to 33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14-bit encoder value range 0 to 16383)
        """
        max_speed = speed & 0xFFFF
        angle_control = int(position * 100)
        max_position = 2**32  # Maximum value for uint32_t
        tolerance = 0.5  # Tolerance in degrees

        # Send position control command to the motor
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_POSITION_MULTITURN_SPEED_CLOSED_LOOP_CONTROL, 0x00,
                (max_speed >> 0) & 0xFF, 
                (max_speed >> 8) & 0xFF,
                (angle_control >> 0) & 0xFF, 
                (angle_control >> 8) & 0xFF,
                (angle_control >> 16) & 0xFF, 
                (angle_control >> 24) & 0xFF
            ]
        )

        while True:
            # Read the current motor angle and status
            motor_angle = self.read_multiturn_encoder_position(debug=True)
            motor_temp, torque_current, motor_speed, encoder_position = self.read_motor_status_2()

            # Handle overflow case (motor_angle near max_position and position near 0)
            if position == 0:
                # Adjust motor_angle for overflow
                if motor_angle > max_position - tolerance:
                    motor_angle = motor_angle - max_position

            # Check if the motor is within the target range and stopped
            if abs(motor_angle - position) < tolerance and motor_speed == 0.0:
                break

        # Optionally print debug information
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor angle: {motor_angle}°")

        return motor_temp, torque_current, motor_speed, motor_angle


    def position_closed_loop_control_3(self, direction, position, debug=None):
        """
        Controls the position of the motor (single-turn angle) with specified direction.

        Parameters:
        - direction: Direction of rotation (0 for clockwise, 1 for counterclockwise).
        - position: Target position to set, in degrees.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current value in Amperes (-2048 to 2048).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Command Structure:
        - DATA[0]: Command byte (0xA5)
        - DATA[1]: Spin Direction byte (0x00 for clockwise, 0x01 for counterclockwise)
        - DATA[2-3]: NULL bytes
        - DATA[4-5]: Position control value (uint16_t type, 0~35999, actual position is 0.01degree/LSB)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA5)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, -2048 to 2048, real torque current range: -33A to 33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14-bit encoder value range 0 to 16383)
        """
        angle_control = int(position * 100)  # Convert position to 0.01°/LSB
        max_angle = 360.0  # Maximum angle for single-turn control
        tolerance = 0.5  # Tolerance in degrees

        # Send the position control command to the motor
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SINGLETURN_DIRECTION_CLOSED_LOOP_CONTROL,
                direction & 0xFF,  # Direction (0: CW, 1: CCW)
                0x00, 0x00,
                (angle_control >> 0) & 0xFF,
                (angle_control >> 8) & 0xFF,
                0x00, 0x00
            ]
        )

        while True:
            # Read the current motor angle and status
            motor_angle = self.read_singleturn_encoder_position(debug=True)
            motor_temp, torque_current, motor_speed, encoder_position = self.read_motor_status_2()

            # Handle overflow case for single-turn (e.g., motor_angle near 360° and position near 0°)
            if abs(motor_angle - position) > max_angle - tolerance:
                # Normalize motor_angle to account for the overflow
                if motor_angle > position:
                    motor_angle -= max_angle
                else:
                    motor_angle += max_angle

            # Check if the motor is within the target range and stopped
            if abs(motor_angle - position) < tolerance and motor_speed == 0.0:
                break

        # Optionally print debug information
        if debug is not None:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor angle: {motor_angle}°")

        return motor_temp, torque_current, motor_speed, motor_angle

	
    def position_closed_loop_control_4(self, speed, direction, position, debug=None):
        """
        Controls the position of the motor (single-turn angle) with specified direction and speed limit.

        Parameters:
        - speed: Maximum speed limit for motor rotation, in degrees per second (dps).
        - direction: Direction of rotation (0 for clockwise, 1 for counterclockwise).
        - position: Target position to set, in degrees.
        - debug: Boolean flag indicating whether to print debug information.

        Returns:
        - motor_temp: Motor temperature in Celsius.
        - torque_current: Torque current value in Amperes (-2048 to 2048).
        - motor_speed: Motor speed in degrees per second (dps).
        - motor_angle: Current motor angle in degrees.

        Command Structure:
        - DATA[0]: Command byte (0xA6)
        - DATA[1]: Spin Direction byte (0x00 for clockwise, 0x01 for counterclockwise)
        - DATA[2-3]: Speed limit value (uint16_t type, maximum speed in dps)
        - DATA[4-5]: Position control value (uint16_t type, 0~35999, actual position is 0.01degree/LSB)
        - DATA[6-7]: NULL bytes

        Response Structure:
        - DATA[0]: Command byte (0xA6)
        - DATA[1]: Motor temperature (int8_t type, unit 1℃/LSB)
        - DATA[2-3]: Torque current (int16_t type, -2048 to 2048, real torque current range: -33A to 33A)
        - DATA[4-5]: Motor speed (int16_t type, 1dps/LSB)
        - DATA[6-7]: Encoder position value (uint16_t type, 14-bit encoder value range 0 to 16383)
        """
        # Convert position to 0.01°/LSB (unit for the command)
        angle_control = int(position * 100)
        max_angle = 360.0  # Maximum angle for single-turn control
        tolerance = 0.5  # Tolerance in degrees for stopping condition

        # Validate inputs
        if not (0 <= position <= max_angle):
            raise ValueError(f"Invalid target position value: {position}. Must be in range [0, {max_angle}]°.")
        if not (0 < speed <= 1000):  # Example: limit speed to 1000 dps for safety
            raise ValueError(f"Invalid speed value: {speed}. Must be in range [1, 1000] dps.")
        if direction not in (0, 1):
            raise ValueError(f"Invalid direction value: {direction}. Must be 0 (CW) or 1 (CCW).")

        # Send the position control command with speed limit
        msg = self.can_bus.sendMessage(
            id=self.BASE_ADDR_ID + self.id,
            data=[
                self.ADDR_WRITE_SINGLETURN_SPEED_DIRECTION_CLOSED_LOOP_CONTROL,
                direction & 0xFF,  # Direction byte
                (speed >> 0) & 0xFF, (speed >> 8) & 0xFF,  # Speed limit
                (angle_control >> 0) & 0xFF, (angle_control >> 8) & 0xFF,  # Position target
                0x00, 0x00
            ]
        )

        # Loop until the motor reaches the target position
        while True:
            motor_angle = self.read_singleturn_encoder_position(debug=True)
            motor_temp, torque_current, motor_speed, encoder_position = self.read_motor_status_2()

            # Handle overflow case for single-turn control
            if abs(motor_angle - position) > max_angle - tolerance:
                if motor_angle > position:
                    motor_angle -= max_angle
                else:
                    motor_angle += max_angle

            # Check if the motor is within the target range and has stopped
            if abs(motor_angle - position) < tolerance and motor_speed == 0.0:
                break

        # Optionally print debug information
        if debug:
            print(f"Motor temperature: {motor_temp}°C")
            print(f"Torque current: {torque_current}A")
            print(f"Motor speed: {motor_speed}dps")
            print(f"Motor angle: {motor_angle}°")

        return motor_temp, torque_current, motor_speed, motor_angle
