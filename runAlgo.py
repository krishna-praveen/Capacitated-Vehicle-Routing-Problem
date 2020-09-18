from nsga_vrp.NSGA2_vrp import *
import argparse

def main():

    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance_name', type=str, default="./data/json/Input_Data.json", required=False,
                        help="Enter the input Json file name")
    parser.add_argument('--popSize', type=int, default=400, required=False,
                        help="Enter the population size")
    parser.add_argument('--crossProb', type=float, default=0.85, required=False,
                        help="Crossover Probability")
    parser.add_argument('--mutProb', type=float, default=0.02, required=False,
                        help="Mutation Probabilty")
    parser.add_argument('--numGen', type=int, default=200, required=False,
                        help="Number of generations to run")


    args = parser.parse_args()

    # Initializing instance
    nsgaObj = nsgaAlgo()

    # Setting internal variables
    nsgaObj.json_instance = load_instance(args.instance_name)
    nsgaObj.pop_size = args.popSize
    nsgaObj.cross_prob = args.crossProb
    nsgaObj.mut_prob = args.mutProb
    nsgaObj.num_gen = args.numGen

    # Running Algorithm
    nsgaObj.runMain()


if __name__ == '__main__':
    main()
