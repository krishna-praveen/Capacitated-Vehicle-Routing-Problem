

# Capacitated Vechile Routing

Multiobjective python implementation of capacitated vehicle routing
 problem with NSGA-II algorithm using [deap](https://github.com/deap/deap) package.


## Contents
- [Installation](#installation)
    - [Requirements](#requirements)
    - [Installing with Virtualenv](#installing-with-virtualenv)
- [Quick Start](#quick-start)
- [Problem Statement](#problem-statement)
    - [Text File Format](#text-file-format)
    - [JSON Format](#json-format)
    - [Convert `*.txt` to `*.json`](#convert-txt-to-json)
- [NSGA-II Implementation](#nsga-ii-implementation)
    - [Individual (Chromosome)](#individual-chromosome)
        - [Individual Coding](#individual-coding)
        - [Individual Decoding](#individual-decoding)
        - [Print Route](#print-route)
    - [Evaluation](#evaluation)
    - [Selection: Roulette Wheel Selection](#selection-roulette-wheel-selection)
    - [Crossover: Partially Matched Crossover](#crossover-partially-matched-crossover)
    - [Mutation: Inverse Operation](#mutation-inverse-operation)
    - [Algorithm](#algorithm)
    - [Sample Codes](#sample-codes)
        - [Instance: R101](#instance-r101)
        - [Instance: C204](#instance-c204)
        - [Customized Instance](#customized-instance)
        - [View Logs](#view-logs)
- [API Reference](#api-reference)
    - [Module: `gavrptw`](#module-gavrptw)
    - [Module: `gavrptw.core`](#module-gavrptwcore)
    - [Module: `gavrptw.utils`](#module-gavrptwutils)
- [File Structure](#file-structure)
- [Further Reading](#further-reading)
- [References](#references)
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






























