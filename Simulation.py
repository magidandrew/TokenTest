# from Structure.SmartAgent import SmartAgent
import Structure.Result
from Agents.AbstractAgent import AbstractAgent
from Structure.Blockchain import Blockchain
from Structure.BlocktimeOracle import BlocktimeOracle
from Structure.Block import Block
import logging as lg


class Simulator:
    def __init__(self, **kwargs):
        self.number_of_periods: int = kwargs['periods']
        self.agents: list[AbstractAgent] = kwargs['agents']

        self.WINDOW_SIZE: int = kwargs['window_size']
        self.TIME_PER_BLOCK: float = kwargs['expected_block_time']
        self.difficulty: float = kwargs['init_difficulty']
        self.period_lengths = [0.0 for _ in range(self.number_of_periods)]

        self.blockchain: Blockchain = Blockchain()
        self.blocktime_oracle: BlocktimeOracle = BlocktimeOracle(agents=self.agents, difficulty=self.difficulty)
        self.orphan_blocks = {_: {"selfish": 0, "honest": 0} for _ in range(self.number_of_periods)}
        self.difficulties: list[float] = []

    # this method sets instructions of what the agent will do when get_longest_published_chain is called
    def transmit_block_to_all_agents(self, payload: dict) -> None:
        for agent in self.agents:
            # do not transmit to the original sender
            if agent != payload["agent"]:
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
        max_len = max(received_blocks, key=lambda x: x[POSITION_OF_LEN])  # len of transmitted blocks is pp_size

        max_blocks = [x for x in received_blocks if x[POSITION_OF_LEN] == max_len[POSITION_OF_LEN]]
        return max_blocks

    def get_longest_internal_chain(self, internal_state: dict) -> list[tuple[AbstractAgent, int]]:
        max_len: int = internal_state[
            max(internal_state, key=lambda x: internal_state[x])]  # len of transmitted blocks is pp_size

        return [(x, internal_state[x]) for x in internal_state if internal_state[x] == max_len]

    @staticmethod
    def explicit_val_to_payload(agent: AbstractAgent, pp_size: int) -> dict:
        return {"agent": agent, "pp_size": pp_size}

    @staticmethod
    def tuple_to_payload(input_tuple: tuple[AbstractAgent, int]) -> dict:
        return {"agent": input_tuple[0], "pp_size": input_tuple[1]}

    def update_difficulty(self, period_index: int) -> None:
        period_time = self.period_lengths[period_index]
        # if period_index > 0:
        #     period_time: float = self.period_lengths[period_index] - self.period_lengths[period_index - 1]

        self.difficulty = self.difficulty * \
                          ((self.WINDOW_SIZE * self.TIME_PER_BLOCK)/period_time)

    # must be run at every period iteration
    def decum_periods(self, period_index: int):
        prev_sum: float = 0.0
        for index in range(period_index):
            prev_sum += self.period_lengths[index]
        if period_index > 0:
            self.period_lengths[period_index] -= prev_sum

    def transmit_difficulty(self):
        for agent in self.agents:
            agent.receive_difficulty(self.difficulty)

    def reset_all_broadcast(self):
        for agent in self.agents:
            agent.reset_broadcast()

    def run(self) -> None:
        # Run this loop for as many periods we want to simulate

        for period_index in range(self.number_of_periods):
            self.period_lengths[period_index] = 0.0

            # Keep looping until the length of the blockchain is equal to the window size.
            while len(self.blockchain) < self.WINDOW_SIZE:

                transmission: Block = self.blocktime_oracle.next_time()
                self.period_lengths[period_index] = transmission.timestamp
                # agent needs to be aware of the block they mined

                lg.debug("winner: " + transmission.winning_agent.__str__())

                transmission.winning_agent.receive_blocks_from_oracle([transmission])

                # if the agent chooses to transmit it publicly to the rest of the miners, we trigger the while loop
                if not transmission.winning_agent.publish_block:
                    continue

                # Make the agents remember the lengths of their private chains before publishing begins
                for agent in self.agents:
                    agent.freeze_lengths()
                    agent.delta = agent.store_length


                # Pops the transmitted block from the mining queue of the agent
                # should always be non_empty
                transmission.winning_agent.mining_queue.get_nowait()

                # Payload variable is passed around between receive and transmit.
                payload = {"agent": transmission.winning_agent, "pp_size": 1}

                # set internal state for each time-step to 0's
                internal_state = dict.fromkeys(self.agents, 0)
                # this is the honest miner that found one. hard-coding the win before iterating further
                internal_state[payload["agent"]] = 1

                # defected blocks - these will be added to the honest agent wins at the end of the do-while
                # FIXME: This only applies to 2-agent cases
                # TODO: Look at internal state and count every entry that is not the max to get the defector blocks
                defector_blocks: int = 0

                # do-while
                while True:
                    self.reset_all_broadcast()
                    # Send all agents the most recent payload
                    self.transmit_block_to_all_agents(payload)

                    # Collect published chains from each agent and select the longest one
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
                            # payload = self.tuple_to_payload(next(iter(longest_state_chains)))
                            # At this point of the code we have the winner.
                            # TODO: Pass in time information of the blocks
                            # FIXME: This renders the blockchain class useless. Restructure
                            winner: list[tuple[AbstractAgent, int]] = self.get_longest_internal_chain(internal_state)
                            # Defector_blocks is zero when the winner is selfish
                            for _ in range(next(iter(winner))[1] - defector_blocks):
                                self.blockchain.add_block(Block(winning_agent=next(iter(winner[0]))))



                            # --------------------------
                            # Extract the honest agent object
                            # FIXME: this is just so so bad
                            other_agent = None
                            for agent in self.agents:
                                if agent != winner[0]:
                                    other_agent = agent
                            assert(other_agent != None)
                            # --------------------------
                            # Only triggered when the winner is selfish
                            for _ in range(defector_blocks):
                                self.blockchain.add_block(Block(winning_agent=other_agent))

                            # Update the period time with the latest block time from the Blocktime Oracle
                            self.period_lengths[period_index] = self.blocktime_oracle.current_time
                            
                            # get orphan blocks by reading internal state of all other agents
                            for agent in self.agents:
                                if agent != next(iter(winner))[0]:
                                    # self.orphan_blocks[period_index][agent.type] += agent.store_length
                                    self.orphan_blocks[period_index][agent.type] += internal_state[agent]
                                    # assert(agent.store_length == internal_state[agent])


                            # Set all agent variables to their default values
                            for agent in self.agents:
                                agent.reset()                                

                            break

                        # If longest chain not unique, we must fork to establish a winner
                        elif len(longest_state_chains) > 1:
                            winning_chain_agent, winning_agent, min_time = self.blocktime_oracle.fork(self.difficulty,
                                                                                                      self.agents)
                            lg.debug("fork winner: " + winning_agent.__str__())
                            # winning_agent could be honest(defector), winning_chain_agent is selfish
                            # defectors won. ex: honest win, but selfish-miner keeps his mined block
                            if winning_chain_agent != winning_agent:
                                # winning_chain_agent.defected_blocks += 1
                                defector_blocks += 1

                            # increment internal_state regardless
                            internal_state[winning_chain_agent] += 1

                            # fork will only have one winner, hence the 1
                            payload = self.explicit_val_to_payload(winning_chain_agent, 1)

                        # error-handling
                        else:
                            raise (Exception(f"longest_state_chains: {len(longest_state_chains)}. Value"
                                             f"must be greater than 0."))

                    # If each entry in the longest chain isn't a pp_size of zero:
                    else:
                        payload = self.tuple_to_payload(next(iter(longest_published_chain)))
                        internal_state[payload["agent"]] += payload["pp_size"]

            self.decum_periods(period_index)
            print(self.period_lengths[period_index])
            self.update_difficulty(period_index)
            self.transmit_difficulty()

            print(str(self.difficulty))
            self.difficulties.append(self.difficulty)

            honest_win: int = 0
            selfish_win: int = 0
            for _ in range(len(self.blockchain)):
                if self.blockchain.pop().winning_agent.type == "selfish":
                    selfish_win += 1
                else:
                    honest_win += 1
            print(f"honest win: {honest_win}")
            print(f"selfish win: {selfish_win}")
            # print(self.blockchain)

            print("______________________")

        for _ in range(self.number_of_periods):
            print("Period " + str(_) + " time: " + str(self.period_lengths[_]))
            print("Orphans " + str(_) + " Selfish: " + str(self.orphan_blocks[_]["selfish"]))
            print("Orphans " + str(_) + " Honest: " + str(self.orphan_blocks[_]["honest"]))

            print("_____________________________________")

        result = Structure.Result.SimResult(periods=self.period_lengths, difficulties=self.difficulties,
                                            agents=self.agents, orphan_blocks=self.orphan_blocks)
