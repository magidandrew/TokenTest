from Agents.AbstractAgent import AbstractAgent
from Structure.Block import Block
import numpy as np


class HonestAgent(AbstractAgent):

    def __init__(self, alpha: float, gamma: float):
        super().__init__(alpha, gamma)
        self.id = super().counter
        self.type = "honest"

    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / self.alpha * difficulty_scaling)

    # def get_type(self):
    #     return str(self.type) + "_" + str(self.id)

    def broadcast(self) -> Block:
        return self.mining_queue.peek()

    def transmit_blocks(self) -> list[Block]:
        pass

    def recieve_blocks(self, *kwargs) -> None:
        pass

    def get_type(self) -> str:
        pass

    def get_id(self) -> str:
        pass

    def transmit_ppsize(self):
        pass

    def length_adjustment(self):
        pass

    # def recieve_blocks(self, payload: tuple[AbstractAgent, int]) -> None:
    #     pass






