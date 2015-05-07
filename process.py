from random import *
from cluster import *
from estimateBus import bus
from person import person
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

if __name__ == '__main__':
    b=[]
    people = []
    for i in range(1, 201):
        people.append(person(i, [0, 0], 0))
    for i in range(15):
        a = bus((randrange(1000), randrange(1000)), randrange(1, 20))
        b=a.getGPS()+b

    #聚类并画图
    center = cluster(b, precision=35)
    print(len(center),center)
    fig = plt.figure(1)
    ax = fig.add_subplot(111)
    plt.xlim(-100, 1100)
    plt.ylim(-100, 1100)
    for x, y in center:
        cir1 = Circle(xy=(x, y), radius=35, alpha=0.5)
        ax.add_patch(cir1)
    for x, y in b:
        plt.plot(x, y, 'b.', markersize=14)
    plt.axis('equal')
    plt.show()