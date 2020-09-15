
import os
import io
import random
import numpy
import fnmatch
import csv

from csv import DictWriter
from json import load, dump
from deap import base, creator, tools, algorithms, benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume


BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))



# Load the given problem, which can be a json file
def load_instance(json_file):
    """
    Inputs: path to json file
    Outputs: json file object if it exists, or else returns NoneType
    """
    if os.path.exists(path=json_file):
        with io.open(json_file, 'rt', newline='') as file_object:
            return load(file_object)
    return None


# Take a route of given length, divide it into subroute where each subroute is assigned to vehicle
def routeToSubroute(individual, instance):
    """
    Inputs: Sequence of customers that a route has
            Loaded instance problem
    Outputs: Route that is divided in to subroutes
             which is assigned to each vechicle.
    """
    route = []
    sub_route = []
    vehicle_load = 0
    last_customer_id = 0
    vehicle_capacity = instance['vehicle_capacity']
    
    for customer_id in individual:
        # print(customer_id)
        demand = instance[f"customer_{customer_id}"]["demand"]
        # print(f"The demand for customer_{customer_id}  is {demand}")
        updated_vehicle_load = vehicle_load + demand

        if(updated_vehicle_load <= vehicle_capacity):
            sub_route.append(customer_id)
            vehicle_load = updated_vehicle_load
        else:
            route.append(sub_route)
            sub_route = [customer_id]
            vehicle_load = demand
        
        last_customer_id = customer_id

    if sub_route != []:
        route.append(sub_route)

    # Returning the final route with each list inside for a vehicle
    return route


def printRoute(route, merge=False):
    route_str = '0'
    sub_route_count = 0
    for sub_route in route:
        sub_route_count += 1
        sub_route_str = '0'
        for customer_id in sub_route:
            sub_route_str = f'{sub_route_str} - {customer_id}'
            route_str = f'{route_str} - {customer_id}'
        sub_route_str = f'{sub_route_str} - 0'
        if not merge:
            print(f'  Vehicle {sub_route_count}\'s route: {sub_route_str}')
        route_str = f'{route_str} - 0'
    if merge:
        print(route_str)


# Calculate the number of vehicles required, given a route
def getNumVehiclesRequired(individual, instance):
    """
    Inputs: Individual route
            Json file object loaded instance
    Outputs: Number of vechiles according to the given problem and the route
    """
    # Get the route with subroutes divided according to demand
    updated_route = routeToSubroute(individual, instance)
    num_of_vehicles = len(updated_route)
    return num_of_vehicles


# Given a route, give its total cost
def getRouteCost(individual, instance, unit_cost=1):
    """
    Inputs : 
        - Individual route
        - Problem instance, json file that is loaded
        - Unit cost for the route (can be petrol etc)

    Outputs:
        - Total cost for the route taken by all the vehicles
    """
    total_cost = 0
    updated_route = routeToSubroute(individual, instance)

    for sub_route in updated_route:
        # Initializing the subroute distance to 0
        sub_route_distance = 0
        # Initializing customer id for depot as 0
        last_customer_id = 0

        for customer_id in sub_route:
            # Distance from the last customer id to next one in the given subroute
            distance = instance["distance_matrix"][last_customer_id][customer_id]
            sub_route_distance += distance
            # Update last_customer_id to the new one
            last_customer_id = customer_id
        
        # After adding distances in subroute, adding the route cost from last customer to depot
        # that is 0
        sub_route_distance = sub_route_distance + instance["distance_matrix"][last_customer_id][0]

        # Cost for this particular sub route
        sub_route_transport_cost = unit_cost*sub_route_distance

        # Adding this to total cost
        total_cost = total_cost + sub_route_transport_cost
    
    return total_cost


# Get the fitness of a given route
def eval_indvidual_fitness(individual, instance, unit_cost):
    """
    Inputs: individual route as a sequence
            Json object that is loaded as file object
            unit_cost for the distance 
    Outputs: Returns a tuple of (Number of vechicles, Route cost from all the vechicles)
    """

    # we have to minimize number of vehicles
    # TO calculate req vechicles for given route
    vehicles = getNumVehiclesRequired(individual, instance)

    # we also have to minimize route cost for all the vehicles
    route_cost = getRouteCost(individual, instance, unit_cost)

    return (vehicles, route_cost)



