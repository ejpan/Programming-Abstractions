"""
Module: earthquake_clusters

A program to create and visualize clusters of earthquakes.

Authors:
1) Long Pham - longpham@sandiego.edu
2) Eric Pan - epan@sandiego.edu
"""

import sys
import math
import matplotlib.pyplot as pp
import imageio

def euclidean_distance(point1, point2):
    """
    Returns the euclidean distance between point1 and point2.
    point1 and point2 are tuples of length 2.
    """
    # Calculates the distance between two points using pythagoras theorem
    # Uses the x and y values of the points
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def get_close_points(p, epsilon, data):
    """
    Returns a list of all the points in the dataset data 
    that are the within epsilon of p.
	"""

    # Initializes a list and iterates through the dataset. 
    # Checks to see if the point in the dataset is within the boundary.
    # of the point p and if so add the point to the list.
    points_list = []

    for key in data.keys():
        if key == p:
            continue
        if euclidean_distance(key, p) < epsilon:
            points_list.append(key)
    return points_list

def add_to_cluster(points, cluster_num, data, epsilon, min_pts):
    """
    Does not return anything but adds a list of points to the
    desired cluster. Uses the get_close_points method and
    add_to_cluster recursively.
    """
    # Iterate through a list of points.
    # Points within epsilon of each other should be added to cluster_num.
    for p in points:
        if data[p] == None or data[p] == -1:
            data[p] = cluster_num
            close_points = get_close_points(p, epsilon, data)
            # Checks to see if there are a minimum number of points within epsiolon of point p.
            # If so, call add_to_cluster recursively until there are no more points to be added.
            if len(close_points) >= min_pts:
                add_to_cluster(close_points, cluster_num, data, epsilon, min_pts)

def dbscan(data, epsilon, min_pts):
    """
    Iterates through the data dictionary and creates a new cluster,
    adding new points to the cluster and identifying outliers.
    Uses get_close_points and add_to_cluster.
    """
    # Set the cluster number to 0 and iterate through the data in the dictionary.
    cluster_num = 0
    for key in data.keys():
        # Check to see if the data has not been assigned to a cluster number yet.
        if data[key] == None:
            close_points = get_close_points(key, epsilon, data)
            # Check to see if the point has enough points around it so that the point
            # can be considered as part of a cluster or an outlier.
            if len(close_points) < min_pts:
                data[key] = -1
            else:
                data[key] = cluster_num
                add_to_cluster(close_points, cluster_num, data, epsilon, min_pts)
                # Increase the cluster number for each new cluster.
                cluster_num += 1
    # Return the total number of clusters in the data.
    return cluster_num

def get_clusters(data, num_clusters):
    """
    Returns a list of clusters where each element is a list of points in the cluster.
    """
    # Initialize a dictionary where the values are a list of points in their respective clusters.
    id = {}
    clusters = []
    # Iterate through the data dictionary and check if the data points are assigned to a valid cluster number.
    for key in data.keys():
        if data[key] <= num_clusters-1 and data[key] != -1:
            # If the value for the data point is not in the id dictionary yet, create a new key for the cluster
            # number and create a value which is a new list for the points within the cluster. Otherwise, append
            # the point to the list.
            if data[key] not in id:
                id[data[key]] = [key]
            else:
                id[data[key]].append(key)
    # Create a list of clusters
    clusters = [list(value) for value in id.values()]
    return clusters

def plot_clusters(clusters):
    """
    Plot clusters containing coordinate points using matplotlib.pyplot.
    """

    #Makes a list containing x coordinates and a list containing y coordinates.
    for cluster in clusters:
        x_coords = list()
        y_coords = list()
        for point in cluster:
            x_coords.append(point[0])
            y_coords.append(point[1])
        #Plots the coordinate points
        pp.scatter(x_coords, y_coords)

def get_eq_locations(filename):
    """
    Gets earthquake location given by filename containing longitude and latitude for each earthquake. 
    """

    #Opens and reads file.
    file = open(filename, 'r')
    lines = file.readlines()
    eq_list = []
    #Gets the longitude and latitude for each earthquake in the file
    #in the format of (longitude, latitude).
    for line in lines[1:]:
        eq_split = line.split(",")
        point = (float(eq_split[2]), float(eq_split[1]))
        #All coordinate points of earthquake is added to a list.
        eq_list.append(tuple(point))
    return eq_list

def initialize_database(locations):
    """
    Creates the intial dataset by making a dictionary with the coordinate points as the key
    and the value assigned as None.
    """
    database = {}
    #Assigns None for each coordinate point as key.
    for point in locations:
        database[tuple(point)] = None
    return database

def plot_earthquakes(filename):
    """
    Creates clusters of earthquakes from the data contained in filename and
    displays them on a world map.
    """

    print("Creating and visualizing clusters from file: %s" % filename)

    # To Do: Use the functions you wrote above to complete the following 5
    # steps. Delete this comment when you are done.

    # Step 1: Gets a list of all of the earthquake locations.
    # Step 2: Initializes the data dictionary.
    # Step 3: Use dbscan to create clusters.
    # Step 4: Get the list of created clusters.
    # Step 5: Plot the clusters.
    epsilon = 2.0
    min_pts = 4
    eq_list = get_eq_locations(filename)
    eq_dict = initialize_database(eq_list)
    cluster_count = dbscan(eq_dict, epsilon, min_pts)
    clusters = get_clusters(eq_dict, cluster_count)
    plot_clusters(clusters)

    # Set the image background to be a world-map
    # Don't change anything after this point.
    img = imageio.imread("world-map-full.jpg")
    pp.imshow(img, zorder=0, extent=[-180, 180, -90, 90])
    pp.axis('off')
    pp.show()


if __name__ == "__main__":
    # Choose the input file
    choice = input("Enter 1 (for eq_day.csv) or 2 (for eq_week.csv): ")

    # Create the clusters and plot the data.
    if choice == "1":
        plot_earthquakes("eq_day.csv")
    elif choice == "2":
        plot_earthquakes("eq_week.csv")
    else:
        print("Invalid choice")