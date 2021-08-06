from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Agents.AbstractAgent import AbstractAgent


class Block:
    def __init__(self, mining_timestamp: float = 0, winning_agent: AbstractAgent = None):
        # time it took to mine the block
        # self.mining_time: float = mining_timestamp - timestamp_of_last_block
        # timestamp is calculated when a block is added to the chain
        self.timestamp: float = 0
        # global timestamp at which point a block is expected to be mined at
        self.estimated_timestamp: float =  mining_timestamp
        # Agent that won the block
        self.winning_agent: AbstractAgent = winning_agent

    def __str__(self):
        return "\n".join([f"timestamp: {self.timestamp}",
                          f"winning_agent: {self.winning_agent}"])
