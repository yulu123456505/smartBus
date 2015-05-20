from random import *
from cluster import *
from estimateBus import bus
from person import person
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from para import people_idle, stable_buses, unstable_buses
from math import pi
import time

def print_info():
    print("***********************stable************************")
    print(len(stable_buses))
    for s_bus in stable_buses:
        print(s_bus.s_id, s_bus.location, s_bus.people)
    print("***********************unstable************************")
    for us_bus in unstable_buses:
        print(us_bus.us_id, us_bus.location, us_bus.people)
    print('***********undetermined*******************')
    for u in undetermined:
        print(u)
    # print("***********************准确率****************************")
    for bus in bus_list:
        p = bus.getPassengerID()
        if p:
            count = 0
            for s_bus in stable_buses:
                t = [x for x in p if x in s_bus.people]
                if len(t) > count:
                    count = len(t)
                    t_p = t
                    s=s_bus.people
            for us_bus in unstable_buses:
                t = [x for x in p if x in us_bus.people]
                if len(t) > count:
                    count =len(t)
                    t_p = t
                    s=us_bus.people
            # print(bus.getID(), count/len(p))
            bus.percent.append(count/len(s))
    #     else:
    #         print(bus.getID(), "该公交车上没有人")

if __name__ == '__main__':
    L=[]
    for i in range(1, 501):
        people_idle.append(person(i))
    #people_idle = people

    map_width = 20
    map_height = 20
    bus_num = 20
    bus_ids = sample(range(1, 1000), bus_num)
    bus_list = []
    for i in range(bus_num):
        a = bus(bus_ids[i], (randrange(map_width), randrange(map_height)))
        a.percent = []
        a.on_bus(randrange(1, 20))
        bus_list.append(a)
        L = a.getGPS()+L

    dynamic_cluster2(L, precision=40)
    print_info()
    count = 0

    stable_count = []
    unstable_count = []
    stable_and_unstable = []
    for i in range(100):
        count += 1
        L = []
        print("******************", i, "************************")
        for a in bus_list:
            if count % 5 == 0:
                a.on_bus(randrange(1, 5))
                a.off_bus(randrange(1, 5))
            a.move(100, uniform(0, 2*pi))
            L = a.getGPS() + L

        dynamic_cluster2(L, precision=40)
        print_info()
        stable_count.append(len(stable_buses))
        unstable_count.append(len(unstable_buses))
        stable_and_unstable.append(len(stable_buses)+len(unstable_buses))
    # for bus in bus_list:
    #     plt.plot(bus.percent)
    # plt.ylim(0, 1)

    plt.plot(stable_count)
    plt.plot(unstable_count)
    plt.plot(stable_and_unstable)
    plt.show()








