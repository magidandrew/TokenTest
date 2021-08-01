from Agents.AbstractAgent import AbstractAgent
# TODO: import the rest of the agents
from Agents.SelfishAgent import SelfishAgent


class Block:
    def __init__(self, timestamp_of_last_block: float, mining_timestamp: float = 0, winning_agent: AbstractAgent = None):
        # time it took to mine the block
        self.mining_time: float = mining_timestamp - timestamp_of_last_block
        # timestamp is calculated when a block is added to the chain
        self.timestamp: float = 0
        # global timestamp at which point a block is expected to be mined at
        self.estimated_timestamp: float =  mining_timestamp
        # Agent that won the block
        self.winning_agent: AbstractAgent = winning_agent

    def __str__(self):
        return "\n".join([f"mining time: {self.mining_time}", f"timestamp: {self.timestamp}",
                          f"winning_agent: {self.winning_agent}"])
