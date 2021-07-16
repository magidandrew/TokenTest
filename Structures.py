class Block:
    def __init__(self, mining_time: float = 0, timestamp: float = 0):
        self.mining_time = mining_time
        self.timestamp = timestamp

    def __str__(self):
        return "\n".join(["mining time: {}".format(self.mining_time), "timestamp: {}".format(self.timestamp)])

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []

    def addBlock(self, block: Block):
        self.chain.append(block)

    def pop(self) -> Block:
        return self.chain.pop()

    def removeBlocksFromEnd(self, numBlocks: int) -> None:
        for i in range(numBlocks):
            self.chain.pop()

    def getGlobalTimeOfChain(self) -> float:
        return self.chain[-1].timestamp

    def getBlock(self, index: int) -> Block:
        return self.chain[index]

    def __str__(self):
        output = []
        for i in range(len(self.chain)):
            output.append("Block: {}".format(i))
            output.append("*"*40)
            output.append(self.chain[i].__str__())
        return "\n".join(output)