def testcosts():
    # Sample instance
    test_instance = load_instance('./data/json/Input_Data.json')

    # Sample individual
    sample_individual = [19, 5, 24, 7, 16, 23, 22, 2, 12, 8, 20, 25, 21, 18,11,15, 1, 14, 17, 6, 4, 13, 10, 3, 9]

    # Sample individual 2
    sample_ind_2 = random.sample(sample_individual, len(sample_individual))
    print(f"Sample individual is {sample_individual}")
    print(f"Sample individual 2 is {sample_ind_2}")

    # Cost for each route
    print(f"Sample individual cost is {getRouteCost(sample_individual, test_instance, 1)}")
    print(f"Sample individual 2 cost is {getRouteCost(sample_ind_2, test_instance, 1)}")

    # Fitness for each route
    print(f"Sample individual fitness is {eval_indvidual_fitness(sample_individual, test_instance, 1)}")
    print(f"Sample individual 2 fitness is {eval_indvidual_fitness(sample_ind_2, test_instance, 1)}")

# testcosts()

def testroutes():
    # Sample instance
    test_instance = load_instance('./data/json/Input_Data.json')

    # Sample individual
    sample_individual = [19, 5, 24, 7, 16, 23, 22, 2, 12, 8, 20, 25, 21, 18,11,15, 1, 14, 17, 6, 4, 13, 10, 3, 9]
    best_ind_300_gen = [16, 14, 12, 10, 15, 17, 21, 23, 11, 9, 8, 20, 18, 19, 13, 22, 25, 24, 5, 3, 4, 6, 7, 1, 2]


    # Sample individual 2
    sample_ind_2 = random.sample(sample_individual, len(sample_individual))
    print(f"Sample individual is {sample_individual}")
    print(f"Sample individual 2 is {sample_ind_2}")
    print(f"Best individual 300 generations is {best_ind_300_gen}")

    # Getting routes
    print(f"Subroutes for first sample individual is {routeToSubroute(sample_individual, test_instance)}")
    print(f"Subroutes for second sample indivudal is {routeToSubroute(sample_ind_2, test_instance)}")
    print(f"Subroutes for best sample indivudal is {routeToSubroute(best_ind_300_gen, test_instance)}")

    # Getting num of vehicles
    print(f"Vehicles for sample individual {getNumVehiclesRequired(sample_individual, test_instance)}")
    print(f"Vehicles for second sample individual {getNumVehiclesRequired(sample_ind_2, test_instance)}")
    print(f"Vehicles for best sample individual {getNumVehiclesRequired(best_ind_300_gen, test_instance)}")

# testroutes()


# Crossover method with ordering
# This method will let us escape illegal routes with multiple occurences
#   of customers that might happen. We would never get illegal individual from this
#   crossOver
def cxOrderedVrp(input_ind1, input_ind2):
    # Modifying this to suit our needs
    #  If the sequence does not contain 0, this throws error
    #  So we will modify inputs here itself and then 
    #       modify the outputs too

    ind1 = [x-1 for x in input_ind1]
    ind2 = [x-1 for x in input_ind2]
    size = min(len(ind1), len(ind2))
    a, b = random.sample(range(size), 2)
    if a > b:
        a, b = b, a

    # print(f"The cutting points are {a} and {b}")
    holes1, holes2 = [True] * size, [True] * size
    for i in range(size):
        if i < a or i > b:
            holes1[ind2[i]] = False
            holes2[ind1[i]] = False

    # We must keep the original values somewhere before scrambling everything
    temp1, temp2 = ind1, ind2
    k1, k2 = b + 1, b + 1
    for i in range(size):
        if not holes1[temp1[(i + b + 1) % size]]:
            ind1[k1 % size] = temp1[(i + b + 1) % size]
            k1 += 1

        if not holes2[temp2[(i + b + 1) % size]]:
            ind2[k2 % size] = temp2[(i + b + 1) % size]
            k2 += 1

    # Swap the content between a and b (included)
    for i in range(a, b + 1):
        ind1[i], ind2[i] = ind2[i], ind1[i]

    # Finally adding 1 again to reclaim original input
    ind1 = [x+1 for x in ind1]
    ind2 = [x+1 for x in ind2]
    return ind1, ind2


