import pickle
from Agents.AbstractAgent import AbstractAgent


class SimResult:
    def __init__(self, periods: list[float], difficulties: list[float], agents: list[AbstractAgent],
                 orphan_blocks: dict):
        # these should be the same length
        assert (len(periods) == len(difficulties) == len(orphan_blocks))

        list_len = len(periods)
        self.frames = dict(zip([i for i in range(list_len)],
                                                          list(zip(periods, difficulties, orphan_blocks.values()))))
        # self.frames: list[(float, float)] = list(zip(periods, difficulties))
        self.agents: list[AbstractAgent] = agents


        pickle_file = open(f"results", "ab")
        pickle.dump(self.frames, pickle_file)
        pickle_file.close()
        print(f"🥒 Pickled results saved to: \'{pickle_file.name}\'")

