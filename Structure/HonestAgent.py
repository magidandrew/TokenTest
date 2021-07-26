from Structure.AbstractAgent import AbstractAgent
import numpy as np


class HonestAgent(AbstractAgent):
    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / (1 - self.alpha) * difficulty_scaling)
