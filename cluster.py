from functools import reduce
from para import predicted_buses, stable_buses, unstable_buses, undetermined, disappeared
from stable_bus import stable_bus
from unstable_bus import unstable_bus
from calDis import calDis_point2point, calDis_point2segment
from DataTransform import searchRouteByRegion, searchSegmentById
from temp import maparea,buslines,searchRegion,busroutes, bus_speed, predict_num, predict_bus_range
import itertools
import datetime

def cluster(people_location, precision=40):
    """cluster the bus via the data from people's GPS on a moment

    the function uses mean-shift algorithm which use a circle to enclose as much as people, each iteration adjust the
    center of the circle to find the high-density place until the center is stable.

    Args:
        people_location:a list contains all people's GPS data on a moment with people id and location
            example:
            [ [1, [114.1, 30.5]], [2, [114.2, 30.4]] ]
        precision:the radius of the circle in the mean-shift algorithm which indicate the error of GPS
    Returns:
        cluster_points: a list which contains the people's GPS data in every result
            example:
            [ [[1, [114.36480123305492, 30.533082344631634]],[2, [114.3648302288409, 30.532986640690257]] ]]
        cluster_center: a list which contains the center point of each result
            example:
            [[114.36479491066619, 30.532969549010176]]
        buses: a list which contains the people id in every result
            example:
            [[[114.36479491066619, 30.532969549010176], [1, 2]]]
    """
    points = [location for pid, location in people_location]
    p_ids = [p_id for p_id, location in people_location]
    flag = [0 for x in range(len(points))]
    cluster_center = []
    cluster_points = []
    buses = []
    for i, point in enumerate(points):
        if flag[i] == 0:
            center_point = [-1, -1]
            shift_point = point
            circle_num = 0
            while center_point != shift_point:
                center_point = shift_point
                p = [[t, x] for t, x in enumerate(points) if flag[t] != 1 and calDis_point2point(center_point[0], center_point[1], x[0], x[1]) <= precision]
                vector = [[x[0]-center_point[0], x[1]-center_point[1]] for i, x in p]
                if len(vector) == 1:
                    shift_point = vector[0]
                else:
                    shift_point = reduce(lambda x, y: [x[0]+y[0], x[1]+y[1]], vector)
                shift_point = [center_point[0]+shift_point[0]/len(p), center_point[1] + shift_point[1]/len(p)]
                circle_num += 1
                if circle_num == 20:
                    '''如果循环20次还没结束，则自动结束'''
                    break

            cluster_center.append(center_point)
            for n, x in p:
                flag[n] = 1
            this_cluster_points = [[p_ids[n], x] for n, x in p]
            cluster_points.append(this_cluster_points)
            buses.append([center_point, [p_ids[n] for n, x in p]])
    return cluster_points, cluster_center, buses

