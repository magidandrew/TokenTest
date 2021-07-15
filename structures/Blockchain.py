from structures import Block

class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []

    def addBlock(self, block: Block):
        self.chain.append(block)

    def getGlobalTime(self) -> int:
        return self.chain[-1].timestamp
