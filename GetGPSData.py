# -*- coding: utf-8 -*-
__author__ = 'Tree'
import csv
from random import *
from math import *
from cluster import dynamic_cluster2, dynamic_cluster
from DataTransform import searchSegmentById, searchRouteLocation, readAllRegionInfo, readAllLineInfo, readAllRouteInfo
from temp import maparea, buslines, busroutes
from process import print_info
#从CSV文件中获取并模拟GPS数据
people = [[id+1, (randrange(0, 60), randrange(70, 134))] for id in range(10)]

def GetGPSData():
    #打开文件
    with open('1.csv',newline='') as csvfile:
            reader = csv.reader(csvfile,delimiter=':', quotechar='|')
            #打开2号文件，查询时间，将整十数据和1号文件整十数据合并
            csvfile2 = open('2.csv',newline='')
            reader2 = csv.reader(csvfile2,delimiter=':', quotechar='|')
            count =1
            time = -1
            result = []
            for row in reader:
                a = row[0].split(',')
                #判断时间的第11位是否为0，如果为0说明是整10s,判断当前时间是否和上一个整10相同，如果相同则跳过
                if (a[19]!="") and (a[0][11:12]=="0" and time!=float(a[0][10:12])):
                    #取第10、11位字符串，即秒数s
                    time = float(a[0][10:12])
                    # print(time)
                    #获取采到的数据
                    location1 = a[20:18:-1]
                    location1 = [float(x) for x in location1]
                    result.append([location1])
                    #dynamic_cluster2(L, 40)
                    #print_info()
                    # print('**********大循环公交的位置************')
                    #print(searchRouteLocation('1'))
            #print(result)
            time = -1
            i = 0
            for row2 in reader2:
                a2 = row2[0].split(',')
                #判断时间的第11位是否为0，如果为0说明是整10s,判断当前时间是否和上一个整10相同，如果相同则跳过
                if (a2[19]!="") and (a2[0][11:12]=="0" and time!=float(a2[0][10:12])):
                    #取第10、11位字符串，即秒数
                    time = float(a2[0][10:12])
                    # print(time)
                    #获取采到的数据
                    location2 = a2[19:17:-1]
                    location2 = [float(x) for x in location2]
                    #如果第二个文件超出第一个文件大小，则不添加了
                    if(i>=len(result)):
                        break
                    result[i].append(location2)
                    #模拟多用户数据
                    #L = CreateUserData(location1,location2,10)
                    i = i+1
    csvfile.close()
    csvfile2.close()
    return result

#对GPS数据进行批量模拟
def GPSDataProcess(result):
    count = 0
    for ls in result:
        if(len(ls) == 2):
            L = []
            for p in people:
                if p[1][0] <= count <=p[1][1]:
                    x1, y1 = ls[0]
                    theta = uniform(0, 2*pi)#产生0～2pi之间的随机数
                    x1 = x1 + 0.0001 * cos(theta)
                    y1 = y1 + 0.0001 * sin(theta)
                    a = [p[0],[x1,y1]]
                    L.append(a)
            count += 1
            dynamic_cluster(L, 110)
            print_info()
            print('**********大循环公交的位置************')
            print(searchRouteLocation('1'))

#模拟产生用户数据
def CreateUserData(location1,location2,userNumber):
    x1,y1 = location1
    x2,y2 = location2
    i = 0
    result = []
    while(i<userNumber):
        theta = uniform(0, 2*pi)#产生0～2pi之间的随机数
        x1 = x1 + 0.0001 * cos(theta)
        y1 = y1 + 0.0001 * sin(theta)
        i=i+1
        result.append([i,[x1,y1]])#将产生的10个数据加入list
    i=0
    if(x2,y2 != -1,-1):
        while(i<userNumber):
            theta = uniform(0, 2*pi)#产生0～2pi之间的随机数
            x2 = x2 + 0.0001 * cos(theta)
            y2 = y2 + 0.0001 * sin(theta)
            i=i+1
            result.append([i+userNumber,[x2,y2]])#将产生的10个数据加入list
    # print(result)
    return result



if __name__ == '__main__':
    for i in readAllRegionInfo():
        maparea.append(i)
    buslines.update(readAllLineInfo())
    busroutes.update(readAllRouteInfo())
    print(busroutes)
    GPSDataProcess(GetGPSData())