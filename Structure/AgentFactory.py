from Agents.SelfishAgent import SelfishAgent
from Agents.HonestAgent import HonestAgent
from Agents.SmartAgent import SmartAgent


def agentFactory(agent_type: str):
    agents = {"honest": HonestAgent,
              "selfish": SelfishAgent,
              "smart": SmartAgent
              }
    return agents[agent_type]
