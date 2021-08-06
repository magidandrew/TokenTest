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
        self.publish_block = True
        self.broadcast = None
        self.is_forking = True
        self.type = None
        AbstractAgent.counter += 1

    def __str__(self) -> str:
        return_val = [f"alpha: {self.alpha}", f"type: {self.__class__.__name__}"]
        return ", ".join(return_val)

    @abstractmethod
    def get_block_time(self, difficulty: float):
        pass

    @abstractmethod
    def transmit_blocks(self) -> list[Block]:
        pass

    @abstractmethod
    def recieve_blocks(self,*kwargs) -> None:
        pass

    # get_type should only return "selfish", "ism", "honest", etc
    @abstractmethod
    def get_type(self) -> str:
        return self.type

    # @abstractmethod
    # def broadcast(self) -> Block:
    #     pass

    @abstractmethod
    def receive_blocks_from_oracle(self, blocks: list[Block]) -> None:
        for block in blocks:
            self.mining_queue.put(block)

    # FIXME: should some of these methods be defined as __name__ since we are needed names of unique class instances
    # get_id is a unique specifier of the class instance
    @abstractmethod
    def get_id(self) -> str:
        pass

    @abstractmethod
    def transmit_ppsize(self):
        pass

    @abstractmethod
    def length_adjustment(self):
        pass
