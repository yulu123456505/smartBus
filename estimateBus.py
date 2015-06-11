from random import sample, randrange, uniform
from math import pi, sin, cos
from para import people_idle, people_on_bus, stable_buses, unstable_buses, undetermined, disappeared
import datetime

class bus(object):
    def __init__(self, bus_id=1, location=(randrange(1000), randrange(1000)), bus_angle = 0):
        self.__bus_id = bus_id
        self.__location = location

        self.__bus_angle = uniform(0, pi)   #公交车的角度，北偏东X度
        self.__people_num = 0    #车上人的数量
        self.__length = 10.2    #公交车的长度
        self.__width = 2.5    #公交车的宽度
        self.__seat_location = [[x*0.5, y+0.5] for x in range(-2, 3) if x !=0 for y in range(-5, 5)]    #公交车上座位的位置
        self.__seat_idle = self.__seat_location    #空闲的座位位置
        self.__seat_with_passenger = []    #有乘客的座位位置
        self.__passenger_location = []    #公交车上乘客的位置
        self.__passenger_on_this_bus = []    #在该公交车上的乘客
        self.__GPS_accuracy = 30

        if bus_angle > 360:
            bus_angle = 360
        elif bus_angle < 0:
            bus_angle = 0
        self.__bus_angle = bus_angle
        self.calculate_passenger_location()

    #上车
    def on_bus(self, people_num=0):
        #上车的人数要小于剩余的座位数和空闲乘客的数量
        if len(self.__seat_idle) < people_num:
            people_num = len(self.__seat_idle)
        if len(people_idle) < people_num:
            people_num = len(people_idle)
        self.__people_num = self.__people_num + people_num    #更新乘客的数量

        new_on_seat = sample(self.__seat_idle, people_num)
        list(map(lambda x: self.__seat_idle.remove(x), new_on_seat))    #新占用的座位从空闲座位中删除
        list(map(lambda x: self.__seat_with_passenger.append(x), new_on_seat))   #新占用的座位加入已有乘客的座位中
        new_on_people = sample(people_idle, people_num)
        #输出新上车的人
        ps = [pid.p_id for pid in new_on_people]
        # print(ps)

        list(map(lambda x:people_idle.remove(x), new_on_people))    #新上车的人从空闲乘客中删除
        list(map(lambda x:people_on_bus.append(x), new_on_people))    #新上车的人加入已上车的乘客中
        self.__passenger_on_this_bus = self.__passenger_on_this_bus + new_on_people
        for i in range(len(new_on_people)):
            new_on_people[i].set_bus_Info(self.__bus_id, new_on_seat[i])

    #下车
    def off_bus(self, people_num=0):
        if people_num >= len(self.__seat_with_passenger):
            people_num = len(self.__seat_with_passenger)
        self.__people_num = self.__people_num - people_num    #更新乘客的数量

        new_off_people = sample(self.__passenger_on_this_bus, people_num)
        list(map(lambda x:people_idle.append(x), new_off_people))    #下车乘客加入空闲乘客列表
        list(map(lambda x:people_on_bus.remove(x), new_off_people))    #下车乘客从在公交上的列表中删除
        list(map(lambda x:self.__passenger_on_this_bus.remove(x), new_off_people))    #下车乘客从该公交上的乘客列表中删除
        new_off_seat = [x.get_bus_Info()[1] for x in new_off_people]
        list(map(lambda x:self.__seat_idle.append(x), new_off_seat))    #座位加入空闲座位
        list(map(lambda x:self.__seat_with_passenger.remove(x), new_off_seat))    #从有乘客的座位中删除
        list(map(lambda x:x.set_bus_Info(0, [0, 0]), new_off_people))    #下车乘客的公交信息设置为0，[0，0]

        #用户下车后需要进行的操作，包括从stablebuses,unstablebuses,undetermined中删除该用户，还有检查是否满足加入disappeared的条件
        t_stable = []
        t_unstable = []
        for p in new_off_people:
            for stable in stable_buses:
                if p.p_id in stable.people:
                    stable.people.remove(p.p_id)
                    if not stable.people:
                        t_stable.append(stable)
                    break
            for un_stable in unstable_buses:
                if p.p_id in un_stable.people:
                    un_stable.people.remove(p.p_id)
                    if not un_stable.people:
                        t_unstable.append(un_stable)
                    break
            t_unde = [u for u in undetermined if u[0] == p.p_id]
            if t_unde:
                undetermined.remove(t_unde[0])

        list(map(lambda x:stable_buses.remove(x), t_stable))
        list(map(lambda x:unstable_buses.remove(x), t_unstable))
        #检查空车是否满足 路线唯一 的条件，满足则加入disappeared
        if t_stable:
            nowtime = datetime.datetime.now()
            for stable in t_stable:
                if len(stable.routes) == 1:
                    stable.lasttime = nowtime    #lasttime记录公交车上一次预测的时间，刚消失时为消失的时间
                    stable.predict_num = 0
                    disappeared.append(stable)




    def move(self, length, angle):
        self.__location = [self.__location[0]+length*cos(angle), self.__location[1]+length*sin(angle)]

    def setLocation(self, location):
        self.__location = location

    def calculate_passenger_location(self):
        self.__passenger_location = [[p.p_id, [p.p_seat_location[0]*cos(self.__bus_angle)+p.p_seat_location[1]*sin(self.__bus_angle), p.p_seat_location[1]*cos(self.__bus_angle)-p.p_seat_location[0]*sin(self.__bus_angle)]] for p in self.__passenger_on_this_bus]

    def getGPS(self):
        self.calculate_passenger_location()
        L = []
        for pid, location in self.__passenger_location:
            x = self.__location[0]
            y = self.__location[1]
            # r = randrange(self.__GPS_accuracy)
            theta = uniform(0, pi)
            x = x + 0.0001 * cos(theta)
            y = y + 0.0001 * sin(theta)
            L.append([pid, [x, y]])
        return L

    def getPassengerID(self):
        return [x.p_id for x in self.__passenger_on_this_bus]

    def getID(self):
        return self.__bus_id

