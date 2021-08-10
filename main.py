import sys
import argparse
import yaml

def parse_config():
    with open("config.yaml", 'r') as stream:
        try:
            print(yaml.safe_load(stream))
        except yaml.YAMLError as exc:
            print(exc)

def run():
    program_description = "Selfish Mining Simulator"
    implemented_mining_techniques = ["lead-stubborn", "intermittent", "smart"]

    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-n', '--num_blocks', required=True, type=int, help="Number of blocks to run the simulation on")
    parser.add_argument('-a', '--alpha', required=True, type=float, help="HashPower of Selfish Miner")
    parser.add_argument('-g', '--gamma', required=True, type=float,
                        help="Percentage of Honest Miners that mine on selfish chain")
    parser.add_argument("-m", "--method", required=True, type=str,
                        help="Type of mining method: ({})".format(", ".join(implemented_mining_techniques)))
    parser.add_argument('-d', action="store_true", help="Display stuff")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_usage()

    # call simulator HERE. look at factory pattern, might come in handy for instantiating
    # the miner classes based on cli input


if __name__ == "__main__":
    # run()
    parse_config()
