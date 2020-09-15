
import os
import io
import random
from csv import DictWriter
import fnmatch
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
def ind2route(individual, instance):
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


# Calculate the number of vehicles required, given a route
def getNumVehiclesRequired(individual, instance):
    """
    Inputs: Individual route
            Json file object loaded instance
    Outputs: Number of vechiles according to the given problem and the route
    """
    # Get the route with subroutes divided according to demand
    updated_route = ind2route(individual, instance)
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
    updated_route = ind2route(individual, instance)

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
    test_instance = load_instance('./data/json_customize/Input_Data.json')

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
    print(f"Subroutes for first sample individual is {ind2route(sample_individual, test_instance)}")
    print(f"Subroutes for second sample indivudal is {ind2route(sample_ind_2, test_instance)}")
    print(f"Subroutes for best sample indivudal is {ind2route(best_ind_300_gen, test_instance)}")

    # Getting num of vehicles
    print(f"Vehicles for sample individual {getNumVehiclesRequired(sample_individual, test_instance)}")
    print(f"Vehicles for second sample individual {getNumVehiclesRequired(sample_ind_2, test_instance)}")
    print(f"Vehicles for best sample individual {getNumVehiclesRequired(best_ind_300_gen, test_instance)}")

# testroutes()


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

    newind7, newind8 = cxOrderedVrp(ind1, ind2)

    print(f"InpInd1 is {ind1}")
    print(f"InpInd2 is {ind2}")
    # print(f"New_ind is {[x-1 for x in ind1]}")
    print(f"newind7 is {newind7}")
    print(f"newind8 is {newind8}")


# testcrossover()


def mutationShuffle(individual, indpb):

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



def nsga2vrp():

    # Loading the instance
    json_instance = load_instance('./data/json/Input_Data.json')
    
    # Getting number of customers to get individual size
    ind_size = json_instance['Number_of_customers']

    # Setting variables
    pop_size = 400

    # Crossover probability
    cross_prob = 0.8
    # Mutation probability
    mut_prob = 0.02
    # Number of generations to run
    num_gen = 300

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

    ### Starting ga process
    print(f"Generating population with size of {pop_size}")
    pop = toolbox.population(n=pop_size)

    ## Print Checks
    print(len(pop))
    print(f"First element of pop is {pop[0]}")

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

    # Starting the generation process
    for gen in range(num_gen):
        print(f"######## Currently Evaluating {gen} Generation ######## ")

        # Selecting individuals
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        # Print Checks
        print(f"Offsprings length is {len(offspring)}")
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
        print(f"The len of offspring after operations {len(offspring)}")
        print(f"Individuals with invalid fitness {len([ind for ind in offspring if not ind.fitness.valid])}")

        # Calculating fitness for all the invalid individuals in offspring
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        

        # Recalcuate the population with newly added offsprings and parents
        # We are using NSGA2 selection method, We have to select same population size
        pop = toolbox.select(pop + offspring, pop_size)
        print(f"New population size is {len(pop)}")

    print(f"{20*'#'} End of Generations {20*'#'} ")

    best_individual = tools.selBest(pop, 1)[0]
    print(f"Best individual is {best_individual}")
    print(f"Fitness of best individual is {best_individual.fitness.values}")



# nsga2vrp()



def run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost, ind_size, pop_size, \
    cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False):
    '''gavrptw.core.run_gavrptw(instance_name, unit_cost, init_cost, wait_cost, delay_cost,
        ind_size, pop_size, cx_pb, mut_pb, n_gen, export_csv=False, customize_data=False)'''
    if customize_data:
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json_customize')
    else:
        json_data_dir = os.path.join(BASE_DIR, 'data', 'json')
    json_file = os.path.join(json_data_dir, f'{instance_name}.json')
    instance = load_instance(json_file=json_file)
    if instance is None:
        return
    creator.create('FitnessMax', base.Fitness, weights=(1.0, ))
    creator.create('Individual', list, fitness=creator.FitnessMax)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register('indexes', random.sample, range(1, ind_size + 1), ind_size)
    # Structure initializers
    toolbox.register('individual', tools.initIterate, creator.Individual, toolbox.indexes)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    # Operator registering
    toolbox.register('evaluate', eval_vrptw, instance=instance, unit_cost=unit_cost, \
        init_cost=init_cost, wait_cost=wait_cost, delay_cost=delay_cost)
    toolbox.register('select', tools.selRoulette)
    toolbox.register('mate', cx_partialy_matched)
    toolbox.register('mutate', mut_inverse_indexes)
    pop = toolbox.population(n=pop_size)
    # Results holders for exporting results to CSV file
    csv_data = []
    print('Start of evolution')
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    print(f'  Evaluated {len(pop)} individuals')
    # Begin the evolution
    for gen in range(n_gen):
        print(f'-- Generation {gen} --')
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < cx_pb:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values
        for mutant in offspring:
            if random.random() < mut_pb:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        print(f'  Evaluated {len(invalid_ind)} individuals')
        # The population is entirely replaced by the offspring
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum([x**2 for x in fits])
        std = abs(sum2 / length - mean**2)**0.5
        print(f'  Min {min(fits)}')
        print(f'  Max {max(fits)}')
        print(f'  Avg {mean}')
        print(f'  Std {std}')
        # Write data to holders for exporting results to CSV file
        if export_csv:
            csv_row = {
                'generation': gen,
                'evaluated_individuals': len(invalid_ind),
                'min_fitness': min(fits),
                'max_fitness': max(fits),
                'avg_fitness': mean,
                'std_fitness': std,
            }
            csv_data.append(csv_row)
    print('-- End of (successful) evolution --')
    best_ind = tools.selBest(pop, 1)[0]
    print(f'Best individual: {best_ind}')
    print(f'Fitness: {best_ind.fitness.values[0]}')
    print_route(ind2route(best_ind, instance))
    print(f'Total cost: {1 / best_ind.fitness.values[0]}')
    if export_csv:
        csv_file_name = f'{instance_name}_uC{unit_cost}_iC{init_cost}_wC{wait_cost}' \
            f'_dC{delay_cost}_iS{ind_size}_pS{pop_size}_cP{cx_pb}_mP{mut_pb}_nG{n_gen}.csv'
        csv_file = os.path.join(BASE_DIR, 'results', csv_file_name)
        print(f'Write to file: {csv_file}')
        make_dirs_for_file(path=csv_file)
        if not exist(path=csv_file, overwrite=True):
            with io.open(csv_file, 'wt', newline='') as file_object:
                fieldnames = [
                    'generation',
                    'evaluated_individuals',
                    'min_fitness',
                    'max_fitness',
                    'avg_fitness',
                    'std_fitness',
                ]
                writer = DictWriter(file_object, fieldnames=fieldnames, dialect='excel')
                writer.writeheader()
                for csv_row in csv_data:
                    writer.writerow(csv_row)


