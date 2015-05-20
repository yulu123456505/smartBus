from functools import reduce
from para import predicted_buses, stable_buses, unstable_buses, undetermined
from stable_bus import stable_bus
from unstable_bus import unstable_bus

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
            circle_num = 0
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

def is_in_cluster(new_point, cluster_center, precision=40):
    if abs(new_point[0]-cluster_center[0])**2+abs(new_point[1]-cluster_center[1])**2 <= precision**2:
        return True
    else:
        return False

def dynamic_cluster2(people_location, precision=40):
    this_stable_buses = []
    this_unstable_buses = []
    this_undetermined = []
    if len(stable_buses) > 0:
        stable_max_id = max([s_bus.s_id for s_bus in stable_buses])    #稳定状态集合的最大id
    else:
        stable_max_id = 0
    if len(unstable_buses) > 0:
        unstable_max_id = max([us_bus.us_id for us_bus in unstable_buses])    #不稳定状态集合的最大id
    else:
        unstable_max_id = 0

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
                unstable_max_id += 1
                this_unstable_buses.append(unstable_bus(unstable_max_id, bus[0], bus[1]))
        elif len(t_buses) == 1:
            '''没有分裂只更新位置'''
            this_stable_buses.append(stable_bus(s_bus.s_id, t_buses[0][0], s_bus.people, s_bus.coincide_bus_count))

    for i in range(len(this_stable_buses)):
        '''输出合并次数列表，供调试'''
        print(this_stable_buses[i].s_id, this_stable_buses[i].coincide_bus_count)

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
                if is_in_cluster(this_stable_buses[i].location, this_stable_buses[j].location, precision):
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
                stable_max_id += 1
                coincide_people = []
                for j in num:
                    coincide_people += this_stable_buses[j].people
                t_coincide_new_bus.append(stable_bus(stable_max_id, this_stable_buses[i].location, coincide_people, []))
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
                unstable_max_id += 1
                this_unstable_buses.append(unstable_bus(unstable_max_id, bus[0], bus[1]))
        elif len(t_buses) == 1:
            '''没有分裂则计数加1，满足要求则转换为稳定状态'''
            us_bus.stable_count += 1
            if us_bus.stable_count == continuous_stable_num:
                stable_max_id += 1
                this_stable_buses.append(stable_bus(stable_max_id, t_buses[0][0], us_bus.people, []))
            else:
                this_unstable_buses.append(unstable_bus(us_bus.us_id, t_buses[0][0], us_bus.people, us_bus.stable_count))

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
        else:
            '''附近没有稳定状态,看是否在某个不稳定状态中'''
            for us_bus in this_unstable_buses:
                if is_in_cluster(people[1], us_bus.location, precision):
                    '''在不稳定状态中，则加入'''
                    us_bus.people.append(people[0])
                    t_people.append(people)
                    break

    list(map(lambda x:people_location.remove(x), t_people))    #处理过的用户都删掉

    '''最后剩下的用户整体调用聚类算法，所有结果都加入不稳定状态'''
    t_cluster_points, t_cluster_center, t_buses = cluster(people_location, precision)
    for bus in t_buses:
        unstable_max_id += 1
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



