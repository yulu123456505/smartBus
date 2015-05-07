from random import *
from math import *
from cluster import *
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

class bus(object):
    __location = (0, 0)   #公交车的位置
    __bus_angle = uniform(0, pi)   #公交车的角度，北偏东X度
    __people_num = 1    #车上人的数量
    __length = 10.2    #公交车的长度
    __width = 2.5    #公交车的宽度
    __seat_location = [[x*0.5, y+0.5] for x in range(-2, 3) if x !=0 for y in range(-5, 5)]    #公交车上座位的位置
    __seat_with_passenger = []    #有乘客的座位位置
    __passenger_location = []    #公交车上乘客的位置
    __GPS_accuracy = 30
    aaa = [[x*0.5, y+0.5] for x in range(-2, 3) if x !=0 for y in range(-5, 5) if y != 0]

    def __init__(self, location=(randrange(1000), randrange(1000)), people_num = randrange(1, 40), bus_angle = 0):
        self.__location = location
        if people_num > 40:
            people_num = 40
        elif people_num < 1:
            people_num = 1
        self.__people_num = people_num
        self.__seat_with_passenger = sample(self.__seat_location, self.__people_num)
        if bus_angle > 360:
            bus_angle = 360
        elif bus_angle < 0:
            bus_angle = 0
        self.__bus_angle = bus_angle
        self.calculate_passenger_location()

    def calculate_passenger_location(self):
        self.__passenger_location = [[x*cos(self.__bus_angle)+y*sin(self.__bus_angle), y*cos(self.__bus_angle)-x*sin(self.__bus_angle)] for x, y in self.__seat_with_passenger]

    def getGPS(self):
        L = []
        for x, y in self.__passenger_location:
            r = randrange(self.__GPS_accuracy)
            theta = uniform(0, pi)
            L.append([self.__location[0]+x+r*sin(theta), self.__location[1]+y+r*cos(theta)])
        return L

