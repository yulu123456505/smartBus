__author__ = 'Steven'
import pymysql
from calDis import calDis_segment2rect
from para import stable_buses, unstable_buses

def connDB(): #连接数据库函数
    conn=pymysql.connect(host='localhost', user='root', passwd='123456', db='businquire', charset='utf8')
    cur=conn.cursor()
    return (conn,cur)

def exeUpdate(conn, cur, sql): #更新语句，可执行update,insert语句
    sta=cur.execute(sql)
    conn.commit()
    return(sta)

def exeInsert(conn, cur, data): #更新语句，可执行update,insert语句
    sta=cur.execute("insert into rawdata (idPhone, timeStamp, accelerometer_x, accelerometer_y, accelerometer_z,gravity_x, gravity_y, gravity_z, gyroscope_x, gyroscope_y, gyroscope_z, magnetic_x, magnetic_y, magnetic_z, stationID, stationSignalTime, wifiID, wifiIntensity, GPS_x, GPS_y, GPS_z)  values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
    conn.commit()
    return(sta)

def exeQuery(cur, sql): #查询语句
    cur.execute(sql)
    return (cur.fetchall())

def connClose(conn, cur): #关闭所有连接
    cur.close()
    conn.close()

def saveAllData(allData):
    conn, cur = connDB()
    sta = exeInsert(conn, cur, allData)
    connClose(conn, cur)
    if(sta == 1):
        #print("success")
        return 1
    else:
        print("it occurs problems when insert ", allData, "into database")
        return 0
def readLatestData():
    conn,cur =connDB()
    sql = "select * from rawdata order by idRawData desc limit 1"
    r = exeQuery(cur,sql)
    connClose(conn,cur)
    return r[0]


#地图网格化，参数：经度分割数量，纬度分割数量，GPS精度
def mapGrid(Longitude_num, Latitude_num, GPS_accuracy):
    conn,cur =connDB()
    sql = "delete from maparea"    #删除原有的所有记录
    cur.execute(sql)
    conn.commit()
    sql = "select max(startPoint_x),min(startPoint_x),max(startPoint_y),min(startPoint_y),max(endPoint_x),min(endPoint_x),max(endPoint_y),min(endPoint_y) from busline"
    r = exeQuery(cur,sql)
    r = r[0]
    #计算经度纬度的最大最小值
    Longitude_max = max(r[0], r[4])+0.0005
    Longitude_min = min(r[1], r[5])-0.0005
    Latitude_max = max(r[2], r[6])+0.0005
    Latitude_min = min(r[3], r[7])-0.0005
    Longitude_step = (Longitude_max - Longitude_min)/Longitude_num
    Latitude_step = (Latitude_max - Latitude_min)/Latitude_num

    sql = "select * from busline"
    cur.execute(sql)
    r = cur.fetchall()
    for n in range(Latitude_num):
        for m in range(Longitude_num):
            lineID  = []
            routeID = []
            upleft_x = Longitude_min+m*Longitude_step
            upleft_y = Latitude_min+(n+1)*Latitude_step
            downright_x = Longitude_min+(m+1)*Longitude_step
            downright_y = Latitude_min+n*Latitude_step
            for line in r:
                dis = calDis_segment2rect(line[1], line[2], line[3], line[4], upleft_x, upleft_y, downright_x, downright_y)
                if calDis_segment2rect(line[1], line[2], line[3], line[4], upleft_x, upleft_y, downright_x, downright_y) <= GPS_accuracy:
                    '''线段到区域的距离小于GPS精度'''
                    if line[0] not in lineID:
                        lineID.append(line[0])
                    for s in line[5].split(','):
                        if s not in routeID:
                            routeID.append(s)
            lineID = [str(x) for x in lineID]
            data = (upleft_x,upleft_y,downright_x,downright_y,','.join(lineID),','.join(routeID))
            data = [str(x) for x in data]
            sta=cur.execute("insert into maparea (upleft_x,upleft_y,downright_x,downright_y,linesContained,routeContained) values(%s,%s,%s,%s,%s,%s)", data)
            conn.commit()

    connClose(conn,cur)

#搜索给定GPS坐标可能的在的路径和线路
def searchRouteByRegion(GPS_x, GPS_y):
    conn,cur =connDB()
    sql = "select linesContained,routeContained from maparea where %s >= upleft_x and %s <= downright_x and %s <= upleft_y and %s >= downright_y and linesContained != ''"
    cur.execute(sql, (GPS_x,GPS_x,GPS_y,GPS_y))
    r = cur.fetchall()
    lines = []
    for i in (','.join([x[0] for x in r])).split(','):
        if i not in lines:
            lines.append(i)
    routes = []
    for i in (','.join([x[1] for x in r])).split(','):
        if i not in routes:
            routes.append(i)
    connClose(conn,cur)
    return ','.join(lines), ','.join(routes)

#通过线段id搜索线段的起始点坐标，返回
def searchSegmentById(segment_id):
    conn,cur =connDB()
    sql = "select * from busline where idbusLine = %s"
    cur.execute(sql,(segment_id,))
    r = cur.fetchall()
    connClose(conn,cur)
    return r[0]

#搜索线路上公交车的位置
def searchRouteLocation(routeID):
    locations1 = [s_bus.location for s_bus in stable_buses if routeID in s_bus.routes]
    locations2 = [us_bus.location for us_bus in unstable_buses if routeID in us_bus.routes]
    return locations1+locations2

#读取所有区域的信息
def readAllRegionInfo():
    conn,cur =connDB()
    sql = "select * from maparea"
    cur.execute(sql)
    r = cur.fetchall()
    connClose(conn,cur)
    return r

#读取所有线段的信息
def readAllLineInfo():
    conn,cur =connDB()
    sql = "select * from busline"
    cur.execute(sql)
    r = cur.fetchall()
    connClose(conn,cur)
    r = [[str(s[0]), [s[0], s[1], s[2], s[3], s[4], s[5]]] for s in r]
    return dict(r)

#读取所有路线的信息
def readAllRouteInfo():
    conn,cur =connDB()
    sql = "select * from busroute"
    cur.execute(sql)
    r = cur.fetchall()
    connClose(conn,cur)
    r = [[str(s[0]), s[2]] for s in r]
    return dict(r)

if __name__=='__main__':
    #data = ('xiaomi', '20150415', 1.23434245, 1.45245, 1.245, 1.2452, 1.245252, 1.2452, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0)
    #sta = saveAllData(data)
    #data = readLatestData()
    #print(data)
    mapGrid(15,15,15)
    # r = searchRouteByRegion(114.374571,30.547172)
    # print(r)
    # r = searchSegmentById(22)
    # print(r)
    # r = readAllRegionInfo()
    # print(r)
    # r = readAllLineInfo()
    # print(r['1'])

