import logging
from queue import Queue
from Structures import Block, Blockchain
from utils import get_block_time

### Pseudocode for the simulation class:

valid_chain = Blockchain()
attack_queue = Queue()
gamma = 0.4

# in honest miner agent class
total_mining_time: float = 0


# FIXME: We should be checking if blockchain has had 2016 blocks appended to it before restarting the count from 0
# FIXME: this while loop is incorrect.
while(len(valid_chain) <= 2016):
    h_mine_time = get_block_time(honest_agent)
    s_mine_time = get_block_time(selfish_agent)

    winner = 'H' if h_mine_time < s_mine_time else 'S'

    # TODO: FIGURE OUT A WAY TO CHECK THE QUEUES OF OTHER MINERS
    # TODO: TLDR; WE DON'T ALWAYS HAVE TO GENERATE NEW BLOCK TIMES FOR EVERYONE ON EVERY TIMESTEP
    # TODO: FIGURE OUT HOW TO DO THIS


    if winner == 'H':
        # if selfish miners found no blocks so far.
        if attack_queue.qsize() == 0:
            # append honest block to the blockchain
            new_timestamp = valid_chain.get_global_time_of_chain() + h_mine_time
            valid_chain.add_block(Block(mining_time=h_mine_time, timestamp=new_timestamp))

        # selfish miners and honest miners have matching chain lengths
        # selfish miners fork and pray to Satoshi for a victory
        elif attack_queue.qsize() == 1:
            # Some honest miners will defect. Create these two new mining groups
            defector_agent = Agent(alpha = honest_agent.alpha*gamma) # Effectively (1 - alpha)*gamma
            new_honest_agent = Agent(alpha = honest_agent.alpha*(1-gamma))
            # TODO: COMPUTE MINING TIME FOR ALL 3 AGENTS AND WINNER HAS THE LOWEST
            #
            # Decides who wins the fork contest
            # If selfish miners win,    they keep to themselves
            # If defector miners win,   selfish miners gain +1 block but have to restart mining from scratch
            # If honest miners win,     rip
            results = get_winner(defector_agent, new_honest_agent, selfish_agent)
            if results["selfish"] == True:
                attack_queue.put(results["block"])
            elif results["defector"] == True:
                selfish_agent.blocks_won += 1
            elif results["honest"] == True:
                # empty attack queue
                attack_queue.empty()
            else:
                logging.error("winner at fork not found")
                raise Exception

        # Selfish miner must publish all blocks to ensure victory
        elif attack_queue.qsize() == 2:
            selfish_agent.blocks_won += 2
            valid_chain.add_block()
            valid_chain.add_block()

        # Selfish miner will only match the block posted but will continue mining on their longer chain
        elif attack_queue.qsize() > 2:
            # We just push one block to fork on the valid chain
            attack_queue.get()


            # # We push the TWO earliest blocks in the attack chain to the valid chain.
            # block1 = attack_queue.get()
            # block1.timestamp = valid_chain.get_global_time_of_chain() + h_mine_time
            #
            # block2 = attack_queue.get()
            # block2.timestamp = valid_chain.get_global_time_of_chain() + h_mine_time
            #
            # valid_chain.add_block(block1)
            # valid_chain.add_block(block2)

    # If the selfish miners win
    else:
        attack_queue.put(Block(mining_time=s_mine_time))






