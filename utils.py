import numpy as np

def get_block_time(alpha, difficulty, gamma=0, _type='selfish'):
    '''
    _type takes 4 options to get the block mining time taken by: 
        'selfish' : selfish miner
        'honest' : honest miner
        'defect' : the proportion of of honest miners who switch
        'honest_fork' : remaining honest miners after defectors leave
    '''
    if _type == 'selfish':   
        return np.random.exponential(1/alpha*10/difficulty)
    elif _type == 'honest':
        return np.random.exponential(1/(1- alpha)*10/difficulty)
    elif _type == 'defect':
        return np.random.exponential(1/((1- alpha)*gamma)*10/difficulty)
    elif _type == 'honest_fork':
        return np.random.exponential(1/((1-alpha)(1 - gamma))*10/difficulty)