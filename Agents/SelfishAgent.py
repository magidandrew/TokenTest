from Agents.AbstractAgent import AbstractAgent
from Structure.Block import Block
import numpy as np


class SelfishAgent(AbstractAgent):
    def __init__(self, alpha: float):
        super().__init__(alpha)
        self.id = super().counter
        self.type = "selfish"

    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / self.alpha * difficulty_scaling)

    def get_type(self):
        return str(self.type) + "_" + str(self.id)

    def broadcast(self) -> Block:
        return None

    def recieve_blocks(self, payload: tuple[AbstractAgent, int]) -> None:
        print("here")
        # if payload[1] > self.mining_queue.qsize():
        #     self.


