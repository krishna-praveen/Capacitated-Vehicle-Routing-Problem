import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from nsga_vrp.NSGA2_vrp import load_instance, routeToSubroute, eval_indvidual_fitness


# Loading locations and customers to dataframe

def getCoordinatesDframe(json_instance):
    num_of_cust = json_instance['Number_of_customers']
    # Getting all customer coordinates
    customer_list = [i for i in range(1, num_of_cust + 1)]
    x_coord_cust = [json_instance[f'customer_{i}']['coordinates']['x'] for i in customer_list]
    y_coord_cust = [json_instance[f'customer_{i}']['coordinates']['y'] for i in customer_list]
    # Getting depot x,y coordinates
    depot_x = [json_instance['depart']['coordinates']['x']]
    depot_y = [json_instance['depart']['coordinates']['y']]
    # Adding depot details
    customer_list = [0] + customer_list
    x_coord_cust = depot_x + x_coord_cust
    y_coord_cust = depot_y + y_coord_cust
    df = pd.DataFrame({"X": x_coord_cust,
                       "Y": y_coord_cust,
                       "customer_list": customer_list
                       })
    return df


def plotSubroute(subroute, dfhere,color):
    totalSubroute = [0]+subroute+[0]
    subroutelen = len(subroute)
    for i in range(subroutelen+1):
        firstcust = totalSubroute[0]
        secondcust = totalSubroute[1]
        plt.plot([dfhere.X[firstcust], dfhere.X[secondcust]],
                 [dfhere.Y[firstcust], dfhere.Y[secondcust]], c=color)
        totalSubroute.pop(0)


def plotRoute(route):
    # Loading the instance
    json_instance = load_instance('../data/json/Input_Data.json')

    subroutes = routeToSubroute(route, json_instance)
    colorslist = ["blue","green","red","cyan","magenta","yellow","black","#eeefff"]
    colorindex = 0

    # getting df
    dfhere = getCoordinatesDframe(json_instance)

    # Plotting scatter
    plt.figure(figsize=(10, 10))

    for i in range(dfhere.shape[0]):
        if i == 0:
            plt.scatter(dfhere.X[i], dfhere.Y[i], c='green', s=200)
            plt.text(dfhere.X[i], dfhere.Y[i], "depot", fontsize=12)
        else:
            plt.scatter(dfhere.X[i], dfhere.Y[i], c='orange', s=200)
            plt.text(dfhere.X[i], dfhere.Y[i], f'{i}', fontsize=12)

    # Plotting routes
    for route in subroutes:
        plotSubroute(route, dfhere, color=colorslist[colorindex])
        colorindex += 1


if __name__ == "__main__":
    sample_route = [1, 2, 4, 25, 24, 22, 23, 17, 13, 10, 15, 19, 18, 12, 14, 16, 11, 9, 6, 8, 7, 3, 5, 21, 20]
    plotRoute(sample_route)
    plt.show()


