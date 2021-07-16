class Block:
    def __init__(self, mining_time: float = 0):
        self.mining_time: float = mining_time
        # timestamp is calculated when a block is added to the chain
        self.timestamp: float = 0

    def __str__(self):
        return "\n".join(["mining time: {}".format(self.mining_time), "timestamp: {}".format(self.timestamp)])

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []

    def addBlock(self, block: Block):
        if len(self.chain) != 0:
            block.timestamp = self.getGlobalTimeOfChain() + block.mining_time
        # edge case if we are adding genesis block
        else:
            block.timestamp = block.mining_time
        self.chain.append(block)

    def pop(self) -> Block:
        return self.chain.pop()

    def removeBlocksFromEnd(self, numBlocks: int) -> None:
        for i in range(numBlocks):
            self.chain.pop()

    def getGlobalTimeOfChain(self) -> float:
        # check that chain is non-empty
        if len(self.chain) == 0:
            return 0.0
        else:
            return self.chain[-1].timestamp

    def getBlock(self, index: int) -> Block:
        return self.chain[index]

    def __str__(self):
        output = []
        for i in range(len(self.chain)):
            output.append("Block: {}".format(i))
            output.append("*"*40)
            output.append(self.chain[i].__str__())
            output.append("-" * 40)
        return "\n".join(output)