def testcrossover():
    ind1 = [3,2,5,1,6,9,8,7,4]
    ind2 = [7,3,6,1,9,2,4,5,8]
    anotherind1 = [16, 14, 12, 7, 4, 2, 1, 13, 15, 8, 9, 6, 3, 5, 17, 18, 19, 11, 10, 21, 22, 23, 25, 24, 20]
    anotherind2 = [21, 22, 23, 25,16, 14, 12, 7, 4, 2, 1, 13, 15, 8, 9, 6, 3, 5, 17, 18, 19, 11, 10, 24, 20]


    newind7, newind8 = cxOrderedVrp(ind1, ind2)
    newind9, newind10 = cxOrderedVrp(anotherind1, anotherind2)

    print(f"InpInd1 is {ind1}")
    print(f"InpInd2 is {ind2}")
    # print(f"New_ind is {[x-1 for x in ind1]}")
    print(f"newind7 is {newind7}")
    print(f"newind8 is {newind8}")
    print(f"newind9 is {newind9}")
    print(f"newind10 is {newind10}")


testcrossover()


def mutationShuffle(individual, indpb):
    """
    Inputs : Individual route
             Probability of mutation betwen (0,1)
    Outputs : Mutated individual according to the probability
    """
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            swap_indx = random.randint(0, size - 2)
            if swap_indx >= i:
                swap_indx += 1
            individual[i], individual[swap_indx] = \
                individual[swap_indx], individual[i]

    return individual,

def testmutation():
    ind1 = [3,2,5,1,6,9,8,7,4]
    mut1 = mutationShuffle(ind1)

    print(f"Given individual is {ind1}")
    print(f"Mutation from first method {mut1}")


# testmutation()

## Statistics and Logging

def createStatsObjs():
    # Method to create stats and logbook objects
    """
    Inputs : None
    Outputs : tuple of logbook and stats objects.
    """
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("std", numpy.std, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)

    # Methods for logging
    logbook = tools.Logbook()
    logbook.header = "Generation", "evals", "avg", "std", "min", "max", "best_one", "fitness_best_one"
    return logbook, stats


def recordStat(invalid_ind, logbook, pop, stats, gen):
    """
    Inputs : invalid_ind - Number of children for which fitness is calculated
             logbook - Logbook object that logs data
             pop - population
             stats - stats object that compiles statistics
    Outputs: None, prints the logs
    """
    record = stats.compile(pop)
    best_individual = tools.selBest(pop, 1)[0]
    record["best_one"] = best_individual
    record["fitness_best_one"] = best_individual.fitness
    logbook.record(Generation=gen, evals=len(invalid_ind), **record)
    print(logbook.stream)


