import os
import time

from MyActuatorRMD import MyActuatorRMD
from CanBusGsUsb import CanBusGsUsb

class RobotNeck:
    """
    Classe pour contrôler les moteurs du cou d'un robot humanoïde.

    Attributes:
    - motor_1: Instance du moteur 1.
    - motor_2: Instance du moteur 2.
    - motor_3: Instance du moteur 3.
    - can_bus: Instance du bus CAN.
    - init_pos_1, init_pos_2, init_pos_3: Positions initiales des moteurs.
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
        self.motor_1 = MyActuatorRMD.L.V1(id=1, reducer_ratio=1, can_bus=self.can_bus)
        self.motor_2 = MyActuatorRMD.L.V1(id=2, reducer_ratio=1, can_bus=self.can_bus)
        self.motor_3 = MyActuatorRMD.L.V1(id=3, reducer_ratio=1, can_bus=self.can_bus)

        # Initialisation des positions initiales (offsets)
        self.init_pos_1 = 0
        self.init_pos_2 = 0
        self.init_pos_3 = 0

        input("OK ?")

    def initialize_motor(self, motor, pid_params, acceleration):
        """
        Configure un moteur avec les paramètres PID, d'accélération, et initialise l'offset.

        Parameters:
        - motor: Instance du moteur à configurer.
        - pid_params: Tuple des paramètres PID (kp1, ki1, kp2, ki2, kp3, ki3).
        - acceleration: Accélération à configurer pour le moteur.
        """
        kp1, ki1, kp2, ki2, kp3, ki3 = motor.write_pid_parameter_to_RAM(
            pid_params[0], pid_params[1], pid_params[2],
            pid_params[3], pid_params[4], pid_params[5]
        )
        if (kp1, ki1, kp2, ki2, kp3, ki3) == pid_params:
            print(f"Motor {motor.id}: PID PARAMETERS OK")
        else:
            print(f"Motor {motor.id}: PID PARAMETERS NOK")

        if motor.write_acceleration_to_RAM(acceleration) == acceleration:
            print(f"Motor {motor.id}: ACCELERATION OK")
        else:
            print(f"Motor {motor.id}: ACCELERATION NOK")
        
        # Lecture de la position actuelle et mise à zéro de l'offset
        init_pos = motor.read_singleturn_encoder_position()
        motor.write_encoder_offset(0)
        print(f"Motor {motor.id}: offset set to 0 (initial position was {init_pos})")

        # Sauvegarde de la position initiale
        if motor == self.motor_1:
            self.init_pos_1 = init_pos
        elif motor == self.motor_2:
            self.init_pos_2 = init_pos
        elif motor == self.motor_3:
            self.init_pos_3 = init_pos

        # Activation du moteur à la position initiale
        self.move_motor(motor, 50, 10)
        self.move_motor(motor, 50, 0)

    def move_motor(self, motor, speed, position):
        """
        Effectue un mouvement pour un moteur donné.

        Parameters:
        - motor: Instance du moteur à déplacer.
        - speed: Vitesse de rotation (en degrés par seconde).
        - position: Position cible (en degrés).
        """
        # Ajustement de la position par rapport à la position initiale
        if motor == self.motor_1:
            position += self.init_pos_1
        elif motor == self.motor_2:
            position += self.init_pos_2
        elif motor == self.motor_3:
            position += self.init_pos_3

        # Lecture de la position actuelle
        current_pos = motor.read_singleturn_encoder_position()

        # Calcul de la direction optimale (la plus courte)
        delta_pos = position - current_pos
        if abs(delta_pos) > 180:
            delta_pos = delta_pos - 360 if delta_pos > 0 else delta_pos + 360

        direction = 0 if delta_pos >= 0 else 1
        target_position = current_pos + delta_pos

        # Commande du moteur
        motor.position_closed_loop_control_4(speed, direction, target_position)
        current_pos = motor.read_singleturn_encoder_position()
        print(f"Motor {motor.id}: moved to {target_position}° (current position: {current_pos})")

    def shutdown(self):
        """Arrête le bus CAN proprement."""
        self.can_bus.shutdown()
        print("CAN bus shutdown.")
        
    def detect_oscillations(self, motor, position_history, threshold=2.0):
        """
        Détecte les oscillations basées sur la variation des positions du moteur.

        Parameters:
        - motor: Instance du moteur surveillé.
        - position_history: Liste des positions enregistrées.
        - threshold: Seuil d'amplitude pour considérer un comportement oscillatoire.

        Returns:
        - True si des oscillations sont détectées, False sinon.
        """
        if len(position_history) < 3:
            return False  # Pas assez de données pour détecter les oscillations

        # Calculer les différences successives entre les positions
        diffs = np.diff(position_history)

        # Analyser l'amplitude des variations
        if max(np.abs(diffs)) > threshold:
            print(f"Motor {motor.id}: Oscillations detected (Amplitude: {max(np.abs(diffs))})")
            return True

        return False

    def auto_adjust_pid(self, motor, position_history, threshold=2.0):
        """
        Ajuste dynamiquement les paramètres PID pour prévenir les oscillations.

        Parameters:
        - motor: Instance du moteur surveillé.
        - position_history: Liste des positions enregistrées.
        - threshold: Seuil d'amplitude pour considérer un comportement oscillatoire.
        """
        if self.detect_oscillations(motor, position_history, threshold):
            # Lire les PID actuels
            current_pid = motor.read_pid_parameters()
            kp1, ki1, kp2, ki2, kp3, ki3 = current_pid

            # Réduire le gain P et augmenter le gain D
            kp1 = max(0, kp1 - 5)
            kp3 = min(100, kp3 + 5)

            # Appliquer les nouveaux PID
            motor.write_pid_parameter_to_RAM(kp1, ki1, kp2, ki2, kp3, ki3)
            print(f"Motor {motor.id}: PID adjusted to ({kp1}, {ki1}, {kp2}, {ki2}, {kp3}, {ki3})")

    def monitor_and_adjust(self, motor, duration=5, threshold=2.0):
        """
        Surveille les positions du moteur et ajuste le PID dynamiquement si nécessaire.

        Parameters:
        - motor: Instance du moteur surveillé.
        - duration: Durée de la surveillance (en secondes).
        - threshold: Seuil d'amplitude pour considérer un comportement oscillatoire.
        """
        position_history = []

        start_time = time.time()
        while time.time() - start_time < duration:
            # Lire la position actuelle
            current_pos = motor.read_singleturn_encoder_position()
            position_history.append(current_pos)

            # Garder seulement les 20 dernières positions pour l'analyse
            if len(position_history) > 20:
                position_history.pop(0)

            # Ajuster les PID si nécessaire
            self.auto_adjust_pid(motor, position_history, threshold)

            # Pause pour éviter de surcharger le système
            time.sleep(0.1)

# Exemple d'utilisation
if __name__ == "__main__":
    try:
        # Création de l'instance du cou
        neck = RobotNeck()

        # Configuration des moteurs
        neck.initialize_motor(neck.motor_1, (100, 100, 40, 14, 70, 70), 100)
        neck.initialize_motor(neck.motor_2, (100, 100, 40, 14, 60, 60), 100)
        neck.initialize_motor(neck.motor_3, (50, 50, 40, 14, 30, 30), 100)

        # Contrôle manuel des moteurs
        active_motor = neck.motor_1
        while True:
            print(f"Controlling Motor {active_motor.id}")
            command = input("Enter command (w: +10°, s: -10°, enter: next motor, q: quit): ").strip().lower()

            if command == "w":
                neck.move_motor(active_motor, speed=360, position=10)
            elif command == "s":
                neck.move_motor(active_motor, speed=360, position=-10)
            elif command == "":
                if active_motor == neck.motor_1:
                    active_motor = neck.motor_2
                elif active_motor == neck.motor_2:
                    active_motor = neck.motor_3
                else:
                    break
            elif command == "q":
                break
            else:
                print("Invalid command.")
            neck.monitor_and_adjust(active_motor, duration=5, threshold=1.5)
    finally:
        neck.shutdown()