def dynamic_cluster(people_location, precision=40):
    """update the location and route of buses dynamically.

    Args:
        people_location:a list contains all people's GPS data on a moment with people id and location
            example:
            [ [1, [114.1, 30.5]], [2, [114.2, 30.4]] ]
        precision:the radius of the circle in the mean-shift algorithm which indicate the error of GPS.
    Returns:
        no return. The function maintains the following global variable:
        stable_buses: a list contains the stable buses.
        unstable_buses: a list contains the unstable buses.
        undetermined: a list contains the people which can't determine which stable buses to join in.
    """
    #每次聚类之前更新空车的位置
    predict_disappear()
    #现有的聚类结果中有，但是本次聚类的数据中没有的乘客，视作已经下车，从聚类结果中删除
    update_off_people(people_location)

    this_stable_buses = []
    this_unstable_buses = []
    this_undetermined = []
    if len(stable_buses) > 0:
        stable_max_id = max([s_bus.s_id for s_bus in stable_buses])    #稳定状态集合的最大id
    else:
        stable_max_id = 0
    for s_bus in stable_buses:
        '''对每一个稳定状态重新聚类'''
        to_cluster = [[pid, location] for pid, location in people_location if pid in s_bus.people]
        t_cluster_points, t_cluster_center, t_buses = cluster(to_cluster, precision+20)
        if len(t_buses) > 1:
            '''稳定状态分裂则都加入不稳定状态'''
            for bus in t_buses:
                pass
        elif len(t_buses) == 1:
            '''没有分裂只更新位置'''
            list(map(lambda x:people_location.remove(x), to_cluster))
            this_stable_buses.append(stable_bus(s_bus.s_id, t_buses[0][0], s_bus.people, s_bus.coincide_bus_count, s_bus.routes, s_bus.line_num, s_bus.direction))

    t_undetermined = [[pid, location, arround_buses] for pid, location in people_location for pid2, arround_buses in undetermined if pid == pid2]
    for u_determine in t_undetermined:
        '''处理待定集合，附近只有一个稳定状态则加入'''
        t_stable1 = [stable for stable in this_stable_buses if stable.s_id in u_determine[2]]
        t_stable2 = [stable for stable in t_stable1 if is_in_cluster(u_determine[1], stable.location, precision)]
        if len(t_stable2) > 1:
            '''多于一个，仍是待定状态，更新t_undetermined'''
            this_undetermined.append([u_determine[0], [bus.s_id for bus in t_stable2]])
            people_location.remove([u_determine[0], u_determine[1]])    #在全集中删除该用户
        elif len(t_stable2) == 1:
            '''附近只有一个稳定状态，则加入'''
            for t_stable_bus in this_stable_buses:
                if t_stable2[0].s_id == t_stable_bus.s_id:
                    t_stable_bus.people.append(u_determine[0])
                    break
            people_location.remove([u_determine[0], u_determine[1]])    #在全集中删除该用户
        elif len(t_stable2) == 0:
            '''附近没有稳定状态，则看作普通新上车的用户'''
            pass

    t_people = []    #保存处理过的用户
    for people in people_location:
        '''处理剩下的用户，即新上车的用户'''
        t_stables = [t_stable for t_stable in this_stable_buses if is_in_cluster(people[1], t_stable.location, precision+20)]
        if len(t_stables) > 1:
            '''附近多于1个稳定状态，进入待定'''
            this_undetermined.append([people[0], [t_stable.s_id for t_stable in t_stables]])
            t_people.append(people)
        elif len(t_stables) == 1:
            '''附近只有一个，加入该稳定状态'''
            for t_stable in this_stable_buses:
                if t_stable.s_id == t_stables[0].s_id:
                    t_stable.people.append(people[0])
                    t_people.append(people)
                    break

    list(map(lambda x:people_location.remove(x), t_people))    #处理过的用户都删掉

    '''最后剩下的用户整体调用聚类算法，所有结果都加入不稳定状态'''
    t_cluster_points, t_cluster_center, t_buses = cluster(people_location, precision)
    for bus in t_buses:
        '''对每一个聚类结果，首先看是否能加入消失的公交车上，如果不能再转为不稳定状态'''
        possible_bus = [d for d in disappeared if calDis_point2point(d.location[0], d.location[1], bus[0][0], bus[0][1])<= predict_bus_range]
        if possible_bus:
            dises = [calDis_point2point(d.location[0], d.location[1], bus[0][0], bus[0][1]) for d in possible_bus]
            min_index = dises.index(min(dises))
            stable_max_id += 1
            this_stable_buses.append(stable_bus(stable_max_id, bus[0], bus[1], [], possible_bus[min_index].routes, possible_bus[min_index].line_num, possible_bus[min_index].direction))
            disappeared.remove(possible_bus[min_index])
        else:
            stable_max_id += 1
            this_stable_buses.append(stable_bus(stable_max_id, bus[0], bus[1]))

    while stable_buses:
        stable_buses.pop()
    list(map(lambda x:stable_buses.append(x), this_stable_buses))
    while undetermined:
        undetermined.pop()
    list(map(lambda x:undetermined.append(x), this_undetermined))

    routeMatch(precision)

