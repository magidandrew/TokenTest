from Agents.AbstractAgent import AbstractAgent
import numpy as np


class HonestAgent(AbstractAgent):

    def __init__(self, alpha: float):
        super().__init__(alpha)
        self.id = super().counter + 1
        self.type = "honest"

    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / (self.alpha) * difficulty_scaling)

    def get_type(self):
        return str(self.type) + "_" + str(self.id)
