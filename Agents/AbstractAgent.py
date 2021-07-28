from abc import ABC, abstractmethod
from queue import Queue
from Structure.Block import Block


class AbstractAgent(ABC):
    counter = 0

    def __init__(self, alpha: float, gamma: float):
        self.alpha = alpha
        self.gamma = gamma
        self.mining_queue = Queue()
        self.tmp_block_storage = []
        AbstractAgent.counter += 1

    @abstractmethod
    def get_block_time(self, difficulty: float):
        pass

    @abstractmethod
    def transmit_blocks(self) -> list[Block]:
        pass

    def receive_blocks(self, blocks: list[Block]) -> None:
        self.tmp_block_storage = blocks

    @abstractmethod
    def get_type(self) -> str:
        pass

    def __str__(self) -> str:
        return_val = [f"alpha: {self.alpha}", f"type: {self.__class__.__name__}"]
        return ", ".join(return_val)