def predict_disappear():
    """predict the location the bus in the disappeared

    if all passengers on a stable bus get off, the stable is saved in the disappeared list(a global variable), before
     every cluster, we will predict the location of buses in the list. the speed is bus_speed which is defined in the
     global variable.
    """
    nowtime = datetime.datetime.now()
    t_delete = []
    for d in disappeared:
        if d.predict_num == predict_num:
            '''满足保留次数，加入要删除的集合'''
            t_delete.append(d)
            break
        seconds = (nowtime-d.lasttime).seconds
        d.lasttime = nowtime
        distance = seconds * bus_speed    #计算车辆距离上一次预测行驶的距离
        route = busroutes[d.routes[0]].split(',')   #获取所在路线的线段集合
        line = d.line_num    #获取车辆所在的线段id
        direction = d.direction    #获取车辆的行驶方向

        r = buslines[line]
        end_point = (r[1], r[2]) if direction == -1 else (r[3], r[4])
        while distance - calDis_point2point(d.location[0], d.location[1], end_point[0], end_point[1]) > 0:
            distance = distance - calDis_point2point(d.location[0], d.location[1], end_point[0], end_point[1])
            next_line = [lid for lid in route if lid != line and (buslines[lid][1] == end_point[0] or buslines[lid][3] == end_point[0])]
            if next_line:
                next_line = next_line[0]
                r = buslines[next_line]
                d.location = end_point
                d.line_num = next_line
                d.direction = 1 if end_point[0] == r[1] else -1
                end_point = (r[1], r[2]) if end_point[0] == r[3] else (r[3], r[4])
            else:
                t_delete.append(d)
                break
        if d not in t_delete and d.location != end_point:
            '''利用相似三角形求出线段中点的坐标'''
            line_startpoint = d.location
            line_endpoint = end_point
            try:
                k = distance / calDis_point2point(line_startpoint[0], line_startpoint[1],line_endpoint[0], line_endpoint[1])
            except Exception as e:
                print(e)
            x = line_startpoint[0] + (line_endpoint[0] - line_startpoint[0])*k
            y = line_startpoint[1] + (line_endpoint[1] - line_endpoint[1])*k
            d.location = (x, y)
        d.predict_num += 1
    #从disappeared中删除达到保留次数或已经到达终点站的空车
    list(map(lambda x:disappeared.remove(x), t_delete))

def update_off_people(people_location):
    people_on_bus = [pid for bus in itertools.chain(stable_buses, unstable_buses) for pid in bus.people]
    people_all = [p[0] for p in people_location]
    pid_disappear = [pid for pid in people_on_bus if pid not in people_all]
    if pid_disappear:
        t_stable = []
        t_unstable = []
        for p in pid_disappear:
            for stable in stable_buses:
                if p in stable.people:
                    stable.people.remove(p)
                    if not stable.people:
                        t_stable.append(stable)
                    break
            for un_stable in unstable_buses:
                if p in un_stable.people:
                    un_stable.people.remove(p)
                    if not un_stable.people:
                        t_unstable.append(un_stable)
                    break
            t_unde = [u for u in undetermined if u[0] == p]
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

#判断一个点是不是在已center为中心，precision为半径的范围内
def is_in_cluster(new_point, cluster_center, precision=40):
    """judge if a point is in a circle.

    Args:
        new_point: a list which contain the Longitude and Latitude of the point.
        cluster_center: a list which contain the Longitude and Latitude of the center of circle.
        precision: the radius of the circle.
    Returns:
        true or false.
    """
    if calDis_point2point(new_point[0], new_point[1], cluster_center[0], cluster_center[1]) <= precision:
        return True
    else:
        return False
