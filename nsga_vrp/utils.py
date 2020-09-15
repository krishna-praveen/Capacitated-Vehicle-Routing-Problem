import os
import io
import fnmatch
from json import load, dump

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def calculate_distance(customer1, customer2):
    # Calculate distance between customer1 and customer 2 given their
    #   euclidean coordinates, returns euclidean distance
    """
    Inputs: customer1 from json object, customer2 from json object
    Outputs: Returns Euclidian distance between these customer locations.
    """
    return ((customer1['coordinates']['x'] - customer2['coordinates']['x']) ** 2 + \
            (customer1['coordinates']['y'] - customer2['coordinates']['y']) ** 2) ** 0.5


def converttext2json():
    """
    Inputs : None
    Outputs: Reads the *.txt file in text directory and converts in to
             *.json file in json directory.
    """
    print(f'base directory is {BASE_DIR}')
    text_dir = os.path.join(BASE_DIR, 'data', 'text')
    json_dir = os.path.join(BASE_DIR, 'data', 'json')
    print(f'text_dir is {text_dir}')
    print(f'json_dir is {json_dir}')

    for text_file in map(lambda text_filename: os.path.join(text_dir, text_filename), \
                         fnmatch.filter(os.listdir(text_dir), '*.txt')):
        print(text_file)
        json_data = {}
        numCustomers = 0
        with io.open(text_file, 'rt', newline='') as file_object:
            for line_count, line in enumerate(file_object, start=1):
                # print(f'line_count is {line_count}')
                # print(f'line is {line}')

                if line_count in [2, 3, 4, 6, 7, 8, 9]:
                    pass

                # Instance name details, input text file name
                elif line_count == 1:
                    json_data['instance_name'] = line.strip()

                # Vehicle capacity and max vehicles details
                elif line_count == 5:
                    values = line.strip().split()
                    json_data['max_vehicle_number'] = int(values[0])
                    json_data['vehicle_capacity'] = float(values[1])

                # Depot details
                elif line_count == 10:
                    # This is depot
                    values = line.strip().split()
                    json_data['depart'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }

                # Customer details
                else:
                    # Rest all are customers
                    # print(f'line_count is {line_count}')
                    # print(f'line is {line}')
                    # Adding customer to number of customers
                    numCustomers += 1
                    values = line.strip().split()
                    json_data[f'customer_{values[0]}'] = {
                        'coordinates': {
                            'x': float(values[1]),
                            'y': float(values[2]),
                        },
                        'demand': float(values[3]),
                        'ready_time': float(values[4]),
                        'due_time': float(values[5]),
                        'service_time': float(values[6]),
                    }

        # print(f'Number of customers is {numCustomers}')
        customers = ['depart'] + [f'customer_{x}' for x in range(1, numCustomers + 1)]
        # print(customers)

        # Writing the distance_matrix
        json_data['distance_matrix'] = [[calculate_distance(json_data[customer1], \
                                                            json_data[customer2]) for customer1 in customers] for
                                        customer2 in customers]

        # Writing the number of customers details
        json_data['Number_of_customers'] = numCustomers

        # Giving filename as instance name, which is input text file name
        json_file_name = f"{json_data['instance_name']}.json"
        json_file = os.path.join(json_dir, json_file_name)
        print(f'Write to file: {json_file}')

        # Writing the json file to disk and saving it under json_customize directory
        with io.open(json_file, 'wt', newline='') as file_object:
            dump(json_data, file_object, sort_keys=True, indent=4, separators=(',', ': '))


if __name__ == "__main__":
    converttext2json()
