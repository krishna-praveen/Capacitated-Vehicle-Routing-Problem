from plots.plotVehicleRoutes import *
from plots.plotGenerations import *
import json




if __name__ == "__main__":
    # Plotting Min fitness with each generation for each result
    createAllFitnessPlots()

    # Plotting Best Route for last generation in each result
    # Get all the result paths
    allpaths, csv_files = loadResultPaths()

    # Plotting Route graphs for each vehicle for each result
    for eachpath in allpaths:
        instance = loadCsv(eachpath)
        best_route_column = instance['best_one']
        # get the last row
        best_last_one = best_route_column.iloc[-1]
        csv_title = eachpath.split("/")[-1][:-4]
        best_last_one = json.loads(best_last_one)
        # print(csv_title)
        # print(best_last_one[0])
        plotRoute(best_last_one, csv_title)


