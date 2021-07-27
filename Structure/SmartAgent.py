from Structure.AbstractAgent import AbstractAgent
import numpy as np


class SmartAgent(AbstractAgent):

    def __init__(self, alpha: float, is_mining: bool):
        super().__init__(alpha)
        self.is_mining = True
        self.id = super().counter + 1
        self.type = "smart"


    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / (1 - self.alpha) * difficulty_scaling)

    def get_type(self):
        return str(self.type) + "_" + str(self.id)
