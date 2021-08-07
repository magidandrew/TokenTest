# from Structure.SmartAgent import SmartAgent
import argparse
import sys
import numpy as np
from queue import Queue
from Structure.Block import Block
from Structure.Blockchain import Blockchain
import utils
from Agents.AbstractAgent import AbstractAgent
from Agents.SelfishAgent import SelfishAgent
from Agents.HonestAgent import HonestAgent
from Agents.SmartAgent import SmartAgent
from Structure.BlocktimeOracle import BlocktimeOracle
import logging


class Simulator:
    def __init__(self, **kwargs):
        self.number_of_periods: int = kwargs['number_of_periods']
        self.agents: list[AbstractAgent] = kwargs['agents']

        self.WINDOW_SIZE: int = kwargs['window_size']
        self.TIME_PER_BLOCK: float = kwargs['minetime_per_block']
        self.difficulty: float = kwargs['difficulty']
        self.period_lengths = [0.0 for i in range(self.number_of_periods)]

        self.blockchain: Blockchain = Blockchain()
        self.blocktime_oracle: BlocktimeOracle = BlocktimeOracle(difficulty=self.difficulty)

    '''
    # pp_size: private progression size
    # TODO: Fork conditions....look at all instruction tuples, and if theres no unique max
    # return val: tuple(agent, pp_size, valid chain length adjustment)
    def receive_from_all_agents(self, transmitted_block: Block) -> tuple[AbstractAgent, int, int]:
        # TODO: compute all instructions and also process forks.
        POSITION_OF_LEN = 1
        POSITION_OF_AGENT = 0
        received_blocks = []

        # only largest pp_size gets accepted
        for agent in self.agents:
            # (agent and transmitted blocks)
            # TODO: transmit actual chain instead of just the size? (to keep timestamps)
            received_blocks.append((agent, agent.transmit_ppsize(), agent.length_adjustment()))

        # find pp_size maxes
        # structure: [ (agent, [block1, block2, ..., block_n], 3), ..., (agent, [block1, block2], 2)]
        max_len = max(received_blocks, key=lambda x: len(x[POSITION_OF_LEN]))  # len of transmitted blocks is pp_size
        max_blocks = [x for x in received_blocks if len(x[POSITION_OF_LEN]) == max_len[POSITION_OF_LEN]]

        # < 1 for completeness
        if len(max_blocks) < 1:
            raise Exception(f"invalid num of blocks ({len(max_blocks)} blocks) received from agents")
        # one winner established
        elif len(max_blocks) == 1:
            self.blockchain.add_block(Block(mining_timestamp=transmitted_block.mining_time,
                                            timestamp_of_last_block=self.blockchain.get_global_time_of_chain(),
                                            winning_agent=max_blocks[0][
                                                POSITION_OF_AGENT]))  # TODO: figure out how this will be passed in
        # here we fork with the winners
        else:
            # TODO: implement this stuff
            pass
    '''

    def transmit_block_to_all_agents(self, payload: dict) -> None:
        for agent in self.agents:
            agent.receive_blocks(payload)

    def get_longest_published_chain(self) -> list[tuple[AbstractAgent, int]]:
        POSITION_OF_LEN = 1
        # we are receiving list[blocks] from each agent
        received_blocks = []

        # only largest pp_size gets accepted
        for agent in self.agents:
            # (agent and transmitted blocks)
            # TODO: transmit actual chain instead of just the size? (to keep timestamps)
            received_blocks.append(agent.broadcast)  # type tuple(AbstractAgent, int)

        # find pp_size maxes
        # structure: [ (agent, int), ... , (agent, int)]
        max_len = max(received_blocks, key=lambda x: len(x[POSITION_OF_LEN]))  # len of transmitted blocks is pp_size

        max_blocks = [x for x in received_blocks if len(x[POSITION_OF_LEN]) == max_len[POSITION_OF_LEN]]
        return max_blocks

    def get_longest_internal_chain(self, internal_state: dict) -> list[tuple[AbstractAgent, int]]:
        max_len: int = internal_state[
            max(internal_state, key=lambda x: internal_state[x])]  # len of transmitted blocks is pp_size

        max_agent_len_tuples = [x for x in internal_state if internal_state[x] == ma]
        return max_blocks

    def tuple_to_payload(self, agent: AbstractAgent, pp_size: int):
        payload = dict()
        payload["agent"] = agent
        payload["pp_size"] = pp_size

        return payload

    def run(self) -> None:
        # Run this loop for as many periods we want to simulate
        for i in range(self.number_of_periods):
            self.period_lengths[i] = 0.0

            # Keep looping until the length of the blockchain is equal to the window size.
            while len(self.blockchain) < self.WINDOW_SIZE:
                transmission = self.blocktime_oracle.next_time()
                self.period_lengths[i] = transmission.mining_time
                # agent needs to be aware of the block they mined
                transmission.winning_agent.receive_blocks_from_oracle([transmission])

                # if the agent chooses to transmit it publicly to the rest of the miners, we trigger the while loop
                if not transmission.winning_agent.publish_block:
                    continue

                transmission.winning_agent.mining_queue.get()

                payload = {"agent": transmission.winning_agent, "pp_size": 1}

                internal_state = dict.fromkeys(self.agents, 0)
                # this is the honest miner that found one. hard-coding the win before iterating further
                internal_state[payload["agent"]] = 1

                # do-while
                while True:
                    self.transmit_block_to_all_agents(payload)
                    longest_published_chain: list[tuple[AbstractAgent, int]] = self.get_longest_published_chain()

                    # base case
                    # check that all are outputs are 0; [1] b/c looking at int in tuple
                    # TODO: make sure this isn't buggy...
                    if longest_published_chain == [x for x in longest_published_chain if x[1] == 0]:
                        # check internal state to see if there should be a fork
                        longest_state_chains: list[tuple[AbstractAgent, int]] = self.get_longest_internal_chain(
                            internal_state)
                        # If the longest chain is unique, so no need to fork
                        if len(longest_state_chains) == 1:
                            # payload["agent"] = longest_state_chains[0][0] #[0]-first and only element in list, [0]-agent
                            # payload["pp_size"] = longest_state_chains[0][1]
                            self.tuple_to_payload(longest_state_chains)
                        # If longest chain not unique, we must fork to establish a winner
                        elif len(longest_state_chains) > 1:
                            winning_chain_agent, winning_agent, min_time = self.blocktime_oracle.fork(self.difficulty,
                                                                                                      self.agents)
                            # defectors won. ex: honest win, but selfish-miner keeps his mined block
                            if winning_chain_agent != winning_agent:
                                winning_chain_agent.defected_blocks += 1
                            # increment internal_state regardless
                            internal_state[winning_chain_agent] += 1

                            # fork will only have one winner, hence the 1
                            payload = self.tuple_to_payload(winning_chain_agent, 1)



                        # error-handling
                        else:
                            raise (Exception(f"longest_state_chains: {len(longest_state_chains)}. Value"
                                             f"must be greater than 0."))

                '''
                # do-while
                while True:
                    blocks_added = 0

                    self.transmit_block_to_all_agents(payload)
                    longest_published_chain = self.get_longest_published_chain()

                    # all found values from agents is 0
                    if len(longest_published_chain) == len(self.agents) and longest_published_chain[0][1] == 0:
                        # This means that the most recent payload was successful
                        # All the blocks in the last payload belong to the agent that pushed that public chain
                        # when no one has any more blocks secretly/publicly
                        for j in range(payload["pp_size"]):
                            self.blockchain.add_block(
                                Block(mining_timestamp=self.period_lengths[j], winning_agent=payload["agent"]))
                            blocks_added += 1
                        # Now break out of the infinite loop
                        break

                    # If the longest published chain/s is equal to the payload pp_size
                    # [0][1] b/c peeking first element (all elements in the list are going to be the same)
                    elif longest_published_chain[0][1] == payload["pp_size"]:
                        agets = [longest_published_chain[0][0], payload["agent"]]
                        winning_block, winning_agent, min_time = self.blocktime_oracle.fork(self.difficulty, agents)

                        payload["agent"] = winning_agent
                        payload["pp_size"] = 1


                        self.blockchain.add_block(
                            Block(mining_timestamp=self.period_lengths[i], winning_agent=winning_block))
                        blocks_added += 1
                        self.period_lengths[i] += min_time

                    # Else the longest published chain is longer, and therefore wins. Design the payload object.
                    else:
                        # FIXME: is this right? and try to avoid magic numbers
                        payload["agent"] = longest_published_chain[0][0]
                        payload["pp_size"] = longest_published_chain[0][1]
                    '''


