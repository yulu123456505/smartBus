from random import *
from cluster import *
from estimateBus import bus
from person import person
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from para import people_idle
import time

if __name__ == '__main__':
    L=[]
    for i in range(1, 501):
        people_idle.append(person(i))
    #people_idle = people

    map_width = 1000
    map_height = 1000
    bus_num = 15
    bus_ids = sample(range(1, 1000), bus_num)
    bus_list = []
    for i in range(bus_num):
        a = bus(bus_ids[i], (randrange(map_width), randrange(map_height)))
        a.on_bus(randrange(1, 20))
        bus_list.append(a)
        L = a.getGPS()+L
    #聚类并画图
    cluster_points, center, buses = dynamic_cluster(L, precision=40)
    for i, points in enumerate(center):
        print("****************************************************************")
        print("center:", points, "num: ", len(cluster_points[i]))
        m = 0
        for pid, c in cluster_points[i]:
            print(m, "id=", pid, "location=", c)
            m=m+1
    print(len(center),center)
    print(buses)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    plt.xlim(-100, 1100)
    plt.ylim(-100, 1100)
    for x, y in center:
        cir1 = Circle(xy=(x, y), radius=40, alpha=0.5)
        ax.add_patch(cir1)
    for pid, location in L:
        plt.plot(location[0], location[1], 'b.', markersize=14)
    plt.axis('equal')
    plt.show()

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    L = []
    for a in bus_list:
        a.off_bus(randrange(1, 5))
        a.on_bus(randrange(1, 5))
        L = a.getGPS()+L

    #聚类并画图
    cluster_points, center, buses = dynamic_cluster(L, precision=40)
    for i, points in enumerate(center):
        print("****************************************************************")
        print("center:", points, "num: ", len(cluster_points[i]))
        m = 0
        for pid, c in cluster_points[i]:
            print(m, "id=", pid, "location=", c)
            m=m+1
    print(len(center),center)
    print(buses)
    fig = plt.figure(2)
    ax = fig.add_subplot(111)
    plt.xlim(-100, 1100)
    plt.ylim(-100, 1100)
    for x, y in center:
        cir1 = Circle(xy=(x, y), radius=40, alpha=0.5)
        ax.add_patch(cir1)
    for locations in cluster_points:
        for pid, location in locations:
            plt.plot(location[0], location[1], 'b.', markersize=14)
    plt.axis('equal')
    plt.show()