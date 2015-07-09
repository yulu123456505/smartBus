__author__ = 'Steven'
from datetime import datetime,timedelta
import csv
from random import *


class SimulateBus(object):
    def __init__(self, routeID, startTime=0, period=10, peopleNum=10, pid_base=0):
        """init the simulate bus with some parameter

        Args:
            routeID: id of the route that the simulate bus is on. The id determine which data file to
                    read as the bus's data.
            startTime: the bus start at the time. so the timestamp in the data file changed by the time.
                    the variable should be a int num, indicate the seconds that the bus start.
                    example:  20
            period(seconds):  the period of cluster. the server will cluster the bus each period.
            peopleNum: the num of people when the bus start
            pid_base: a num, the pid of the people in this bus will plus the pid_base
        """
        self.randomData = []
        self.periodData = []
        self.routeID = routeID
        self.startTime = startTime
        self.period = period
        self.peopleNum = peopleNum
        self.pid_base = pid_base

        self.dataNeedOnePeriod = 10

        if routeID == 1:
            filename = '1.csv'
        else:
            filename = ''
        self.originData = []
        initTime = datetime(2015, 1, 1, 0, 0, 0)
        timeSpan = timedelta(seconds=startTime)
        if filename != '':
            with open('1.csv',newline='') as csvfile:
                reader = csv.reader(csvfile,delimiter=':', quotechar='|')
                for row in reader:
                    a = row[0].split(',')
                    time = datetime(2015, 1, 1, int(a[0][6:8]), int(a[0][8:10]), int(a[0][10:12]))
                    # print(time)
                    #获取采到的数据
                    location1 = a[20:18:-1]
                    # location2 = a[22:20:-1]
                    location1 = [float(x) for x in location1]
                    # location2 = [float(x) for x in location2]
                    self.originData.append([time, location1])
            csvfile.close()
        absTime = self.originData[0][0] - initTime
        for d in self.originData:
            d[0] = d[0] - absTime + timeSpan

    stopPoints = []    #记录该车的停车点和停车时间
    def stop(self, stopPoint, stopTime):
        """add a stop action, the simulate bus will stop stopTime seconds at stopPoint

        the stopPoint and stopTime will recorded in the stopPoints list.

        Args:
            stopPoint: the time point that the bus will stop from the bus start.eg. 10
            stopTime: the duration that the bus stop this time. eg. 10
        """
        times = [t[0] for t in self.stopPoints]
        if stopPoint not in times:
            self.stopPoints.append([stopPoint, stopTime])
            self.stopPoints.sort()

    # deliverData = []    #可以传输的数据
    randomData = []    #随机时刻的数据
    periodData = []    #整周期的数据
    def generateData(self):
        """generate the deliver data by file data and the stop points

        the final data will recorded in the deliverData list.
        """
        tempData = []
        realStopPoints = []   #记录增加了停车时间以后,公交车停车的时间点
        if self.originData:
            startTime = self.originData[0][0]
            cur = 0
            totalSpan = timedelta(seconds=0)
            if self.stopPoints:
                for s in self.stopPoints:
                    span = timedelta(seconds=s[0])
                    while cur < len(self.originData) and startTime+span > self.originData[cur][0]:
                        tempData.append([self.originData[cur][0]+totalSpan, self.originData[cur][1]])
                        cur += 1
                    for i in range(1, s[1]+1):
                        span2 = timedelta(seconds=i)
                        for j in range(0, 5):
                            tempData.append([self.originData[cur-1][0]+totalSpan+span2, self.originData[cur-1][1]])
                    realStopPoints.append(self.originData[cur-1][0]+totalSpan)
                    totalSpan += timedelta(seconds=s[1])
            while cur < len(self.originData):
                tempData.append([self.originData[cur][0]+totalSpan, self.originData[cur][1]])
                cur += 1
        # for k in tempData:
        #     print(k[0], k[1])

        if tempData:
            lastChangeTime = tempData[0][0]
            lastLocation = tempData[0][1]
            lastPeriodData = None
            lastPeriodRealTime = None
            lastPeriodTime = None
            initTime = datetime(2015, 1, 1, 0, 0, 0)
            t_data = []    #临时保存一个周期内的数据
            for d in tempData:
                if realStopPoints and realStopPoints[0] <= d[0]:
                    self.peopleNum = randrange(5, 10)
                    realStopPoints.remove(realStopPoints[0])
                if d[1] != lastLocation:
                    lastLocation = d[1]
                    lastChangeTime = d[0]
                if (d[0] - initTime).total_seconds() % self.period == 0 and d[0] != lastPeriodRealTime:
                    '''整周期初是从initTime开始的整period倍数'''
                    if lastPeriodData:
                        while(len(t_data)<self.peopleNum):
                            '''保证t_data中的数据数量比车上的人数多'''
                            t_data *= 2
                        t_data = sample(t_data, self.peopleNum)
                        for i in range(1, self.peopleNum+1):
                            self.randomData.append([i+self.pid_base, t_data[i-1][0], t_data[i-1][1], t_data[i-1][2]])
                    lastPeriodTime = lastChangeTime
                    lastPeriodRealTime = d[0]
                    lastPeriodData = d[1]
                    for i in range(1, self.peopleNum+1):
                        self.periodData.append([i+self.pid_base, d[1], lastPeriodTime, d[0]])
                    t_data = []   #清空列表5
                else:
                    t_data.append([d[1], lastChangeTime, d[0]])
        # print for test
        # for i in self.randomData:
        #     print(i)
        # print("period")
        # for i in self.periodData:
        #     print(i)


