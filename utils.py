import logging
import random
import numpy as np


def get_block_time(alpha: float, difficulty: float, gamma: float = 0, _type: str = 'selfish') -> float:
    """
    _type takes 4 options to get the block mining time taken by:
    'selfish' : selfish miner
    'honest' : honest miner
    'defect' : the proportion of of honest miners who switch
    'honest_fork' : remaining honest miners after defectors leave
    """
    # difficulty cannot be 0
    assert(difficulty != 0)
    # selfish miners cannot have entire hashpower
    assert(alpha != 1)
    # selfish miners cannot have all honest miners mining on their chain
    assert(gamma != 1)

    difficulty_scaling = 10 / difficulty

    if _type == 'selfish':
        return np.random.exponential(1 / alpha * difficulty_scaling)
    elif _type == 'honest':
        return np.random.exponential(1 / (1 - alpha) * difficulty_scaling)
    elif _type == 'defect':
        return np.random.exponential(1 / ((1 - alpha) * gamma) * difficulty_scaling)
    elif _type == 'honest_fork':
        return np.random.exponential(1 / ((1 - alpha)(1 - gamma)) * difficulty_scaling)


# FIXME: CLEAN UP HOW ALL THESE PARAMETERS ARE PASSED IN
def get_winner(alpha: float, gamma: float, difficulty: float, _type: tuple = ('honest', 'selfish')) -> dict:
    results = {'time': None, 'winner': None}
    honest_time = get_block_time(alpha, difficulty, gamma, 'honest')
    attacker_time = get_block_time(alpha, difficulty, gamma, 'selfish')

    # TODO: COMPLEXITY TO MODEL; ACCURACY TO MODEL WHEN BLOCKS ARE MINED AT THE SAME (OR NEAR-SAME) TIME?
    # Attacker won race
    if honest_time > attacker_time:
        results['time'] = attacker_time
        results['winner'] = 'selfish'
    # Honest miner won race
    elif honest_time < attacker_time:
        results['time'] = honest_time
        results['winner'] = 'honest'
    # if equal, pick at random
    else:
        # honest time or attacker_time doesn't matter since they're the same
        results['time'] = attacker_time
        results['winner'] = random.choice(['selfish', 'honest'])
        logging.debug("honest time and attacker_time equivalent")
    return results