#动态聚类算法
#输入：所有用户的GPS信息， 定位的精度
def dynamic_cluster2(people_location, precision=40):
    """update the location and route of buses dynamically.

    Args:
        people_location:a list contains all people's GPS data on a moment with people id and location
            example:
            [ [1, [114.1, 30.5]], [2, [114.2, 30.4]] ]
        precision:the radius of the circle in the mean-shift algorithm which indicate the error of GPS.
    Returns:
        no return. The function maintains the following global variable:
        stable_buses: a list contains the stable buses.
        unstable_buses: a list contains the unstable buses.
        undetermined: a list contains the people which can't determine which stable buses to join in.
    """
    #每次聚类之前更新空车的位置
    predict_disappear()

    this_stable_buses = []
    this_unstable_buses = []
    this_undetermined = []
    #stable_max_id和 unstable_max_id为稳定态和不稳定态的id
    #stable_max_id为稳定态id，是偶数，从2开始，2.4.6.8.....
    #unstable_max_id为非稳定态id，是奇数，从3开始，3.5.7.9.....
    if len(stable_buses) > 0:
        stable_max_id = max([s_bus.s_id for s_bus in stable_buses])    #稳定状态集合的最大id
    else:
        stable_max_id = 0
    if len(unstable_buses) > 0:
        unstable_max_id = max([us_bus.us_id for us_bus in unstable_buses])    #不稳定状态集合的最大id
    else:
        unstable_max_id = 1

    continuous_coincide_num = 3
    continuous_stable_num = 3

    for s_bus in stable_buses:
        '''对每一个稳定状态重新聚类'''
        to_cluster = [[pid, location] for pid, location in people_location if pid in s_bus.people]
        list(map(lambda x:people_location.remove(x), to_cluster))
        t_cluster_points, t_cluster_center, t_buses = cluster(to_cluster, precision+20)
        if len(t_buses) > 1:
            '''稳定状态分裂则都加入不稳定状态'''
            for bus in t_buses:
                unstable_max_id = (((unstable_max_id+1)/2))*2+1
                this_unstable_buses.append(unstable_bus(unstable_max_id, bus[0], bus[1], 0, s_bus.routes, s_bus.line_num, s_bus.direction))
        elif len(t_buses) == 1:
            '''没有分裂只更新位置'''
            this_stable_buses.append(stable_bus(s_bus.s_id, t_buses[0][0], s_bus.people, s_bus.coincide_bus_count, s_bus.routes, s_bus.line_num, s_bus.direction))

    for i in range(len(this_stable_buses)):
        '''输出合并次数列表，供调试'''
        #print(this_stable_buses[i].s_id, this_stable_buses[i].coincide_bus_count)

    for i in range(len(this_stable_buses)):
        '''删除coincide_bus_count中不存在的id'''
        t = []    #临时存放要删除的coincide_bus_count
        for bus_id, count in this_stable_buses[i].coincide_bus_count:
            f = False
            for j in range(len(this_stable_buses)):
                if bus_id == this_stable_buses[j].s_id:
                    f = True
                    break
            if not f:
                t.append([bus_id, count])
        list(map(lambda x:this_stable_buses[i].coincide_bus_count.remove(x), t))



    for i in range(len(this_stable_buses)-1):
        for j in range(i+1, len(this_stable_buses)):
            t_coincide1 = [t for t in this_stable_buses[j].coincide_bus_count if t[0] == this_stable_buses[i].s_id]
            t_coincide2 = [t for t in this_stable_buses[i].coincide_bus_count if t[0] == this_stable_buses[j].s_id]
            if len(t_coincide1) == 1 and len(t_coincide2) == 1:
                if is_in_cluster(this_stable_buses[i].location, this_stable_buses[j].location, precision)\
                        and this_stable_buses[i].routes == this_stable_buses[j].routes and len(this_stable_buses[i].routes) == 1:
                    '''如果重合'''
                    a = [t_coincide1[0][0], t_coincide1[0][1]+1]
                    b = [t_coincide2[0][0], t_coincide2[0][1]+1]
                    this_stable_buses[j].coincide_bus_count.remove(t_coincide1[0])
                    this_stable_buses[i].coincide_bus_count.remove(t_coincide2[0])
                    this_stable_buses[j].coincide_bus_count.append(a)
                    this_stable_buses[i].coincide_bus_count.append(b)

                else:
                    this_stable_buses[j].coincide_bus_count.remove(t_coincide1[0])
                    this_stable_buses[i].coincide_bus_count.remove(t_coincide2[0])
            elif len(t_coincide1) == 0 and len(t_coincide2) == 0:
                if is_in_cluster(this_stable_buses[i].location, this_stable_buses[j].location, precision):
                    '''如果重合'''
                    a = [this_stable_buses[i].s_id, 1]
                    b = [this_stable_buses[j].s_id, 1]
                    this_stable_buses[j].coincide_bus_count.append(a)
                    this_stable_buses[i].coincide_bus_count.append(b)

    t_coincide_bus = []    #暂时存放满足要求的稳定状态
    t_coincide_new_bus = []    #暂时存放合并以后的稳定状态
    flag = [0 for i in range(len(this_stable_buses))]
    for i in range(len(this_stable_buses)):
        if flag[i] == 0:
            t = [id for id, count in this_stable_buses[i].coincide_bus_count if count == continuous_coincide_num]
            if t:
                num = [n for n, b in enumerate(this_stable_buses) if b.s_id in t]
                num = num + [i]
                for j in num:
                    flag[j] = 1
                list(map(lambda x:t_coincide_bus.append(this_stable_buses[x]), num))
                stable_max_id = ((stable_max_id/2)+1)*2
                coincide_people = []
                t_routes = []
                for j in num:
                    coincide_people += this_stable_buses[j].people
                    t_routes += this_stable_buses[j].routes
                t_routes = list(set(t_routes))
                t_coincide_new_bus.append(stable_bus(stable_max_id, this_stable_buses[i].location, coincide_people, [], t_routes, this_stable_buses[i].line_num, this_stable_buses[i].direction))
    '''删掉原来的，加入新合并的'''
    list(map(lambda x:this_stable_buses.remove(x), t_coincide_bus))
    list(map(lambda x:this_stable_buses.append(x), t_coincide_new_bus))

    for us_bus in unstable_buses:
        '''对不稳定的状态重新聚类'''
        to_cluster = [[pid, location] for pid, location in people_location if pid in us_bus.people]
        list(map(lambda x:people_location.remove(x), to_cluster))
        t_cluster_points, t_cluster_center, t_buses = cluster(to_cluster, precision+20)
        if len(t_buses) > 1:
            '''不稳定状态分裂仍然是不稳定状态'''
            for bus in t_buses:
                unstable_max_id = (((unstable_max_id+1)/2))*2+1
                this_unstable_buses.append(unstable_bus(unstable_max_id, bus[0], bus[1], 0, [], us_bus.line_num, us_bus.direction))
        elif len(t_buses) == 1:
            '''没有分裂则计数加1，满足要求则转换为稳定状态'''
            us_bus.stable_count += 1
            if us_bus.stable_count == continuous_stable_num:
                stable_max_id = ((stable_max_id/2)+1)*2
                this_stable_buses.append(stable_bus(stable_max_id, t_buses[0][0], us_bus.people, [], us_bus.routes, us_bus.line_num, us_bus.direction))
            else:
                this_unstable_buses.append(unstable_bus(us_bus.us_id, t_buses[0][0], us_bus.people, us_bus.stable_count, us_bus.routes, us_bus.line_num, us_bus.direction))

    t_undetermined = [[pid, location, arround_buses] for pid, location in people_location for pid2, arround_buses in undetermined if pid == pid2]
    for u_determine in t_undetermined:
        '''处理待定集合，附近只有一个稳定状态或非稳定状态则加入'''
        t_stable1 = [stable for stable in itertools.chain(this_stable_buses,this_unstable_buses) if stable.s_id in u_determine[2]]
        t_stable2 = [stable for stable in t_stable1 if is_in_cluster(u_determine[1], stable.location, precision)]
        if len(t_stable2) > 1:
            '''多于一个，仍是待定状态，更新t_undetermined'''
            this_undetermined.append([u_determine[0], [bus.s_id for bus in t_stable2]])
            people_location.remove([u_determine[0], u_determine[1]])    #在全集中删除该用户
        elif len(t_stable2) == 1:
            '''附近只有一个稳定状态或非稳定状态，则加入'''
            for t_stable_bus in this_stable_buses:
                if t_stable2[0].s_id == t_stable_bus.s_id:
                    t_stable_bus.people.append(u_determine[0])
                    break
            for t_unstable_bus in this_unstable_buses:
                if t_stable2[0].s_id == t_unstable_bus.s_id:
                    t_unstable_bus.people.append(u_determine[0])
                    break
            people_location.remove([u_determine[0], u_determine[1]])    #在全集中删除该用户
        elif len(t_stable2) == 0:
            '''附近没有稳定状态，则看作普通新上车的用户'''
            pass

    t_people = []    #保存处理过的用户
    for people in people_location:
        '''处理剩下的用户，即新上车的用户'''
        t_stables = [t_stable for t_stable in itertools.chain(this_stable_buses, this_unstable_buses) if is_in_cluster(people[1], t_stable.location, precision+20)]
        if len(t_stables) > 1:
            '''附近多于1个状态，进入待定'''
            this_undetermined.append([people[0], [t_stable.s_id for t_stable in t_stables]])
            t_people.append(people)
        elif len(t_stables) == 1:
            '''附近只有一个状态,加入'''
            for t_stable in itertools.chain(this_stable_buses, this_unstable_buses):
                if t_stable.s_id == t_stables[0].s_id:
                    t_stable.people.append(people[0])
                    t_people.append(people)
                    break
        else:
            '''附近没有稳定状态,看是否在某个不稳定状态中'''
            # for us_bus in this_unstable_buses:
            #     if is_in_cluster(people[1], us_bus.location, precision):
            #         '''在不稳定状态中，则加入'''
            #         us_bus.people.append(people[0])
            #         t_people.append(people)
            #         break

    list(map(lambda x:people_location.remove(x), t_people))    #处理过的用户都删掉

    '''最后剩下的用户整体调用聚类算法，所有结果都加入不稳定状态'''
    t_cluster_points, t_cluster_center, t_buses = cluster(people_location, precision)
    for bus in t_buses:
        '''对每一个聚类结果，首先看是否能加入消失的公交车上，如果不能再转为不稳定状态'''
        possilbe_bus = [d for d in disappeared if calDis_point2point(d.location[0], d.location[1], bus[0][0], bus[0][1])<= predict_bus_range]
        if possilbe_bus:
            dises = [calDis_point2point(d.location[0], d.location[1], bus[0][0], bus[0][1]) for d in possilbe_bus]
            min_index = dises.index(min(dises))
            stable_max_id = ((stable_max_id/2)+1)*2
            this_stable_buses.append(stable_bus(stable_max_id, bus[0], bus[1], [], possilbe_bus[min_index].routes, possilbe_bus[min_index].line_num, possilbe_bus[min_index].direction))
            disappeared.remove(possilbe_bus[min_index])
        else:
            unstable_max_id = (((unstable_max_id+1)/2))*2+1
            this_unstable_buses.append(unstable_bus(unstable_max_id, bus[0], bus[1]))

    while stable_buses:
        stable_buses.pop()
    list(map(lambda x:stable_buses.append(x), this_stable_buses))
    while unstable_buses:
        unstable_buses.pop()
    list(map(lambda x:unstable_buses.append(x), this_unstable_buses))
    while undetermined:
        undetermined.pop()
    list(map(lambda x:undetermined.append(x), this_undetermined))

    routeMatch(precision)