class simulate(object):
    simulateBuses = []
    startTime = None
    endTime = None
    def __init__(self):
        pass

    def addSimulateBus(self, bus):
        """add a simulate bus to the simulateBuses list
        """
        self.simulateBuses.append(bus)
        a = [bus.randomData[0][3], bus.randomData[len(bus.randomData)-1][3]]
        b = [bus.periodData[0][3], bus.periodData[len(bus.periodData)-1][3]]
        tempStartTime = min(a[0], b[0])
        tempEndTime = max(a[1], b[1])
        if not self.startTime:
            self.startTime = tempStartTime
        else:
            self.startTime = min(self.startTime, tempStartTime)

        if not self.endTime:
            self.endTime = tempEndTime
        else:
            self.endTime = max(self.endTime, tempEndTime)


    def init(self):
        """get the startTime and the stopTime in this time simulate from the bus in the simulateBuses
        """
        pass

    def getNext(self):
        """get next data for delivering to the server to cluster or update the bus location

        Returns:
            a list contain the data of random time and the period time.
            example:
                [ [ [pid_random1, location, timestamp], [pid_random2, location, timestamp] ],
                [[pid_period1, location, timestamp], [pid_period2, location, timestamp]] ]
            if return [-1], all data in the simulate have been delivered
        """
        if self.simulateBuses:
            '''如果该模拟器中有添加模拟公交车'''
            oneSecond = timedelta(seconds=1)
            p_data = []
            r_data = []
            if self.startTime <= self.endTime:
                for bus in self.simulateBuses:
                    for p_d in bus.periodData:
                        if p_d[3] == self.startTime:
                            t = p_d[2].strftime('%Y%m%d%H%M%S')
                            p_data.append([p_d[0], p_d[1], t])
                    for r_d in bus.randomData:
                        if r_d[3] == self.startTime:
                            t = r_d[2].strftime('%Y%m%d%H%M%S')
                            r_data.append([r_d[0], r_d[1], t])
                self.startTime = self.startTime + oneSecond
                return [r_data, p_data]
            else:
                self.startTime = self.startTime + oneSecond
                return [-1]


if __name__ == "__main__":
    a = SimulateBus(1, 0, 10, 10)
    a.stop(30, 10)
    # a.stop(40, 10)
    a.generateData()
    s = simulate()
    s.addSimulateBus(a)
    d = s.getNext()
    while d != [-1]:
        # print("random:",d[0])
        print("period:",d[1])

        d=s.getNext()

    # for i in a.originData:
    #     print(i[0], i[1])