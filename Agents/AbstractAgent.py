from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Agents.AbstractAgent import AbstractAgent

from abc import ABC, abstractmethod
from queue import Queue
from Structure.Block import Block


class AbstractAgent(ABC):
    counter = 0

    def __init__(self, alpha: float, gamma: float):
        self.alpha = alpha
        self.gamma = gamma
        self.mining_queue = Queue()
        self.is_mining = True
        self.broadcast_queue = Queue()
        self.publish_block = False
        self.broadcast = None
        self.is_forking = True
        self.type = None
        self.store_length = None
        AbstractAgent.counter += 1

    def __str__(self) -> str:
        return_val = [f"alpha: {self.alpha}", f"type: {self.__class__.__name__}"]
        return ", ".join(return_val)

    @abstractmethod
    def get_block_time(self, difficulty: float, alpha: float = None):
        pass



    @abstractmethod
    def receive_blocks(self, *kwargs) -> None:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass


    # @abstractmethod
    # def broadcast(self) -> Block:
    #     pass

    @abstractmethod
    def receive_blocks_from_oracle(self, blocks: list[Block]) -> None:
        for block in blocks:
            self.mining_queue.put(block)

    def freeze_lengths(self):
        self.store_length = self.mining_queue.qsize()

    @abstractmethod
    def recieve_difficulty(self, difficulty: float):
        pass