def routeMatch(precision):
    """match route for each bus
    """
    #路线匹配
    for s_bus in itertools.chain(stable_buses, unstable_buses):
        # if len(s_bus.routes) != 1:
        segmentids, routeid = searchRegion(s_bus.location[0], s_bus.location[1])
        segmentids = segmentids.split(',')
        dises = []
        res = []
        if segmentids != ['']:
            for s_id in segmentids:
                try:
                    r = buslines[s_id]
                except KeyError as k:
                    print(k)
                dis, projection_point = calDis_point2segment(s_bus.location[0], s_bus.location[1], r[1], r[2], r[3], r[4])
                dises.append(dis)
                res.append([dis, projection_point, r[5], r[0]])
            #在所有的距离中找到小于精度的，然后将路线的集合作为可能匹配的路线
            res = [p for p in res if p[0] <= precision]
            if s_bus.routes:
                possible_line = []
                for i in s_bus.routes:
                    possible_line += busroutes[i].split(',')
                res =[p for p in res if str(p[3]) in possible_line]
            route = [p[2] for p in res]
            if route:
                '''只有在精度范围内有路线时才进行线路匹配'''
                routes = list(set((','.join(route)).split(',')))
                if not s_bus.routes:
                    s_bus.routes = routes
                else:
                    s_bus.routes = [x for x in s_bus.routes if x in routes]
                    if not s_bus.routes:
                        s_bus.routes = routes
                #找到最短距离的线段，将投影点作为公交的位置
                mindis = min([p[0] for p in res])
                t = [(p[1], p[3]) for p in res if p[0] == mindis]
                new_location = t[0][0]
                new_line_num = str(t[0][1])
                if s_bus.location != new_location:
                    '''车辆位置发生变化时才会更新行驶方向'''
                    if s_bus.line_num != '0':
                        if s_bus.line_num == new_line_num:
                            '''前后都在一条线段上'''
                            r = buslines[s_bus.line_num]
                            if calDis_point2point(new_location[0], new_location[1], r[1], r[2]) > calDis_point2point(new_location[0], new_location[1], r[3], r[4]):
                                s_bus.direction = 1
                            else:
                                s_bus.direction = -1
                        else:
                            for i in s_bus.routes:
                                bus_route = busroutes[i]
                                bus_route = bus_route.split(',')
                                if new_line_num in bus_route and s_bus.line_num in bus_route:
                                    try:
                                        num1 = bus_route.index(s_bus.line_num)
                                    except ValueError as v:
                                        print(v)
                                    num2 = bus_route.index(new_line_num)
                                    if num2 > num1:
                                        p_num = num2-1
                                    else:
                                        p_num = num2+1
                                    r1 = buslines[new_line_num]
                                    r2 = buslines[bus_route[p_num]]
                                    for k in (r2[1], r2[3]):
                                        if r1[1] == k:
                                            s_bus.direction = 1
                                            break
                                        if r1[3] == k:
                                            s_bus.direction = -1
                                            break
                                    break
                s_bus.location = new_location
                s_bus.line_num = new_line_num