from Agents.AbstractAgent import AbstractAgent
from Structure.Block import Block
import numpy as np


class HonestAgent(AbstractAgent):

    def __init__(self, alpha: float, gamma: float):
        super().__init__(alpha, gamma)
        self.id = super().counter
        self.type = "honest"
        self.broadcast = (self.id, 0)
        self.is_forking = True

    def get_block_time(self, difficulty: float, alpha=None) -> float:
        if not alpha:
            alpha = self.alpha
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / alpha * difficulty_scaling)

    # def get_type(self):
    #     return str(self.type) + "_" + str(self.id)

    # def broadcast(self) -> Block:
    #     return self.mining_queue.peek()



    def receive_blocks_from_oracle(self, blocks: list[Block]) -> None:
        for block in blocks:
            self.mining_queue.put(block)

        self.publish_block = True

    # def receive_blocks(self, payload: dict) -> None:
    #     if self.mining_queue.qsize() < payload["pp_size"]:
    #         self.broadcast = (self, 0)
    #         self.mining_queue.empty()
    #     else:
    #         self.broadcast = (self, self.mining_queue.qsize())
    #         self.mining_queue.empty()

    def receive_blocks(self, payload: dict) -> None:
        if self.store_length < payload["pp_size"]:
            self.broadcast = (self, 0)
            self.mining_queue.queue.clear()
        else:
            self.broadcast = (self, self.mining_queue.qsize())
            # honest miner will have empty queue after broadcasting
            # assert(self.mining_queue.qsize() == 0)
            self.mining_queue.queue.clear()

    def reset(self):
        self.is_mining = True
        self.is_forking = True
        self.publish_block = False
        self.broadcast = (self.id, 0)
        self.store_length = 0
        self.mining_queue.queue.clear()

    def receive_difficulty(self, difficulty: float):
        pass









