from Structure.AbstractAgent import AbstractAgent
# TODO: import the rest of the agents
from Structure.SelfishAgent import SelfishAgent


class Block:
    def __init__(self, mining_time: float = 0, winning_agent: AbstractAgent = None):
        # time it took to mine the block
        self.mining_time: float = mining_time
        # timestamp is calculated when a block is added to the chain
        self.timestamp: float = 0
        # Agent that won the block
        self.winning_agent: AbstractAgent = winning_agent

    def __str__(self):
        return "\n".join([f"mining time: {self.mining_time}", f"timestamp: {self.timestamp}",
                          f"winning_agent: {self.winning_agent}"])