'''

    def run(self) -> None:
        LEN_POSITION = 1
        while len(self.__blockchain) < self.WINDOW_SIZE:
            winning_agent, mining_time = self.blocktime_oracle.next_time()
            # send/recv for agents - which agent mined a block and will it be released publicly
            self.transmit_block_to_agent(winning_agent, mining_time)
            broadcast = self.receive_broadcast_from_agent()

            if broadcast is None:
                continue

            transmission = Block(mining_timestamp=mining_time, timestamp_of_last_block=self.blockchain.get_global_time_of_chain(), winning_agent=winning_agent)


            while True:
                self.transmit_block_to_all_agents(transmission)
                # payload is a list of tuples of type (agent, num_revealed_blocks)
                payload: list[tuple[AbstractAgent, int]] = self.receive_from_all_agents(transmission)

                # exit condition, all lengths are 0
                # base case
                if max(payload, key=lambda x: x[LEN_POSITION]) == 0:
                    # TODO: Append blocks to blockchain
                    break
                # Only 1 agent has a block
                if is_onehot(payload, key=lambda x: x[LEN_POSITION]) == 1:
                    # TODO: Append blocks to blockchain
                    break

                # Create the block to be transmitted to every agent
                transmission: Block = self.PLACEHOLDER_FOR_EXECUTION(payload)

'''
# send/recv for blockchain
'''
    def run(self) -> None:
        while len(self.blockchain) < self.WINDOW_SIZE:
            winning_agent, mining_time = self.blocktime_oracle.next_time()

            transmission = Block(mining_timestamp=mining_time, timestamp_of_last_block=self.blockchain.get_global_time_of_chain(), winning_agent=winning_agent)
            self.transmit_block_to_all_agents(transmission)

            winning_agent, pp_size, length_adjustment = self.receive_from_all_agents(transmission)

            self.execute_instruction(winning_agent, pp_size, length_adjustment)

            self.reset_agents()
'''

