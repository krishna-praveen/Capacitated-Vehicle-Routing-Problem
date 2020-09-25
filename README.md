

# Capacitated Vechile Routing

Multiobjective python implementation of capacitated vehicle routing
 problem with NSGA-II algorithm using [deap](https://github.com/deap/deap) package.


## Contents
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Installing with Virtualenv](#installing-with-virtualenv)
- [Problem Statement](#problem-statement)
- [Parsing Input](#parsing-input)
    - [Text File Format](#text-file-format)
    - [JSON Format](#json-format)
    - [Convert `*.txt` to `*.json`](#convert-txt-to-json)
- [Running Algorithm](#running-algorithm)
- [Algorithm Selection](#algoritm-selection)
- [Assumptions](#assumptions)
- [NSGA-II Implementation](#nsga-ii-implementation)
    - [Individual (Chromosome)](#individual-chromosome)
        - [Individual Coding](#individual-coding)
        - [Individual Decoding](#individual-decoding)
    - [Fitness evaluation](#fitness-evaluation)
    - [Selection: Non dominated sorting selection](#selection-non-dominated-sorting-selection)
    - [Crossover: Ordered Crossover](#crossover-ordered-crossover)
    - [Mutation: Inverse Operation](#mutation-inverse-operation)

- [Running Tests](#running-tests)
- [Visualizations](#visualizations)
    - [Distance Travelled vs Generations](#distance-travelled-vs-generations)
    - [Efficient vehicle routing in last generation](#efficient-vehicle-routing-in-last-generation)
- [File Structure](#file-structure)
- [Framework Documentation](#framework-documentation)
- [Future Improvements](#future-improvements)
- [License](#license)


## Installation
### Requirements
- [Python 3.8](https://docs.python.org/)
- [Pip](https://pypi.python.org/pypi/pip)
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)

### Installing with Virtualenv
On Unix, Linux, BSD, macOS, and Cygwin:

```sh
git clone https://github.com/icav_vrp.git
cd icav_vrp
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Problem Statement
Delivery companies every day
need to deliver packages to many different clients. The deliveries are accomplished using an
available fleet of vehicles from a central warehouse. The goal of this exercise is to design a
route for each vehicle so that all customers are served, and the number of vehicles
**(objective 1)** along with the total traveled distance **(objective 2)** by all the vehicles are
minimized. In addition, the capacity of each vehicle should not be exceeded (constraint 1)

**Notes**
1. For each client we have we only need to consider first four fields. They are `id, xcoord, ycoord, demand`
2. Distance between each client can be calculated using `Euclidian formula`



## Parsing Input

### Text File Format
The text files for this problem which are inputs provided can be found in the 
`data/text` directory. Text file is named as `Input_Data.txt`.

The description of the format of the text file defined in the problem instance

```
<Instance Name>
<empty line>
VEHICLE
NUMBER  CAPACITY
 K        Q
<empty line>
CUSTOMER
CUST NO.   XCOORD.  YCOORD.    DEMAND    READY TIME  DUE DATE  SERVICE TIME
 
    0      40         50          0          0       1236          0   
    1      45         68         10          0       1127         90   
    2      45         70         30          0       1125         90
    .......
    n      x_n        y_n       d_n         r_n      due_n        s_n 
```

**Definitions**
1. `CUST No.` 0 denotes the depot , where all vehicles start and finish
2.  `K` denotes maximum number of vehicles that are available
3.  `Q` denotes maximum capacity of each vehicle
4.  `n` denotes the maximum number of customers in the given problem, excluding the depot

### JSON Format
Since text file is pretty bad to behave in object oriented way , we are converting
given text input file into JSON format. And they are stored under `data/json` directory.
The file name of these json file is same as text file and it can be named as instance in the
code. Since our problem is `Input_Data.txt` our json file will be `Input_Data.json`.

**Notes**
1. We are adding additional fields here such as `Number_of_customers`,`distance_matrix`
which are calculated from `Input_Data.txt`.
2. `distance_matrix` contains distances from each customer to other with first array being distances from
depot.
3. If a json file doesn't exist at the `data/json` directory , when we run `parseText2Json` it creates
json file. If it exists its overwritten.


Below is description of the JSON format.

```js
{
    "instance_name" : "<Instance name>",
    "Number_of_customers" : n,
    "max_vehicle_number" : K,
    "vehicle_capacity" : Q,
    "depart" : {
        "coordinates" : {
            "x" : x0,
            "y" : y0
        },
        "demand" : q0,
        "ready_time" : e0,
        "due_time" : l0,
        "service_time" : s0
    },
    "customer_1" : {
        "coordinates" : {
            "x" : x1,
            "y" : y2
        },
        "demand" : q1,
        "ready_time" : e1,
        "due_time" : l1,
        "service_time" : s1
    },
    ...
    "customer_n" : {
        "coordinates" : {
            "x" : x_n,
            "y" : y_n
        },
        "demand" : q100,
        "ready_time" : e100,
        "due_time" : l100,
        "service_time" : s100
    },
    "distance_matrix" : [
        [dist0_0, dist0_1, ..., dist0_n],
        [dist1_0, dist1_1, ..., dist1_n],
        ...
        [distn_0, distn_1, ..., dist0_0]
    ]
}

```

### Convert `*.txt` to `*.json`
Run the `parseText2Json.py` to convert `*.txt` file to `*.json` file.

```sh
python parseText2Json.py
```


## Running Algorithm
To run the algorithm activate the virtual environment that you have named and run this command

```sh
python runAlgo.py 
```

Additionally you can specify arguments to change the hyperparameters or even file names. The 
following arguments are available

```sh
python runAlgo.py --popSize=300 --crossProb=0.7 --mutProb=0.01 --numGen=320
```

 - `--pop_size` : Specify the number of population that is generated
 - `--crossProb` : Cross over probability that needs to be considered
 - `--mutProb` : Mutation probability 
 - `--numGen` : Number of generations that you want the algorithm to run

On doing so the above, the following result file will be generated in the `results` directory
`Input_Data_pop300_crossProb0.7_mutProb0.01_numGen320.csv` which can later be used to plot results from them.

## Algorithm Selection
Multiobjective optimization of travelling salesman is a NP-hard problem.
So simple Genetic algorithm cannot compute good solutions when there are
multiple objectives. We need a non dominated sorting approach where only
non dominated inviduals are selected. Another way of formulating this problem is to 
use genetic algorithm but combining both objectives into a single one.

Here our objective is 
```
Minimize -> Number of vehicles
Minimize -> Distance travelled by all vehicles
```

This can be formulated in another way like this
```
Minimize -> (Number of vehicles) * (Distance travelled by all vehicles)

---- or -----

Maximize -> 1/ (Num of vehicles) *(Distance by all )
```

## Assumptions
We are assuming the following things.

1. There is no time delay and no time windows for our vehicle at the objective locations
2. Fixed cost for extra vehicle is assumed to be 0.
3. Due date, service time , ready time are Ignored
4. Distance between client to client is assumed to be Euclidean.
5. Vehicle always starts from the depot `customer_0` and delivers goods 
and then comes back to depot again after delivery
6. 


## NSGA-II Implementation

### Individual (Chromosome)
#### Individual Coding
All visited customers of a route (including several sub-routes) are coded into an `individual` in turn. For example, the following route

```
Sub-route 1: 0 - 5 - 3 - 2 - 0
Sub-route 2: 0 - 7 - 1 - 6 - 9 - 0
Sub-route 3: 0 - 8 - 4 - 0
```
are coded as `5 3 2 7 1 6 9 8 4`, which can be stored 
in a Python `list` object, i.e., `[5, 3, 2, 7, 1, 6, 9, 8, 4]`.


#### Individual Decoding
The route of is given as sequence of customers , but it is actually divided in to subroutes according to the
load carrying capacity of the vechicle. Starting from the depot demand from each customer is added and when the load
exceeds the vechicle capacity the subroute is closed and assigned to that vechicle. This process is repeated until all
the customers in the sequence is fulfilled. Thus we will get subroutes from routes and number of subroutes
is equivalent to number of vechicles.

```python
routeToSubroute(individual, instance)
```
Decodes an `individual` to `route`. Refer the below example

```python
# Individual
[12, 14, 16, 8, 9, 11, 21, 20, 5, 3, 4, 6, 10, 7, 2, 1, 22, 25, 24, 23, 18, 19, 17, 15, 13]

# Route
[[12, 14, 16], [8, 9, 11, 21, 20], [5, 3, 4, 6, 10], [7, 2, 1], [22, 25, 24], [23, 18, 19, 17], [15, 13]]
```

### Fitness Evaluation
Since our problem is Multiobjective , we need to calculated two objectives here
One is `Number of vehicles` and `Total Distance Travelled`

So we divided the objectives, calculate them and return a `tuple`

First objective is calculated using `getNumVehiclesRequired` function
which just finds number of elements in list after the `Indiviudal` is 
passed in to `routeToSubroute`

Second objective is caclulated using `getRouteCost`.
After dividing an individual in to sub routes, For each subroute distance
is calculated between indiviudals and added. Final Route cost will be
addition of all these sub routes cost

```python
eval_indvidual_fitness(individual, instance, unit_cost)
```
This function returns a tuple of `(Num of vehicles, Route Cost)`
We have to minimize both the objectives at same time.
So when we create our individual using [deap]() package, we have to specify the
individual in following way - 

```python
creator.create('FitnessMin', base.Fitness, weights=(-1.0, -1.0))
```

Assigning weights (-1.0, -1.0) is crucial step when defining objective.

### Selection: Non dominated sorting selection

Apply NSGA-II selection operator on the *individuals*. Usually, the
size of *individuals* will be larger than *k* because any individual
present in *individuals* will appear in the returned list at most once.
Having the size of *individuals* equals to *k* will have no effect other
than sorting the population according to their front rank. The
list returned contains references to the input *individuals*. For more
details on the NSGA-II operator see [Deb2002](https://www.iitk.ac.in/kangal/Deb_NSGA-II.pdf).

From a group of individuals, it selects `k` number of inviduals for next
generation. First, all the individuals are assigned crowding distance.

The algorithm works as follows -

1. First parent `Pt` and offspring population `Qt` are combined to form `Rt`
2. Fast non dominated sorting is performed over combined population, to find Pareto Fronts
3. Now next generation parent Population say Pt+1 is to be filled
    - Assign crowding distance in Each pareto front
    - If population length doesn't exceed initial parent population, add this population
      to `Pt+1`, Repeat this process until this condition is overridden
4. Now we are in say some Pareto front `Fi` and we have to add `N-Pt+1` population
    - Sort all individuals in `Fi` using `<` **crowded** operator
    - Keep adding new population until it doesn't reach `N`
5. Now `N` individuals are selected for next generation
6. Perform `Crossover` and `Mutation` operations over these population
7. This new population is `Qt+1` , aka., `offspring`
8. Repeat 1-7 until all generations are complete.

```python
selNSGA2(individuals, k, nd='standard')
```

### Crossover: Ordered Crossover
Ordered crossover will never give us invalid and infeasible
individuals or routes which have same customer multiple times. This helps
us in computing fitness values without rechecking if an individual is valid or not.

Executes an ordered crossover (OX) on the input
individuals. The two individuals are modified in place. This crossover
expects :term:`sequence` individuals of indices, the result for any other
type of individuals is unpredictable.

Moreover, this crossover generates holes in the input
individuals. A hole is created when an attribute of an individual is
between the two crossover points of the other individual. Then it rotates
the element so that all holes are between the crossover points and fills
them with the removed elements in order. For more details see
[Goldberg1989]

```python
cxOrdered(ind1, ind2)
```

Ordered CrossOver works as follows - 
Lets say we have two routes `A` and `B` as follows

```
A = 9 8 4 5 6 7 1 3 2 10
B = 8 7 1 2 3 10 9 5 4 6
```
Here we select two random positions in `A` and `B`
say we select  3 and 6

```
A = 9 8 4 | 5 6 7 | 1 3 2 10
B = 8 7 1 | 2 3 10 | 9 5 4 6
```

Now , ordered crossover uses sliding motion to left to fill the holes
by transferring mapped positions. For example, when string `B` maps to string `A`,
the cities 5, 6, 7 will leave hoes in string `B`

```
B = 8 H 1 | 2 3 10 | 9 H 4 H
```
Now these holes are filled with a sliding motion towards left.
To understand this in better way imagine that holes `H` are rocks and
middle portion in between | | is a pond, rest numbers will float but only in the
first and last regions. Say that if hole `H` comes in pond it is stuck there and cant get out.
And also all the numbers in the right tail that is `9 * 4 *` are also stuck there.
So , we start moving entire thing slowly left, 

```
After 1 digit displacement towards left
B = H 1 2 | 3 10 H | 9 4 H 8

After another digit displacement
B = 1 2 3 | 10 H H | 9 4 8 H

After another digit displacement
B = 2 3 10 | H H H  | 9 4 8 1

Remember that H cannot escape in between | | and alos numbers cannot escape the last tail
```

After full sliding motion and filling portion in between | |
we have the following `B`

```
B = 2 3 10 | H H H | 9 4 8 1
```

Similarily repeating this process for A - 

```
A = 9 8 4 | 5 6 7 | 1 H H H

After 1 digit displacement towards left

A = 8 4 5 | 6 7 H | 1 H H 9

After another digit displacement

A = 4 5 6 | 7 H H | 1 H 9 8

After another digit displacement

A = 5 6 7 | H H H | 1 9 8 4
```

Now we just have to swap middle portions that are cut in first place and we have
two new individuals. They will be - 

```
A_new = 5 6 7 | 2 3 10 | 1 9 8 4
B_new = 2 3 10| 5 6 7 | 9 4 8 1
```

Ultimately we swapped `5, 6, 7 ` cities from `A` and `2 3 10`
cities from `B` to each other , but no repeatation of cities in both
`A_new` and `B_new`


### Mutation: Inverse Operation
Inverses the cities between two random points of input individual and returns
new one. The mutation is controlled by mutation probability and is executed over all the
offspring population. 

```
A = 5 6 7 2 3 10 1 9 8 4
```
Say our mutation probability is `0.02` and randomly we selected 
position `4` and `8`

So our new individual will be
```
A = 5 6 7 9 3 10 1 2 8 4
```

## Running Tests
We used python inbuilt `unittest` module to run all the tests
To run all the tests do the following

```sh
python -m unittest discover test
```
This command will discover all the tests in the test folder and runs them all.


## Visualizations
Plots are generated for Minimum fitness values for each combination of parameters with respect to 
population generations.
Vechicle routing plots are generated as well where each color represents a route taken by a vehicle.
The final combination of routes is the best route that is generated at the end of generations for each
combination of parameters

### Distance Travelled vs Generations
![image info](./figures/Input_Data_pop400_crossProb0.8_mutProb0.02_numGen150.png)
![image info](./figures/Input_Data_pop400_crossProb0.8_mutProb0.02_numGen180.png)
![image info](./figures/Input_Data_pop400_crossProb0.8_mutProb0.02_numGen200.png)
![image info](./figures/Input_Data_pop400_crossProb0.8_mutProb0.02_numGen220.png)
![image info](./figures/Input_Data_pop400_crossProb0.8_mutProb0.02_numGen300.png)
![image info](./figures/Input_Data_pop400_crossProb0.8_mutProb0.02_numGen400.png)
![image info](./figures/Input_Data_pop400_crossProb0.85_mutProb0.02_numGen150.png)
![image info](./figures/Input_Data_pop4000_crossProb0.8_mutProb0.02_numGen180.png)

### Efficient vehicle routing in last generation
![image info](./figures/Route_Input_Data_pop400_crossProb0.8_mutProb0.02_numGen150.png)
![image info](./figures/Route_Input_Data_pop400_crossProb0.8_mutProb0.02_numGen180.png)
![image info](./figures/Route_Input_Data_pop400_crossProb0.8_mutProb0.02_numGen200.png)
![image info](./figures/Route_Input_Data_pop400_crossProb0.8_mutProb0.02_numGen220.png)
![image info](./figures/Route_Input_Data_pop400_crossProb0.8_mutProb0.02_numGen300.png)
![image info](./figures/Route_Input_Data_pop400_crossProb0.8_mutProb0.02_numGen400.png)
![image info](./figures/Route_Input_Data_pop400_crossProb0.85_mutProb0.02_numGen150.png)
![image info](./figures/Route_Input_Data_pop4000_crossProb0.8_mutProb0.02_numGen180.png)


## File Structure
```
├── data/
│   ├── json/
│   │   ├── <Instance name>.json
│   │   └── ...
│   ├── text/
│   │   ├── <Instance name>.txt
│   │   └── ...
├── figures/
│   ├── Input_Data_... .png
│   └── ...
├── plots/
│   ├── __init__.py
│   └── plotGenerations.py
│   └── plotVehicleRoutes.py
├── results/
│   └── ...
├── nsga_vrp/
│   ├── __init__.py
│   ├── NSGA2_vrp.py
│   └── utils.py
├── test/
│   ├── __init__.py
│   ├── test_distance.py
│   └── test_route.py
├── parseText2Json.py
├── plotAllResults.py
├── runAlgo.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Framework Documentation
**Distributed Evolutionary Algorithms in Python**

- [DEAP github](https://github.com/DEAP/deap)
- [DEAP documentation](http://deap.readthedocs.org/)


## Future Improvements

1. Test cases for mutation , crossover and selection
2. Web based interface to Input data and see the graphs and Optimal route
3. Comparison of frameworks and hyperparameter optimization
4. Gifs of transporation route and how is it changing with generations

## License
MIT License





























