from functools import reduce

def cluster(points, precision=40):
    flag = [0 for x in range(len(points))]
    cluster_center = []
    for i, point in enumerate(points):
        print(i, point, flag[i])
        if flag[i] == 0:
            flag[i] = 1
            center_point = [-1, -1]
            shift_point = point
            while center_point != shift_point:
                center_point = shift_point
                p = [[i, x] for i, x in enumerate(points) if flag[i] != 1 and abs(center_point[0] - x[0]) <= precision and abs(center_point[1] - x[1]) <= precision]    #先缩小范围在方形区域
                p = [[i, x] for i, x in p if abs(center_point[0] - x[0])**2 + abs(center_point[1] - x[1])**2 <= precision**2]    #再在方形区域中计算是不是在圆内
                if not p:
                    break
                vector = [[x[0]-center_point[0], x[1]-center_point[1]] for i, x in p]
                shift_point = reduce(lambda x, y: [x[0]+y[0], x[1]+y[1]], vector)
                shift_point = [center_point[0]+shift_point[0]/len(p), center_point[1] + shift_point[1]/len(p)]

            cluster_center.append(center_point)
            for n, x in p:
                flag[n] = 1
    return cluster_center