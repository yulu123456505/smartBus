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

import csv

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

def getSimulateData(data_type):
    """get simulate buses data presenting different kinds of situation

    Args:
        data_type: the index of the list data which indicate different data
            0:
            1:
            2:
            3:
    """
    data = [
        [#index:0
            [#bus1
                [1,[114.365293,30.540298]],
                [2,[114.365724,30.540594]],
                [3,[114.366236,30.541278]],
                [4,[114.36638,30.541574]],
                [5,[114.366595,30.542312]],
                [6,[114.366685,30.542903]],   #此处开始分开
                [7,[114.365922,30.54351]],
                [8,[114.364817,30.54508]],
                [9,[114.364035,30.546348]],
                [10,[114.36426,30.547957]],
                [11,[114.370368,30.548167]],
                [12,[114.37336,30.546838]],
                [13,[114.374078,30.546814]],    #此处开始合并
                [14,[114.375417,30.547771]],
                [15,[114.376782,30.547631]],
                [16,[114.377312,30.547312]],
                [17,[114.377743,30.546566]],
                [18,[114.37795,30.54543]]
            ],
            [#bus2
                [101,[114.365436,30.540306]],
                [102,[114.365751,30.540508]],
                [103,[114.366308,30.541208]],
                [104,[114.366443,30.541597]],
                [105,[114.366685,30.542328]],
                [106,[114.367125,30.543183]],    #此处开始分开
                [107,[114.367727,30.543525]],
                [108,[114.368805,30.543976]],
                [109,[114.368904,30.545127]],
                [110,[114.36965,30.545679]],
                [111,[114.372434,30.546068]],
                [112,[114.37362,30.54655]],
                [113,[114.374105,30.546768]],    #此处开始合并
                [114,[114.37548,30.547709]],
                [115,[114.376953,30.547553]],
                [116,[114.377339,30.547374]],
                [117,[114.377671,30.546674]],
                [118,[114.377869,30.545477]]
            ]
        ],
        [#index:1
            [#bus1
                [1,[114.365293,30.540298]],
                [2,[114.365724,30.540594]],
                [3,[114.366236,30.541278]],
                [4,[114.36638,30.541574]],
                [5,[114.366595,30.542312]],
                [6,[114.366901,30.54288]],    #此处相遇
                [7,[114.367727,30.543525]],
                [8,[114.368805,30.543976]],
                [9,[114.368904,30.545127]],
                [10,[114.36965,30.545679]],
                [11,[114.372434,30.546068]]
            ],
            [#bus2
                [101,[114.369605,30.545555]],
                [102,[114.368895,30.545135]],
                [103,[114.368859,30.544653]],
                [104,[114.36876,30.544007]],
                [105,[114.367727,30.543494]],
                [106,[114.366955,30.542965]],    #此处相遇
                [107,[114.366748,30.542538]],
                [108,[114.36664,30.542235]],
                [109,[114.366335,30.541441]],
                [110,[114.365931,30.540749]],
                [111,[114.365293,30.540221]]
            ]
        ],
        [#index:2
            [#bus1
                [1,[114.365293,30.540298]],
                [2,[114.365724,30.540594]],
                [3,[114.366236,30.541278]],
                [4,[114.36638,30.541574]],
                [5,[114.366595,30.542312]],
                [6,[114.366901,30.54288]],    #此处追上
                [7,[114.367727,30.543525]],
                [8,[114.368805,30.543976]],
                [9,[114.368904,30.545127]],
                [10,[114.36965,30.545679]],
                [11,[114.372434,30.546068]]
            ],
            [#bus2
                [101,[114.366645,30.542305]],
                [102,[114.366672,30.542445]],
                [103,[114.366744,30.542592]],
                [104,[114.366842,30.542748]],
                [105,[114.366869,30.542771]],
                [106,[114.36695,30.54288]],    #此处被追上
                [107,[114.366995,30.543028]],
                [108,[114.367121,30.543214]],
                [109,[114.367184,30.543269]],
                [110,[114.367372,30.543346]],
                [111,[114.367642,30.543486]]
            ]
        ],
        [#index:3
            [#bus1
                [1,[114.365293,30.540298]],    #前5个点和bus2合并，从大门附近走到教五
                [2,[114.365724,30.540594]],
                [3,[114.366236,30.541278]],
                [4,[114.36638,30.541574]],
                [5,[114.366595,30.542312]],
                [6,[114.366708,30.542903]],    #此处和bus2分开，独自走向计算机学院方向
                [7,[114.36624,30.543214]],
                [8,[114.36607,30.543393]],
                [9,[114.365432,30.544116]],
                [10,[114.365109,30.544746]],
                [11,[114.364471,30.54564]]
            ],
            [#bus2
                [101,[114.365436,30.540306]],    #前5个点和bus1合并，从计算机学院附近走到教五
                [102,[114.365751,30.540508]],
                [103,[114.366308,30.541208]],
                [104,[114.366443,30.541597]],
                [105,[114.366685,30.542328]],
                [106,[114.366914,30.542989]],    #此处和bus1分开，和bus3一起走向樱花大道
                [107,[114.367157,30.543269]],
                [108,[114.36775,30.543556]],
                [109,[114.368253,30.543681]],
                [110,[114.368765,30.543984]],
                [111,[114.368864,30.544684]]
            ],
            [#bus3
                [201,[114.365046,30.544668]],    #前5个点和bus4合并，从计算机学院走到教五
                [202,[114.365252,30.54435]],
                [203,[114.365441,30.544077]],
                [204,[114.365594,30.543914]],
                [205,[114.366223,30.543269]],
                [206,[114.366995,30.542981]],    #此处和bus4分开，和bus2一起走向樱花大道
                [207,[114.367229,30.543222]],
                [208,[114.367813,30.54351]],
                [209,[114.368181,30.543712]],
                [210,[114.368765,30.543945]],
                [211,[114.368908,30.544637]]
            ],
            [#bus4
                [301,[114.364992,30.544645]],    #前5个点和bus3合并，从计算机走到教五
                [302,[114.365261,30.544287]],
                [303,[114.365423,30.544]],
                [304,[114.365594,30.543805]],
                [305,[114.36624,30.543168]],
                [306,[114.36686,30.542616]],    #此处和bus3分开，独自走向大门口
                [307,[114.366618,30.54232]],
                [308,[114.366492,30.541978]],
                [309,[114.366384,30.541558]],
                [310,[114.365746,30.540493]],
                [311,[114.365297,30.540259]]
            ]
        ]
    ]

    if data_type >= len(data):
        return []
    data = data[data_type]
    L = []
    for i in range(len(data[0])):
        s = []
        for k in range(len(data)):
            s.append([k+1,data[k][i][1]])
        L.append(s)
    return L

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

    #222
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

    #333333
    # route = range(12, 17)
    # r = buslines['11']
    # a = bus(999, (r[1],r[2]))
    # a.on_bus(5)
    # for i in route:
    #     r = buslines[str(i)]
    #     a.setLocation((r[1], r[2]))
    #     a.off_bus(1)
    #     print('a车', a.getPassengerID())
    #     print('*****车上人数为',len(a.getPassengerID()),'***************')
    #     L = a.getGPS()
    #     dynamic_cluster2(L, 40)
    #     print_info()
    #     print('**********大循环公交的位置************')
    #     print(searchRouteLocation('1'))
    #     time.sleep(1)
    #
    # route = range(18, 23)
    # r = buslines['17']
    # a.setLocation((r[1], r[2]))
    # for i in route:
    #     r = buslines[str(i)]
    #     a.setLocation((r[1], r[2]))
    #     a.on_bus(1)
    #     print('a车', a.getPassengerID())
    #     print('*****车上人数为',len(a.getPassengerID()),'***************')
    #     L = a.getGPS()
    #     dynamic_cluster2(L, 40)
    #     print_info()
    #     print('**********大循环公交的位置************')
    #     print(searchRouteLocation('1'))

    #444444
    # p = [[id+1, (randrange(0, 3500), randrange(4500, 8066))] for id in range(10)]
    # print(p)
    #
    # with open('1.csv',newline='') as csvfile:
    #     reader = csv.reader(csvfile,delimiter=':', quotechar='|')
    #     count =1
    #     for row in reader:
    #         print(count)
    #         count+=1
    #         a = row[0].split(',')
    #         if a[19]!="":
    #             location = a[20:18:-1]
    #             location = [float(x) for x in location]
    #             L = [[1, location]]
    #             dynamic_cluster2(L, 40)
    #             print_info()
    #             print('**********大循环公交的位置************')
    #             print(searchRouteLocation('1'))
    # csvfile.close()


    #55555
    data = getSimulateData(3)
    for L in data:
        dynamic_cluster2(L, 40)
        print_info()