## Exporting CSV files
def exportCsv(csv_file_name, logbook):
    csv_columns = logbook[0].keys()
    csv_path = os.path.join(BASE_DIR, "results", csv_file_name)
    try:
        with open(csv_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in logbook:
                writer.writerow(data)
    except IOError:
        print("I/O error")






def nsga2vrp():

    # Loading the instance
    json_instance = load_instance('./data/json/Input_Data.json')
    
    # Getting number of customers to get individual size
    ind_size = json_instance['Number_of_customers']

    # Setting variables
    pop_size = 400
    # Crossover probability
    cross_prob = 0.2
    # Mutation probability
    mut_prob = 0.02
    # Number of generations to run
    num_gen = 220

    # Developing Deap algorithm from base problem    
    creator.create('FitnessMin', base.Fitness, weights=(-1.0, -1.0))
    creator.create('Individual', list, fitness=creator.FitnessMin)

    # Registering toolbox
    toolbox = base.Toolbox()
    toolbox.register('indexes', random.sample, range(1,ind_size+1), ind_size)

    # Creating individual and population from that each individual
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    
    # Creating evaluate function using our custom fitness
    #   toolbox.register is partial, *args and **kwargs can be given here
    #   and the rest of args are supplied in code
    toolbox.register('evaluate', eval_indvidual_fitness, instance=json_instance, unit_cost = 1)

    # Selection method
    toolbox.register("select", tools.selNSGA2)

    # Crossover method
    toolbox.register("mate", cxOrderedVrp)

    # Mutation method
    toolbox.register("mutate", mutationShuffle, indpb = mut_prob)

    # Creating logbook and Stats object, We are going to use them to record data
    logbook, stats = createStatsObjs()

    ### Starting ga process
    print(f"Generating population with size of {pop_size}")
    pop = toolbox.population(n=pop_size)

    ## Print Checks
    # print(len(pop))
    # print(f"First element of pop is {pop[0]}")

    # Getting all invalid individuals who don't have fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]

    # Print checks
    # print(f"Length of invalid_ind is {len(invalid_ind)}")    

    # Evaluate the population, making list for same size as population
    fitnesses = list(map(toolbox.evaluate, invalid_ind))

    # Print checks
    # print(fitnesses)
    # firstfitness = eval_indvidual_fitness(pop[0],json_instance,1.0)
    # secondfitness = toolbox.evaluate(pop[0])
    # Print Checks
    # print(f"The first element fitness value is {pop[0].fitness.values}")
    # print(firstfitness)
    # print(secondfitness)

    # Assigning fitness attribute to each of the individual with the calculated one
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    
    # Print Checks
    # Check if invalid indiviudals are there, Should return 0, since we have assigned fitness
    #       to each one
    # print(f"Invalidity check {not invalid_ind[0].fitness.valid}")
    # print(f"Individuals with invalid fitness {len([ind for ind in invalid_ind if not ind.fitness.valid])}")


    # Assigning crowding distance using NSGA selection process, no selection is done here
    pop = toolbox.select(pop, len(pop))

    # Print Checks
    # print(f"The first element crowding distance {pop[230].fitness.crowding_dist}")
    # for i in pop:
    #     print(f"Crowd distance is {i.fitness.crowding_dist}")

    # After generating population and assiging fitness to them
    # Recording Logs and Stats
    print("Recording the Data and Statistics")
    recordStat(invalid_ind, logbook, pop, stats,gen=0)

    # Starting the generation process
    for gen in range(num_gen):
        print(f"######## Currently Evaluating {gen} Generation ######## ")

        # Selecting individuals
        # Selecting offsprings from the population, about 1/2 of them
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        # Print Checks
        # print(f"Offsprings length is {len(offspring)}")
        # print(f"Offsprings are {offspring}")

        # Performing , crossover and mutation operations according to their probabilities
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            # Mating will happen 80% of time if cross_prob is 0.8
            if random.random() <= cross_prob:
                # print("Mating happened")
                toolbox.mate(ind1, ind2)

                # If cross over happened to the individuals then we are deleting those individual
                #   fitness values, This operations are being done on the offspring population.
                del ind1.fitness.values, ind2.fitness.values                 
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
   

        # Print Checks
        # print(f"The len of offspring after operations {len(offspring)}")
        # print(f"Individuals with invalid fitness {len([ind for ind in offspring if not ind.fitness.valid])}")

        # Calculating fitness for all the invalid individuals in offspring
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        

        # Recalcuate the population with newly added offsprings and parents
        # We are using NSGA2 selection method, We have to select same population size
        pop = toolbox.select(pop + offspring, pop_size)


        # Recording stats in this generation
        recordStat(invalid_ind, logbook, pop, stats,gen+1)

    print(f"{20*'#'} End of Generations {20*'#'} ")

    best_individual = tools.selBest(pop, 1)[0]

    # Printing the best after all generations
    print(f"Best individual is {best_individual}")
    print(f"Number of vechicles required are {best_individual.fitness.values[0]}")
    print(f"Cost required for the transportation is {best_individual.fitness.values[1]}")

    # Printing the route from the best individual
    printRoute(routeToSubroute(best_individual, json_instance))

    # Extra
    print(f"Testing whether we can export logbook")
    print(logbook[1].keys())

    # Exporting csv
    csv_file_name = f"{json_instance['instance_name']}_pop{pop_size}_crossProb{cross_prob}_mutProb{mut_prob}_numGen{num_gen}.csv"
    exportCsv(csv_file_name, logbook)


nsga2vrp()

