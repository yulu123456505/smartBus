from functools import reduce
from para import predicted_buses

def cluster(people_location, precision=40):
    points = [location for pid, location in people_location]
    p_ids = [p_id for p_id, location in people_location]
    flag = [0 for x in range(len(points))]
    cluster_center = []
    cluster_points = []
    buses = []
    for i, point in enumerate(points):
        #print(p_ids[i], point, flag[i])
        if flag[i] == 0:
            center_point = [-1, -1]
            shift_point = point
            while center_point != shift_point:
                center_point = shift_point
                p = [[t, x] for t, x in enumerate(points) if flag[t] != 1 and abs(center_point[0] - x[0]) <= precision and abs(center_point[1] - x[1]) <= precision]    #先缩小范围在方形区域
                p = [[t, x] for t, x in p if abs(center_point[0] - x[0])**2 + abs(center_point[1] - x[1])**2 <= precision**2]    #再在方形区域中计算是不是在圆内
                vector = [[x[0]-center_point[0], x[1]-center_point[1]] for i, x in p]
                if len(vector) == 1:
                    shift_point = vector[0]
                else:
                    shift_point = reduce(lambda x, y: [x[0]+y[0], x[1]+y[1]], vector)
                shift_point = [center_point[0]+shift_point[0]/len(p), center_point[1] + shift_point[1]/len(p)]

            cluster_center.append(center_point)
            for n, x in p:
                flag[n] = 1
            this_cluster_points = [[p_ids[n], x] for n, x in p]
            cluster_points.append(this_cluster_points)
            buses.append([center_point, [p_ids[n] for n, x in p]])
    return cluster_points, cluster_center, buses

def dynamic_cluster(people_location, precision=40):
    print(len(people_location), "people_location", people_location)
    this_cluster_points = []
    this_cluster_center = []
    this_buses = []
    for bus in predicted_buses:
        to_cluster = [[pid, location] for pid, location in people_location if pid in bus[1]]
        list(map(lambda x:people_location.remove(x), to_cluster))
        t_cluster_points, t_cluster_center, t_buses = cluster(to_cluster, precision)
        this_cluster_points = this_cluster_points + t_cluster_points
        this_cluster_center = this_cluster_center + t_cluster_center
        this_buses = this_buses + t_buses
    print(len(people_location), "people_location", people_location)
    print(len(this_buses),len(this_cluster_center),len(this_cluster_points))
    temp_people = []
    for p in people_location:
        for i, location in enumerate(this_cluster_center):
            if is_in_cluster(p[1], location, precision):
                this_cluster_points[i].append(p)    #把人加入对应的公交车上
                this_buses[i][1].append(p[0])    #把乘客编号加入对应的公交车上
                temp_people.append(p)
    try:
        list(map(lambda x:people_location.remove(x), temp_people))    #删掉加入聚类中心的点
    except(ValueError):
        print(len(temp_people),"temp_people",temp_people)
        print(len(people_location),"people:",people_location)
    t_cluster_points, t_cluster_center, t_buses = cluster(people_location, precision)
    this_cluster_points = this_cluster_points + t_cluster_points
    this_cluster_center = this_cluster_center + t_cluster_center
    this_buses = this_buses + t_buses
    l = len(predicted_buses)
    for i in range(l):
        predicted_buses.remove(predicted_buses[0])
    list(map(lambda x:predicted_buses.append(x), this_buses))
    return this_cluster_points, this_cluster_center, this_buses

def is_in_cluster(new_point, cluster_center, precision):
    if abs(new_point[0]-cluster_center[0])**2+abs(new_point[1]-cluster_center[1])**2 <= precision**2:
        return True
    else:
        return False