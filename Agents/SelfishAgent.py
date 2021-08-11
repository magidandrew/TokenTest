from Agents.AbstractAgent import AbstractAgent
from Structure.Block import Block
import numpy as np


class SelfishAgent(AbstractAgent):
    def __init__(self, alpha: float, gamma: float):
        super().__init__(alpha, gamma)
        self.id = super().counter
        self.type = "selfish"
        self.publish_block = False


    def get_block_time(self, difficulty: float, alpha=None) -> float:
        if not alpha:
            alpha = self.alpha
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / alpha * difficulty_scaling)
    # def get_type(self):
    #     return str(self.type) + "_" + str(self.id)

    # def broadcast(self) -> Block:
    #     pass

    def receive_blocks_from_oracle(self, blocks: list[Block]) -> None:
        for block in blocks:
            self.mining_queue.put(block)

        self.publish_block = False



    # def receive_blocks(self, payload: dict) -> None:
    #     if self.mining_queue.qsize() < payload["pp_size"]:
    #         self.broadcast = (self.id, 0)
    #         self.mining_queue.empty()
    #
    #     else:
    #         delta = self.mining_queue.qsize() - payload["pp_size"]
    #
    #         if delta <= 1:
    #             self.broadcast = (self, self.mining_queue.qsize())
    #             self.mining_queue.empty()
    #             self.is_forking = True
    #
    #         else:
    #             self.broadcast = (self, 1)
    #             self.mining_queue.get()
    #             self.is_forking = False

    def receive_blocks(self, payload: dict) -> None:
        if self.store_length < payload["pp_size"]:
            self.broadcast = (self.id, 0)
            self.mining_queue.empty()

        else:
            delta = self.store_length - payload["pp_size"]

            if delta <= 1:
                self.broadcast = (self, self.mining_queue.qsize())
                self.mining_queue.empty()
                self.is_forking = True

            else:
                self.broadcast = (self, 1)
                self.mining_queue.get()
                self.is_forking = False


    def reset(self):
        self.is_forking = False
        self.publish_block = False
        self.broadcast = None
        self.store_length = 0
        self.mining_queue.empty()






