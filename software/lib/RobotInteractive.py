import keyboard
import time
from RobotNeck import RobotNeck

class RobotNeckInteractive(RobotNeck):
    """
    Extension de la classe RobotNeck pour un contrôle interactif via le clavier.
    """

    def interactive_control(self):
        """
        Permet de contrôler les moteurs avec les touches du clavier :
        - Flèche haut : +10° sur la position actuelle.
        - Flèche bas : -10° sur la position actuelle.
        - Entrée : Passer au moteur suivant.
        """
        motor_index = 0
        while motor_index < len(self.motors):
            motor = self.motors[motor_index]
            print(f"Controlling Motor {motor.id} (Index {motor_index + 1}/{len(self.motors)})")
            
            current_position = motor.read_singleturn_encoder_position()
            print(f"Current position: {current_position}°")
            print(f"Offset: {motor.write_encoder_offset(int(current_position))}")

            while True:
                if keyboard.is_pressed("up"):
                    current_position += 10
                    motor.position_closed_loop_control_4(360, 0, current_position)
                    print(f"Motor {motor.id}: moved to {current_position}°")
                    time.sleep(0.3)  # Pour éviter les répétitions rapides

                elif keyboard.is_pressed("down"):
                    current_position -= 10
                    motor.position_closed_loop_control_4(360, 1, current_position)
                    print(f"Motor {motor.id}: moved to {current_position}°")
                    time.sleep(0.3)

                elif keyboard.is_pressed("enter"):
                    print(f"Finished controlling Motor {motor.id}")
                    time.sleep(0.5)  # Petit délai pour éviter un double appui
                    break

            motor_index += 1

        print("All motors have been controlled. Exiting.")

if __name__ == "__main__":
    try:
        # Création de l'instance du cou interactif
        neck = RobotNeckInteractive()

        # Configuration des moteurs
        pid_params = (100, 100, 40, 14, 30, 30)
        acceleration = 200
        neck.initialize_motors(pid_params, acceleration)

        # Contrôle interactif
        neck.interactive_control()

    finally:
        # Arrêter le bus CAN
        neck.shutdown()

