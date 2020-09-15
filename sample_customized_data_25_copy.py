# -*- coding: utf-8 -*-

'''sample_customized_data.py'''

import random
from gavrptw.core import run_gavrptw


def main():
    '''main()'''
    random.seed(64)

    instance_name = 'Input_Data'

    unit_cost = 1

    ind_size = 25
    pop_size = 400
    cx_pb = 0.85
    mut_pb = 0.02
    n_gen = 300

    export_csv = True
    customize_data = True

    run_gavrptw(instance_name=instance_name, unit_cost=unit_cost, ind_size=ind_size, pop_size=pop_size, \
        cx_pb=cx_pb, mut_pb=mut_pb, n_gen=n_gen, export_csv=export_csv, \
        customize_data=customize_data)


if __name__ == '__main__':
    main()
