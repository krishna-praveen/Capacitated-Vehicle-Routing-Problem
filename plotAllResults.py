from plots.plotResults import *
from plots.plotGenerations import *

if __name__ == "__main__":
    createAllFitnessPlots()
    sample_route = [ 13, 10, 15, 19, 25, 24, 22, 23, 17,18, 12, 14, 16, 11, 9, 6, 8, 7, 3, 5, 21, 20,1,2,4]
    plotRoute(sample_route)
    plt.show()

