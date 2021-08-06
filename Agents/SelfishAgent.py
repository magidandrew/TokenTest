from Agents.AbstractAgent import AbstractAgent
from Structure.Block import Block
import numpy as np


class SelfishAgent(AbstractAgent):
    def __init__(self, alpha: float):
        super().__init__(alpha)
        self.id = super().counter
        self.type = "selfish"
        self.publish_block = False

    def get_block_time(self, difficulty: float) -> float:
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / self.alpha * difficulty_scaling)

    # def get_type(self):
    #     return str(self.type) + "_" + str(self.id)

    # def broadcast(self) -> Block:
    #     pass



    def receive_blocks(self, payload: dict) -> None:
        if self.mining_queue.qsize() < payload["pp_size"]:
            self.broadcast = (self.id, 0)
            self.mining_queue.empty()

        else:
            delta = self.mining_queue.qsize() - payload["pp_size"]

            if delta <= 1:
                self.broadcast = (self, self.mining_queue.qsize())
                self.mining_queue.empty()

            else:
                self.broadcast = (self, 1)
                self.mining_queue.get()
                self.is_forking = False






