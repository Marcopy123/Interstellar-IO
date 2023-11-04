import numpy as np
class Body:

    def __init__(self, mass: float, pos: np.ndarray[np.float64], vel: np.ndarray[np.float64]) -> None:
        self.mass = mass
        self.pos = pos
        self.vel = vel
        return