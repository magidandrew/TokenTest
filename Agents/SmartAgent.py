from Agents.AbstractAgent import AbstractAgent
import numpy as np


class SmartAgent(AbstractAgent):

    def __init__(self, alpha: float, is_mining: bool):
        super().__init__(alpha)
        self.is_mining = True
        self.id = super().counter
        self.type = "smart"


    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / (1 - self.alpha) * difficulty_scaling)

    def get_type(self):
        return str(self.type) + "_" + str(self.id)

    def receive_blocks(self, blocks: list[Block]) -> None:
        if self.is_mining:
            for block in blocks:
                self.mining_queue.put(block)

    def broadcast(self) -> Block:
        # if miner is active then it will want to broadcast the block immediately
        if self.is_mining:
            return self.mining_queue.peek()
        # If its not working this will not execute
        return None
