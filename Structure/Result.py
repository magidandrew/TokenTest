import pickle
from Agents.AbstractAgent import AbstractAgent


class SimResult:
    def __init__(self, periods: list[float], difficulties: list[float], agents: list[AbstractAgent],
                 orphan_blocks: dict):
        # these should be the same length
        assert (len(periods) == len(difficulties) == len(orphan_blocks))

        list_len = len(periods)
        self.frames: dict[(float, float)] = dict.fromkeys([i for i in range(list_len)],
                                                          list(zip(periods, difficulties, orphan_blocks)))
        # self.frames: list[(float, float)] = list(zip(periods, difficulties))
        self.agents: list[AbstractAgent] = agents

        pickle_file = open(f"pickled", "ab")
        pickle.dump(self, pickle_file)
        pickle_file.close()
