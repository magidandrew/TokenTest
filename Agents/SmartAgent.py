from Agents.AbstractAgent import AbstractAgent
import numpy as np
from Structure.Block import Block


class SmartAgent(AbstractAgent):

    def __init__(self, alpha: float, gamma: float):
        super().__init__(alpha)
        self.is_mining: bool = True
        self.id = super().counter
        self.type: str = "smart"
        self.publish_block: bool = True
        self.difficulty: float = 1

    def get_block_time(self, difficulty: float, alpha=None) -> float:
        if not alpha:
            alpha = self.alpha
        difficulty_scaling = 10 * difficulty
        return np.random.exponential(1 / alpha * difficulty_scaling)


    # def get_type(self):
    #     return str(self.type) + "_" + str(self.id)

    # def receive_blocks(self, blocks: list[Block]) -> None:
    #     if self.is_mining:
    #         for block in blocks:
    #             self.mining_queue.put(block)

    # def broadcast(self) -> Block:
    #     # if miner is active then it will want to broadcast the block immediately
    #     if self.is_mining:
    #         return self.mining_queue.peek()
    #     # If its not working this will not execute
    #     return None

    # def receive_blocks(self, payload: dict) -> None:
    #     if not self.is_mining:
    #         return
    #
    #     if self.mining_queue.qsize() < payload["pp_size"]:
    #         self.broadcast = (self, 0)
    #         self.mining_queue.empty()
    #     else:
    #         self.broadcast = (self, self.mining_queue.qsize())
    #         self.mining_queue.empty()

    def receive_blocks(self, payload: dict) -> None:
        if not self.is_mining:
            return

        if self.store_length < payload["pp_size"]:
            self.broadcast = (self, 0)
            self.mining_queue.queue.clear()
        else:
            self.broadcast = (self, self.mining_queue.qsize())
            self.mining_queue.queue.clear()




    def receive_blocks_from_oracle(self, blocks: list[Block]) -> None:
        # If agent is active
        if self.is_mining:
            for block in blocks:
                self.mining_queue.put(block)
            self.publish_block = True

    def reset(self):
        self.is_forking = True
        self.publish_block = False
        self.broadcast = None
        self.store_length = 0
        self.mining_queue.queue.clear()

    def receive_difficulty(self, difficulty: float):
        if difficulty > self.difficulty:
            self.is_mining = False
        else:
            self.is_mining = True
        self.difficulty = difficulty




