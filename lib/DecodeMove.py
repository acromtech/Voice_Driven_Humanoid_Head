class DecodeMove:
    def __init__(self, answer_move: str, time_step: float = 0.1):
        """
        Initialize the DecodeMove class with the input string answer_move.
        :param answer_move: The symbolic command for movement (e.g., "head_nod").
        :param time_step: The time increment (in seconds) for trajectory calculation.
        """
        self.answer_move = answer_move
        self.time_step = time_step  # Time increment for the trajectory
        self.trajectory = []  # List to store trajectory points (positions, speeds, accelerations)
        self.generate_trajectory()

    def generate_trajectory(self):
        """
        Generate a trajectory for the given movement command.
        Each step is computed based on time_step.
        """
        if self.answer_move == "head_nod":
            # A nod consists of moving the head up and down (pitch axis)
            self.trajectory = [
                {
                    "time": 0,
                    "positions": [0, 0, 0],
                    "speeds": [0, 0, 0],
                    "accelerations": [0, 50, 0],
                },
                {
                    "time": 0.5,
                    "positions": [0, 30, 0],
                    "speeds": [0, 20, 0],
                    "accelerations": [0, 0, 0],
                },
                {
                    "time": 1.0,
                    "positions": [0, 0, 0],
                    "speeds": [0, -20, 0],
                    "accelerations": [0, -50, 0],
                },
            ]
        elif self.answer_move == "head_shake":
            # A shake consists of rotating left and right (yaw axis)
            self.trajectory = [
                {
                    "time": 0,
                    "positions": [0, 0, 0],
                    "speeds": [0, 0, 0],
                    "accelerations": [50, 0, 0],
                },
                {
                    "time": 0.5,
                    "positions": [30, 0, 0],
                    "speeds": [20, 0, 0],
                    "accelerations": [0, 0, 0],
                },
                {
                    "time": 1.0,
                    "positions": [-30, 0, 0],
                    "speeds": [-20, 0, 0],
                    "accelerations": [-50, 0, 0],
                },
                {
                    "time": 1.5,
                    "positions": [0, 0, 0],
                    "speeds": [0, 0, 0],
                    "accelerations": [0, 0, 0],
                },
            ]
        elif self.answer_move == "head_tilt":
            # A tilt consists of tilting the head sideways (roll axis)
            self.trajectory = [
                {
                    "time": 0,
                    "positions": [0, 0, 0],
                    "speeds": [0, 0, 0],
                    "accelerations": [0, 0, 50],
                },
                {
                    "time": 0.5,
                    "positions": [0, 0, 30],
                    "speeds": [0, 0, 20],
                    "accelerations": [0, 0, 0],
                },
                {
                    "time": 1.0,
                    "positions": [0, 0, 0],
                    "speeds": [0, 0, -20],
                    "accelerations": [0, 0, -50],
                },
            ]
        else:
            raise ValueError(f"Unknown movement command: {self.answer_move}")

    def get_trajectory(self):
        """
        Return the trajectory as a list of states at each time step.
        """
        return self.trajectory
