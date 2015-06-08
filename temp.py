maparea = []
buslines = {}
busroutes = {}

def searchRegion(GPS_x, GPS_y):
    a= ''
    b= ''
    for m in maparea:
        if float(m[1]) <= GPS_x <= float(m[3]) and float(m[4]) <= GPS_y <= float(m[2]):
            a = m[5]
            b = m[6]
            break
    return a, b