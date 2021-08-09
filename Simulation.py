# from Structure.SmartAgent import SmartAgent
from Agents.AbstractAgent import AbstractAgent
from Structure.Blockchain import Blockchain
from Structure.BlocktimeOracle import BlocktimeOracle


class Simulator:
    def __init__(self, **kwargs):
        self.number_of_periods: int = kwargs['number_of_periods']
        self.agents: list[AbstractAgent] = kwargs['agents']

        self.WINDOW_SIZE: int = kwargs['window_size']
        self.TIME_PER_BLOCK: float = kwargs['minetime_per_block']
        self.difficulty: float = kwargs['difficulty']
        self.period_lengths = [0.0 for _ in range(self.number_of_periods)]

        self.blockchain: Blockchain = Blockchain()
        self.blocktime_oracle: BlocktimeOracle = BlocktimeOracle(difficulty=self.difficulty)

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

    @staticmethod
    def explicit_tuple_to_payload(agent: AbstractAgent, pp_size: int) -> dict:
        return {"agent": agent, "pp_size": pp_size}

    @staticmethod
    def tuple_to_payload(input_tuple: tuple[AbstractAgent, int]) -> dict:
        return {"agent": input_tuple[0], "pp_size": input_tuple[1]}

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

                # set internal state for each time-step to 0's
                internal_state = dict.fromkeys(self.agents, 0)
                # this is the honest miner that found one. hard-coding the win before iterating further
                internal_state[payload["agent"]] = 1

                # defected blocks - these will be added to the honest agent wins at the end of the do-while
                defector_blocks: int = 0

                # do-while
                while True:
                    self.transmit_block_to_all_agents(payload)
                    longest_published_chain: list[tuple[AbstractAgent, int]] = self.get_longest_published_chain()

                    # base case
                    # check that all received values are 0; [1] b/c looking at int in tuple[AbstractAgent, int]
                    # TODO: make sure this isn't buggy...
                    INT_POSITION = 1
                    if longest_published_chain == [x for x in longest_published_chain if x[INT_POSITION] == 0]:
                        # return the longest chain(s); will be used to create forks otherwise
                        longest_state_chains: list[tuple[AbstractAgent, int]] = self.get_longest_internal_chain(
                            internal_state)

                        # If the longest chain is unique; no need to fork
                        if len(longest_state_chains) == 1:
                            payload = self.tuple_to_payload(next(iter(longest_state_chains)))

                        # If longest chain not unique, we must fork to establish a winner
                        elif len(longest_state_chains) > 1:
                            winning_chain_agent, winning_agent, min_time = self.blocktime_oracle.fork(self.difficulty,
                                                                                                      self.agents)
                            # winning_agent could be honest(defector), winning_chain_agent is selfish
                            # defectors won. ex: honest win, but selfish-miner keeps his mined block
                            if winning_chain_agent != winning_agent:
                                # winning_chain_agent.defected_blocks += 1
                                defector_blocks += 1

                            # increment internal_state regardless
                            internal_state[winning_chain_agent] += 1

                            # fork will only have one winner, hence the 1
                            payload = self.explicit_tuple_to_payload(winning_chain_agent, 1)

                        # error-handling
                        else:
                            raise (Exception(f"longest_state_chains: {len(longest_state_chains)}. Value"
                                             f"must be greater than 0."))
