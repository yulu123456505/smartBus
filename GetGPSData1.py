# -*- coding: utf-8 -*-
__author__ = 'Tree'
import csv
from random import *
from math import *
from cluster import dynamic_cluster2
from DataTransform import searchSegmentById, searchRouteLocation, readAllRegionInfo, readAllLineInfo, readAllRouteInfo
from temp import maparea, buslines, busroutes
from process import print_info

#从CSV文件中获取并模拟GPS数据
def GetGPSData():
    #打开文件
    with open('1.csv',newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=':', quotechar='|')
            count =1
            time = 0.0
            for row in reader:
                a = row[0].split(',')
                #判断时间的第11位是否为0，如果为0说明是整10s,判断当前时间是否和上一个整10相同，如果相同则跳过
                if (a[19]!="") and (a[0][11:12]=="0" and time!=float(a[0][10:12])):
                    #取第10、11位字符串，即秒数
                    time = float(a[0][10:12])
                    print(time)
                    #获取采到的数据
                    location1 = a[20:18:-1]
                    location2 = a[22:20:-1]
                    location1 = [float(x) for x in location1]
                    location2 = [float(x) for x in location2]
                    #模拟多用户数据
                    L = CreateUserData(location1,location2,10)
                    dynamic_cluster2(L, 100)
                    print_info()
                    print('**********大循环公交的位置************')
                    print(searchRouteLocation('1'))
    csvfile.close()

#模拟产生用户数据
def CreateUserData(location1,location2,userNumber):
    x1,y1 = location1
    x2,y2 = location2
    i = 0
    result = []
    while(i<userNumber):
        theta = uniform(0, pi)#产生0～2pi之间的随机数
        x1 = x1
        y1 = y1
        i=i+1
        result.append([i,[x1,y1]])#将产生的10个数据加入list
    i=0
    while(i<userNumber):
        theta = uniform(0, pi)#产生0～2pi之间的随机数
        x2 = x2
        y2 = y2
        i=i+1
        result.append([i+userNumber,[x2,y2]])#将产生的10个数据加入list
    print(result)
    return result

if __name__ == '__main__':
    for i in readAllRegionInfo():
        maparea.append(i)
    buslines.update(readAllLineInfo())
    busroutes.update(readAllRouteInfo())
    print(busroutes)
    GetGPSData()