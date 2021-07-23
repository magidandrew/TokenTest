class Block:
    def __init__(self, mining_time: float = 0):
        self.mining_time: float = mining_time
        # timestamp is calculated when a block is added to the chain
        self.timestamp: float = 0

    def __str__(self):
        return "\n".join(["mining time: {}".format(self.mining_time), "timestamp: {}".format(self.timestamp)])
