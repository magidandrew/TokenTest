from Agents.AbstractAgent import AbstractAgent
from Structure.Block import Block
import numpy as np
import logging as lg


class SelfishAgent(AbstractAgent):
    def __init__(self, alpha: float, gamma: float):
        super().__init__(alpha, gamma)
        self.id = super().counter
        self.type = "selfish"
        self.publish_block = False
        self.broadcast = (self, 0)
        self.delta = 0

    def get_block_time(self, difficulty: float, alpha=None) -> float:
        if not alpha:
            alpha = self.alpha
        #     FIXME: this 10 is a config var 'expected_block_time'
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

    # FIXME: broadcast should be set in another function otherwise the setting and recving is done in one place
    def receive_blocks(self, payload: dict) -> None:
        # if payload["agent"] == self
        #     self.broadcast(self.id, 0)

        #The multi-agent thing
        if self.store_length < payload["pp_size"]:
            self.broadcast = (self, 0)
            self.mining_queue.queue.clear()

        else:
            self.delta -= payload["pp_size"]
            #delta = self.mining_queue.qsize() - payload["pp_size"]

            if self.delta <= 1:
                # publishes entire attack queue
                self.broadcast = (self, self.mining_queue.qsize())
                self.mining_queue.queue.clear()
                self.is_forking = True

            else:
                self.broadcast = (self, 1)
                self.mining_queue.get_nowait()
                self.is_forking = False

    def reset(self):
        self.is_forking = False
        self.publish_block = False
        self.broadcast = (self, 0)
        self.store_length = 0
        self.mining_queue.queue.clear()

    def receive_difficulty(self, difficulty: float):
        pass
