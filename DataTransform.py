__author__ = 'Steven'
import pymysql

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
    return (cur)

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

if __name__=='__main__':
    data = ('xiaomi', '20150415',1.23434245,1.45245,1.245, 1.2452,1.245252,1.2452, 1.0,1.0,1.0, 1.0,1.0,1.0, 1.0,1.0, 1.0,1.0, 1.0,1.0,1.0)
    sta = saveAllData(data)

