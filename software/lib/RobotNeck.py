import os
import time

from MyActuatorRMD import MyActuatorRMD
from CanBusGsUsb import CanBusGsUsb

class RobotNeck:
    """
    Classe pour contrôler les moteurs du cou d'un robot humanoïde.

    Attributes:
    - motors: Liste des moteurs (instances de MyActuatorRMD).
    - can_bus: Instance du bus CAN.
    """
    def __init__(self, can_bus_channel=0, can_bus_baudrate=1000000):
        """
        Initialise le bus CAN et les moteurs du cou.

        Parameters:
        - can_bus_channel: Canal CAN utilisé.
        - can_bus_baudrate: Baudrate pour le bus CAN.
        """
        self.can_bus = CanBusGsUsb(can_bus_channel, can_bus_baudrate)
        self.can_bus.setup()

        # Initialisation des moteurs (3 moteurs pour le cou)
        self.motors = [
            MyActuatorRMD.L.V1(id=i, reducer_ratio=1, can_bus=self.can_bus)
            for i in range(1, 4)
        ]

    def initialize_motors(self, pid_params, acceleration):
        """
        Configure les moteurs avec les paramètres PID et d'accélération.

        Parameters:
        - pid_params: Tuple des paramètres PID (kp1, ki1, kp2, ki2, kp3, ki3).
        - acceleration: Accélération à configurer pour les moteurs.
        """
        for motor in self.motors:
            # Configurer les paramètres PID
            kp1, ki1, kp2, ki2, kp3, ki3 = motor.write_pid_parameter_to_RAM(
                pid_params[0], pid_params[1], pid_params[2],
                pid_params[3], pid_params[4], pid_params[5]
            )
            if (kp1, ki1, kp2, ki2, kp3, ki3) == pid_params:
                print(f"Motor {motor.id}: PID PARAMETERS OK")
            else:
                print(f"Motor {motor.id}: PID PARAMETERS NOK")

            # Configurer l'accélération
            if motor.write_acceleration_to_RAM(acceleration) == acceleration:
                print(f"Motor {motor.id}: ACCELERATION OK")
            else:
                print(f"Motor {motor.id}: ACCELERATION NOK")

    def perform_movement(self, speed, directions, positions):
        """
        Effectue un mouvement pour les trois moteurs.

        Parameters:
        - speed: Vitesse de rotation (en degrés par seconde).
        - directions: Liste des directions (0 pour horaire, 1 pour antihoraire).
        - positions: Liste des positions cibles (en degrés).
        """
        for motor in self.motors:
            for direction, position in zip(directions, positions):
                motor.position_closed_loop_control_4(speed, direction, position)
                print(f"Motor {motor.id}: moved to {position}° with direction {direction}")

    def shutdown(self):
        """Arrête le bus CAN proprement."""
        self.can_bus.shutdown()
        print("CAN bus shutdown.")

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Création de l'instance du cou
        neck = RobotNeck()

        # Configuration des moteurs
        pid_params = (100, 100, 40, 14, 30, 30)
        acceleration = 200
        neck.initialize_motors(pid_params, acceleration)

        # Effectuer un mouvement spécifique
        speed = 360 * 2
        positions = [90, 0, 270, 0]  # Positions cibles (en degrés)
        directions = [0, 1, 1, 0]    # Directions correspondantes
        neck.perform_movement(speed, directions, positions)

    finally:
        # Arrêter le bus CAN
        neck.shutdown()

