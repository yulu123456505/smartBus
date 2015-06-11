from random import *
from cluster import *
from estimateBus import bus
from person import person
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from para import people_idle, stable_buses, unstable_buses
from math import pi
import time
from DataTransform import searchSegmentById, searchRouteLocation, readAllRegionInfo, readAllLineInfo, readAllRouteInfo
from temp import maparea, buslines, busroutes

def print_info():
    print("***********************stable************************")
    for s_bus in stable_buses:
        print(s_bus.s_id, s_bus.location, s_bus.people, s_bus.routes, s_bus.direction, s_bus.line_num)
    print("***********************unstable************************")
    for us_bus in unstable_buses:
        print(us_bus.us_id, us_bus.location, us_bus.people, us_bus.routes, us_bus.direction, us_bus.line_num)
    print('***********undetermined*******************')
    for u in undetermined:
        print(u)
    # print("***********************准确率****************************")
    # for bus in bus_list:
    #     p = bus.getPassengerID()
    #     if p:
    #         count = 0
    #         for s_bus in stable_buses:
    #             t = [x for x in p if x in s_bus.people]
    #             if len(t) > count:
    #                 count = len(t)
    #                 t_p = t
    #                 s=s_bus.people
    #         for us_bus in unstable_buses:
    #             t = [x for x in p if x in us_bus.people]
    #             if len(t) > count:
    #                 count =len(t)
    #                 t_p = t
    #                 s=us_bus.people
    #         # print(bus.getID(), count/len(p))
    #         bus.percent.append(count/len(s))
    #     else:
    #         print(bus.getID(), "该公交车上没有人")

if __name__ == '__main__':
    # L=[]
    for i in range(1, 501):
        people_idle.append(person(i))

    for i in readAllRegionInfo():
        maparea.append(i)
    buslines.update(readAllLineInfo())
    busroutes.update(readAllRouteInfo())
    print(busroutes)
    #people_idle = people
    #
    # map_width = 20
    # map_height = 20
    # bus_num = 20
    # bus_ids = sample(range(1, 1000), bus_num)
    # bus_list = []
    # for i in range(bus_num):
    #     a = bus(bus_ids[i], (randrange(map_width), randrange(map_height)))
    #     a.percent = []
    #     a.on_bus(randrange(1, 20))
    #     bus_list.append(a)
    #     L = a.getGPS()+L
    #
    # dynamic_cluster2(L, precision=40)
    # print_info()
    # count = 0
    #
    # stable_count = []
    # unstable_count = []
    # stable_and_unstable = []
    # for i in range(100):
    #     count += 1
    #     L = []
    #     print("******************", i, "************************")
    #     for a in bus_list:
    #         if count % 5 == 0:
    #             a.on_bus(randrange(1, 5))
    #             a.off_bus(randrange(1, 5))
    #         a.move(100, uniform(0, 2*pi))
    #         L = a.getGPS() + L
    #
    #     dynamic_cluster2(L, precision=40)
    #     print_info()
    #     stable_count.append(len(stable_buses))
    #     unstable_count.append(len(unstable_buses))
    #     stable_and_unstable.append(len(stable_buses)+len(unstable_buses))
    # # for bus in bus_list:
    # #     plt.plot(bus.percent)
    # # plt.ylim(0, 1)
    #
    # plt.plot(stable_count)
    # plt.plot(unstable_count)
    # plt.plot(stable_and_unstable)
    # plt.show()


    # route = range(2, 51)
    # r = buslines['1']
    # a = bus(999, (r[1],r[2]))
    # a.on_bus(20)
    # b = bus(999, (r[1],r[2]))
    # b.on_bus(20)
    # a.setLocation((r[1], r[2]))
    # b.setLocation((r[1], r[2]))
    # L=[]
    # for i in route:
    #     r = buslines[str(i)]
    #     # gps = [[1, [r[1], r[2]]]]
    #     a.setLocation((r[1], r[2]))
    #     b.setLocation((r[1], r[2]))
    #     num = randrange(1, 5)
    #     print('上车人数：',num,'**********')
    #     a.on_bus(num)
    #     b.on_bus(num)
    #     num = randrange(1, 5)
    #     print('下车人数：',num,'**********')
    #     a.off_bus(num)
    #     b.off_bus(num)
    #     print('a车', a.getPassengerID())
    #     print('b车', b.getPassengerID())
    #     print('*****车上人数为',len(a.getPassengerID()),'***************')
    #     L = a.getGPS() + b.getGPS()
    #     dynamic_cluster2(L, 40)
    #     print_info()
    #     print('**********大循环公交的位置************')
    #     print(searchRouteLocation('1'))


    route = range(12, 17)
    r = buslines['11']
    a = bus(999, (r[1],r[2]))
    a.on_bus(5)
    for i in route:
        r = buslines[str(i)]
        a.setLocation((r[1], r[2]))
        a.off_bus(1)
        print('a车', a.getPassengerID())
        print('*****车上人数为',len(a.getPassengerID()),'***************')
        L = a.getGPS()
        dynamic_cluster2(L, 40)
        print_info()
        print('**********大循环公交的位置************')
        print(searchRouteLocation('1'))
        time.sleep(1)

    route = range(18, 23)
    r = buslines['17']
    a.setLocation((r[1], r[2]))
    for i in route:
        r = buslines[str(i)]
        a.setLocation((r[1], r[2]))
        a.on_bus(1)
        print('a车', a.getPassengerID())
        print('*****车上人数为',len(a.getPassengerID()),'***************')
        L = a.getGPS()
        dynamic_cluster2(L, 40)
        print_info()
        print('**********大循环公交的位置************')
        print(searchRouteLocation('1'))













