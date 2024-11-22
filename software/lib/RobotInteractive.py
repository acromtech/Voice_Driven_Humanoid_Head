import numpy as np
from scipy.optimize import minimize

class PIDTuner:
    """
    Classe pour ajuster automatiquement les paramètres PID du moteur.
    """
    def __init__(self, motor, setpoint):
        """
        Initialise le tuner PID.

        Parameters:
        - motor: Instance du moteur à régler.
        - setpoint: Position cible (en degrés).
        """
        self.motor = motor
        self.setpoint = setpoint
        self.last_error = 0
        self.integral = 0

    def simulate_pid(self, params):
        """
        Simule le système PID avec les paramètres donnés.

        Parameters:
        - params: Liste des paramètres [Kp_position, Ki_position, Kp_speed, Ki_speed, Kp_torque, Ki_torque].

        Returns:
        - float: Erreur cumulée (fonction de coût).
        """
        position_loop_kp, position_loop_ki, speed_loop_kp, speed_loop_ki, current_loop_kp, current_loop_ki = params

        # Initialiser la simulation
        error_sum = 0
        current_position = self.motor.read_singleturn_encoder_position()

        for t in range(100):  # Simulation sur 100 itérations (ajuster selon le système réel)
            error = self.setpoint - current_position
            self.integral += error
            derivative = error - self.last_error

            # Calcul PID simplifié
            output = (
                position_loop_kp * error +
                position_loop_ki * self.integral +
                speed_loop_kp * derivative
            )
            # Commande du moteur (position simulée)
            self.motor.position_closed_loop_control_4(
                speed=abs(output), direction=0 if output > 0 else 1, position=current_position + output
            )
            current_position = self.motor.read_singleturn_encoder_position()
            error_sum += abs(error)  # Accumuler l'erreur absolue
            self.last_error = error

        return error_sum

    def tune(self):
        """
        Optimise les paramètres PID.

        Returns:
        - list: Meilleurs paramètres PID trouvés.
        """
        initial_guess = [50, 50, 50, 50, 50, 50]  # PID initial
        bounds = [(0, 256), (0, 256), (0, 256), (0, 256), (0, 256), (0, 256)]  # Bornes PID
        result = minimize(
            self.simulate_pid, initial_guess, method="L-BFGS-B", bounds=bounds
        )
        return result.x

# Exemple d'utilisation avec le moteur 3
pid_tuner = PIDTuner(neck.motor_3, setpoint=0)  # Ajuster le setpoint si nécessaire
best_pid_params = pid_tuner.tune()

print("Meilleurs paramètres PID trouvés :")
print(f"Position Kp: {best_pid_params[0]}, Ki: {best_pid_params[1]}")
print(f"Speed Kp: {best_pid_params[2]}, Ki: {best_pid_params[3]}")
print(f"Torque Kp: {best_pid_params[4]}, Ki: {best_pid_params[5]}")

# Appliquer les nouveaux paramètres
neck.initialize_motor(neck.motor_3, tuple(best_pid_params), acceleration=100)