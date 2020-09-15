import matplotlib.pyplot as plt




def plotTSP(path, points, num_iters=1):
    """
    path: List of lists with the different orders in which the nodes are visited
    points: coordinates for the different nodes
    num_iters: number of paths that are in the path list

    """

    # Unpack the primary TSP path and transform it into a list of ordered
    # coordinates

    x = [];
    y = []
    for i in paths[0]:
        x.append(points[i][0])
        y.append(points[i][1])

    plt.plot(x, y, 'co')

    # Set a scale for the arrow heads (there should be a reasonable default for this, WTF?)
    a_scale = float(max(x)) / float(100)

    # Draw the older paths, if provided
    if num_iters > 1:

        for i in range(1, num_iters):

            # Transform the old paths into a list of coordinates
            xi = [];
            yi = [];
            for j in paths[i]:
                xi.append(points[j][0])
                yi.append(points[j][1])

            plt.arrow(xi[-1], yi[-1], (xi[0] - xi[-1]), (yi[0] - yi[-1]),
                      head_width=a_scale, color='r',
                      length_includes_head=True, ls='dashed',
                      width=0.001 / float(num_iters))
            for i in range(0, len(x) - 1):
                plt.arrow(xi[i], yi[i], (xi[i + 1] - xi[i]), (yi[i + 1] - yi[i]),
                          head_width=a_scale, color='r', length_includes_head=True,
                          ls='dashed', width=0.001 / float(num_iters))

    # Draw the primary path for the TSP problem
    plt.arrow(x[-1], y[-1], (x[0] - x[-1]), (y[0] - y[-1]), head_width=a_scale,
              color='g', length_includes_head=True)
    for i in range(0, len(x) - 1):
        plt.arrow(x[i], y[i], (x[i + 1] - x[i]), (y[i + 1] - y[i]), head_width=a_scale,
                  color='g', length_includes_head=True)

    # Set axis too slitghtly larger than the set of x and y
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()


if __name__ == '__main__':
    # Run an example

    # Create a randomn list of coordinates, pack them into a list
    x_cor = [1, 8, 4, 9, 2, 1, 8]
    y_cor = [1, 2, 3, 4, 9, 5, 7]
    points = []
    for i in range(0, len(x_cor)):
        points.append((x_cor[i], y_cor[i]))

    # Create two paths, teh second with two values swapped to simulate a 2-OPT
    # Local Search operation
    path4 = [0, 1, 2, 3, 4, 5, 6]
    path3 = [0, 2, 1, 3, 4, 5, 6]
    path2 = [0, 2, 1, 3, 6, 5, 4]
    path1 = [0, 2, 1, 3, 6, 4, 5]
    path11 = [0, 2, 1, 3]
    path12 = [0, 6, 4, 5]
    # Pack the paths into a list
    # paths = [path1, path2, path3, path4]
    paths = [path11, path12]
    # Run the function
    plotTSP(paths, points, 2)