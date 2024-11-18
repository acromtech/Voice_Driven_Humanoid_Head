"""
Class representing MyActuatorRMD equipment, which includes various actuators.

Dependencies:
- Real: Module containing protocols for different actuator series.
  Install dependencies as per the respective protocol requirements.

Usage:
1. Import the required protocol modules from the Real package.
2. Create instances of different actuator series, such as X or L, by providing the necessary parameters.
3. Access specific functionality or properties of each actuator series as needed.
"""

# Import the required protocol modules from the Real package
from ProtocolV1 import ProtocolV1
from ProtocolV2 import ProtocolV2
from ProtocolV3 import ProtocolV3

class MyActuatorRMD:
    class X:
        """
        Class representing the RMD-X series.
        """
        class V2(ProtocolV2):
            """
            Class representing the RMD-X-V2 actuators.
            """
            def __init__(self, id: int, reducer_ratio: int, can_bus):
                """
                Initialize the RMD-X-V2 actuator with the given parameters.

                Parameters:
                    id (int): Identifier for the actuator.
                    reducer_ratio (int): Reducer ratio for the actuator.
                    can_bus: CAN bus instance for communication.
                """
                self.id = id
                self.reducer_ratio = reducer_ratio
                self.can_bus = can_bus
                
                super().__init__(id, reducer_ratio, can_bus)
        class V3(ProtocolV3):
            """
            Class representing the RMD-X-V3 actuators.
            """
            def __init__(self, id=None, reducer_ratio=None, 
                         peak_torque=None, rated_speed=None,
                         can_bus=None):
                """
                Initialize the RMD-X-V3 actuator with the given parameters.

                Parameters:
                    id (int): Identifier for the actuator.
                    reducer_ratio (int): Reducer ratio for the actuator.
                    can_bus: CAN bus instance for communication.
                """
                self.id = id
                self.reducer_ratio = reducer_ratio
                self.peak_torque = peak_torque
                self.rated_speed = rated_speed 
                self.can_bus = can_bus
                super().__init__(id, reducer_ratio, can_bus)
            
            def get_rated_speed(self):
                return self.rated_speed
    class L:
        """
        Class representing the RMD-L series.
        """
        class V1(ProtocolV1):
            """
            Class representing the RMD-L-V1 actuators.
            """
            def __init__(self, id: int, reducer_ratio: int, can_bus):
                """
                Initialize the RMD-L-V1 actuator with the given parameters.

                Parameters:
                    id (int): Identifier for the actuator.
                    reducer_ratio (int): Reducer ratio for the actuator.
                    can_bus: CAN bus instance for communication.
                """
                super().__init__(id, reducer_ratio, can_bus)
        class V2(ProtocolV2):
            """
            Class representing the RMD-L-V2 actuators.
            """
            def __init__(self, id: int, reducer_ratio: int, can_bus):
                """
                Initialize the RMD-L-V2 actuator with the given parameters.

                Parameters:
                    id (int): Identifier for the actuator.
                    reducer_ratio (int): Reducer ratio for the actuator.
                    can_bus: CAN bus instance for communication.
                """
                super().__init__(id, reducer_ratio, can_bus)
