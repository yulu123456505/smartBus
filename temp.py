maparea = []
buslines = {}
busroutes = {}

bus_speed = 5    #公交车的预测速度
predict_num = 5    #空车持续预测的次数
predict_bus_range = 70    #由于空车的位置预测不准，空车的有效范围比较大，在此范围内的人可以加入该车

def searchRegion(GPS_x, GPS_y):
    a= ''
    b= ''
    for m in maparea:
        if float(m[1]) <= GPS_x <= float(m[3]) and float(m[4]) <= GPS_y <= float(m[2]):
            a = m[5]
            b = m[6]
            break
    return a, b