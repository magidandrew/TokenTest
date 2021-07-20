from queue import Queue
from Structures import Block, Blockchain
from utils import get_block_time




### Pseudocode for the simulation class:

valid_chain = Blockchain()
attack_queue = Queue()
gamma = 0.4

# in honest miner agent class
total_mining_time: float = 0



# TODO: edge cases at end of difficulty period (2015ish)
while(len(valid_chain) <= 2016):
    h_mine_time = get_block_time(honest_agent)
    s_mine_time = get_block_time(selfish_agent)

    winner = 'H' if h_mine_time < s_mine_time else 'S'

    if winner == 'H':
        # check len of attack_queue
        if attack_queue.qsize() == 0:
            valid_chain.add_block(Block(mining_time=h_mine_time))

        elif attack_queue.qsize() == 1:
            defector_agent = Agent(alpha = honest_agent.alpha*gamma) # Effectively (1 - alpha)*gamma
            new_honest_agent = Agent(alpha = honest_agent.alpha*(1-gamma))
            # TODO: COMPUTE MINING TIME FOR ALL 3 AGENTS AND WINNER HAS THE LOWEST
            # Decide who wins the fork contest and everyone switches mining on that block once its discovered
            results = get_winner(defector_agent, new_honest_agent, selfish_agent)
            valid_chain.add_block(results['block'])
            # remove entry from queue
            attack_queue.get()

        elif attack_queue.qsize() > 1:
            # with lead stubborn mining, we only push enough blocks to maintain a lead over the honest chain
            # this means either a two block addition or a one block addition

            # delta is attacker_queue.qsize() - valid_chain_from_branch.size()




