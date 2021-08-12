from Structure.Block import Block


class Blockchain:
    def __init__(self):
        self.chain: list[Block] = []

    # def add_block(self, block: Block):
    #     if len(self.chain) != 0:
    #         block.timestamp = self.get_global_time_of_chain() + block.mining_time
    #     # edge case if we are adding genesis block
    #     else:
    #         block.timestamp = block.mining_time
    #     self.chain.append(block)

    def add_block(self, block: Block):
        self.chain.append(block)

    def pop(self) -> Block:
        return self.chain.pop()

    def remove_blocks_from_end(self, num_blocks: int) -> None:
        for i in range(num_blocks):
            self.chain.pop()

    def get_global_time_of_chain(self) -> float:
        # check that chain is non-empty
        if len(self.chain) == 0:
            return 0.0
        else:
            return self.chain[-1].timestamp

    def get_block_at_index(self, index: int) -> Block:
        return self.chain[index]

    def __len__(self):
        return len(self.chain)

    def __str__(self):
        # FIXME: DEPENDS ON NUMBER OF PARAMETERS IN A BLOCK!
        # FIXME: THIS IS SO MESSY....NEEDS TO BE CLEANED UP
        block_num_arr = []
        star_arr = []
        mining_time_param_arr = []
        timestamp_param_arr = []
        winning_agent_param_arr = []
        dashes_arr = []
        for i in range(len(self.chain)):
            block_num_arr.append("Block: {}".format(i+1).ljust(40))
            star_arr.append("*" * 40)
            # magic index numbers should be removed
            mining_time_param_arr.append(self.chain[i].__str__().split('\n')[0].ljust(40))
            timestamp_param_arr.append(self.chain[i].__str__().split('\n')[1].ljust(40))
            winning_agent_param_arr.append(self.chain[i].__str__().split('\n')[2].ljust(40))
            dashes_arr.append("-" * 40)

        lines = [" ".join(block_num_arr), " ".join(star_arr), " ".join(mining_time_param_arr),
                 " ".join(timestamp_param_arr), " ".join(winning_agent_param_arr), " ".join(dashes_arr)]

        final_str = ""
        for line in lines:
            final_str += (line + '\n')
        return final_str