'''
class SelfishMining:
    # TODO: these values can be implemented in an abstract class if it makes sense and is easier
    def __init__(self, **kwargs):
        self.__blocks_in_cur_window = 0

        self.__attack_queue = Queue()
        self.__blockchain = Blockchain()

        self.block_time_oracle = BlocktimeOracle(difficulty=self.__difficulty)

        # Set Parameters
        self.__alpha = kwargs['alpha']
        self.__gamma = kwargs['gamma']

        # For Rewards
        self.__honest_reward = 0
        self.__selfish_reward = 0

        # For difficulty adjustment
        self.__window_size = 2016

        self.__difficulty = 1

    def set_difficulty(self):
        time_taken = self.__blockchain.get_global_time_of_chain()

        if not time_taken:
            self.__difficulty = 1

        else:
            self.__difficulty = self.__difficulty * (time_taken / 20160)

    def simulate(self):

        block_difficulty_periods = [self.__window_size for x in range(0, self.__nb_simulations // self.__window_size)] \
                                   + [self.__nb_simulations % self.__window_size]

        # TODO: HOW ARE WE DETERMINING DIFFICULTY
        difficulty = self.__difficulty
        selfish_agent = SelfishAgent(self.__alpha)
        honest_agent = HonestAgent(1 - self.__alpha)
        smart_agent = SmartAgent(self.__alpha, is_mining=True)

        # TESTING PLAYGROUND
        # for _ in range(75):
        #     print(selfish_agent.get_block_time(difficulty))
        # return
        # END PLAYGROUND

        for window in block_difficulty_periods:

            # Set the difficulty for this period:
            prev_difficulty = self.__difficulty
            self.set_difficulty()

            # Disable smart agent if the difficulty increases
            if prev_difficulty < self.__difficulty:
                smart_agent.is_mining = False

            # Only run till window filled up
            while self.__blocks_in_cur_window < window:
                # ---PSEUDOCODE----
                next_block = self.block_time_oracle.next_time()

                # ---END PSEUDOCODE---

                # Find whether selfish-miner or honest-miner finds block first
            results = utils.get_winner(selfish_agent, honest_agent, gamma=self.__gamma, difficulty=difficulty)

            if results['type'] == 'honest' or results['type'] == 'smart':

                # check if selfish miner has no blocks
                if self.__attack_queue.qsize() == 0:
                    self.__honest_valid_blocks += 1
                    self.__blockchain.add_block(Block(results['time']))
                    # move window over
                    self.__blocks_in_cur_window += 1
                    logging.debug("honest win, selfish 0 blocks")
                    logging.debug(self.__blockchain)

                # selfish miner has 1 block to fork
                elif self.__attack_queue.qsize() == 1:
                    logging.debug("pre-fork blockchain:")
                    logging.debug(self.__blockchain)
                    # perform the fork
                    # TODO: DIFFICULTY MUST BE CHANGED DEPENDING ON WHETHER WE ARE AT 2015 BLOCKS (NEXT BLOCK WOULD
                    # TODO: BE ADJUSTED FOR DIFFICULTY)
                    fork_results = utils.get_winner(alpha=self.__alpha, gamma=self.__gamma, difficulty=difficulty)
                    # winner takes the subsequent block
                    if fork_results['winner'] == 'selfish':
                        logging.debug(f"selfish fork winner-->time: {fork_results['time']}")
                        # add 2: the first is the mined block, the second is the fork win
                        self.__blockchain.add_block(self.__attack_queue.get())
                        self.__selfish_valid_blocks += 2
                    # honest win
                    else:
                        logging.debug(f"honest fork winner-->time: {fork_results['time']}")
                        self.__blockchain.add_block(Block(results['time']))
                        self.__honest_valid_blocks += 2

                        # have honest miner forfeit his block
                        self.__attack_queue.get()

                    # shift this frame over 2 blocks
                    self.__blocks_in_cur_window += 2
                    # FIXME: CONSIDER INCREMENTING BLOCKS IN WINDOW WITH THE ADD_BLOCK() FUNCTION?
                    self.__blockchain.add_block(Block(fork_results['time']))

                    logging.debug("post-fork blockchain:")
                    logging.debug(self.__blockchain)

                # force selfish miner to push all blocks and establish win
                elif self.__attack_queue.qsize() == 2:
                    self.__blocks_in_cur_window += 2
                    for _ in range(2):
                        self.__blockchain.add_block(self.__attack_queue.get())
                    logging.debug("selfish miner added 2 blocks")
                    logging.debug(self.__blockchain)


                # selfish miner publishes only one block and
                else:  # attack_queue.qsize() > 2:
                    pass


            elif results['type'] == 'selfish':
                self.__delta += 1
                self.__attack_queue.put(Block(results['time']))

    print("---<SUMMARY>---")
    print(self.__blockchain)

    # FIXME: Figure out what the selfish miner does when validated blocks exceeds 2016 (does he publish or throw those away?)
    # FIXME: In this case, selfish miner will publish only his first block to potentially win the fork, and has to discard his subsequent blocks in his selfish chain
    # FIXME: since they will no longer be valid (difficulty is encoded into the header)


def main() -> None:
    program_description = "Selfish Mining Simulator"
    implemented_mining_techniques = ["lead-stubborn", "intermittent", "smart"]

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-n', '--num_blocks', required=True, type=int, help="Number of blocks to run the simulation on")
    parser.add_argument('-a', '--alpha', required=True, type=float, help="HashPower of Selfish Miner")
    parser.add_argument('-g', '--gamma', required=True, type=float,
                        help="Percentage of Honest Miners that mine on selfish chain")
    parser.add_argument("-m", "--method", required=True, type=str,
                        help="Type of mining method: ({})".format(", ".join(implemented_mining_techniques)))
    parser.add_argument('-d', action="store_true", help="Display stuff")

    # args = parser.parse_args()
    #
    # if len(sys.argv) == 1:
    #     parser.print_usage()
    a = SelfishMining(**{'nb_simulations': 10, 'alpha': .3, 'gamma': .2})
    a.simulate()
    print("Sim complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
'''
