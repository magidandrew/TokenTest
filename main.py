import sys
import argparse
import yaml
from Structure.AgentFactory import agentFactory
from pathlib import Path


def parse_config(config_path: Path):
    with open(config_path, 'r') as stream:
        try:
            config_values: dict = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

        # simulation_blocks: int = config_values["num_blocks"]
        periods: int = config_values["periods"]
        window_size: int = config_values["window_size"]
        init_difficulty: float = config_values["init_difficulty"]
        debug: bool = config_values["debug"]
        export_graphs: bool = config_values["export_graphs"]

        sim_agents = []

        for agent in config_values["agents"]:
            # b/c only one agent definition per "agent#" subheading
            agent_class: str = next(iter(config_values["agents"][agent].keys()))
            agent_params = next(iter(config_values["agents"][agent].values()))
            # creating 'n' num of agents
            for _ in range(agent_params["num"]):
                # FIXME: deal with splitting the alpha param for multiple agents
                sim_agents.append(agentFactory(agent_class)(agent_params["alpha"], agent_params["gamma"]))

        total_alpha: float = 0.0
        total_gamma: float = 0.0
        for agent in sim_agents:
            total_alpha += agent.alpha
            total_gamma += agent.gamma

        assert(total_alpha == 1)
        assert(total_gamma == 1)

        return {"periods": periods,
                "window_size": window_size,
                "agents": sim_agents,
                "init_difficulty": init_difficulty,
                "debug": debug,
                "export_graphs": export_graphs
                }


def parse_args() -> Path:
    # FIXME: update program description when close to being finished
    program_description = "Selfish Mining Simulator."
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-c', '--config', required=False, type=str, help="YAML config file as str."
                                                                         "Defaults to \'config.yaml\' if not specified.")
    args = parser.parse_args()

    # default
    config_path: Path = Path("config.yaml")
    # if specified
    if args.config is not None:
        config_path: Path = Path(args.config)

    return config_path


def run():
    config_path: Path = parse_args()
    sim_config: dict = parse_config(config_path)
    print(sim_config)


if __name__ == "__main__":
    run()
