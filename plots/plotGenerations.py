import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import ast
import json
import glob
from nsga_vrp.NSGA2_vrp import load_instance, routeToSubroute, eval_indvidual_fitness


def loadResultPaths():
    allpaths = glob.glob("./results/*.csv")
    allpaths = [i.replace("\\","/") for i in allpaths]
    csv_files = [eachpath.split("/")[-1] for eachpath in allpaths]
    return allpaths, csv_files


def loadCsv(csv_file_path):
    instance = pd.read_csv(csv_file_path)
    return instance


def cleanResult(csv_file_path):
    loaded_result = loadCsv(csv_file_path)
    min_column = loaded_result['min']
    gen_column = loaded_result['Generation']

    def clean_row(inp):
        out = inp.replace("[","").replace("]","").strip().split(" ")
        return out

    min_dist = [float(clean_row(i)[-1]) for i in min_column]
    min_vehicles = [float(clean_row(i)[0]) for i in min_column]
    return min_dist, gen_column


def plotFitnessFromCSV(csv_file_path):
    distances, generations = cleanResult(csv_file_path)
    csv_title = csv_file_path.split("/")[-1][:-4]
    # Num_gen = csv_title.split("")
    # print(csv_title)
    fig = plt.figure(figsize=(10, 10))
    plt.plot(generations, distances)
    plt.xlabel("Generations")
    plt.ylabel("Min distance")
    plt.title(csv_title)
    plt.savefig(f"./figures/Fitness_{csv_title}.png")
    # plt.show()



def createAllFitnessPlots():
    allpaths, csv_files = loadResultPaths()

    # Plotting all
    for eachpath in allpaths:
        plotFitnessFromCSV(eachpath)



