import math
#计算点到点的距离
def calDis_point2point(a2,a1,b2,b1):
    radLat1 = math.radians(a1)
    radLat2 = math.radians(b1)
    a = math.radians(a1)-math.radians(b1)
    b = math.radians(a2)-math.radians(b2)

    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) + math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2),2)))
    s *= 6371393
    s = round(s*10000)/10000
    return s
#计算点到直线的距离
def calDis_point2line(point_x, point_y, line_x1, line_y1, line_x2, line_y2):
    projection_x = 0
    projection_y = 0
    if line_x1 == line_x2:
        projection_x = line_x1
        projection_y = point_y
    else:
        k = (line_y1 - line_y2)/(line_x1-line_x2)
        projection_x = (k * line_x1 + point_x/k + point_y-line_y1)/(1/k + k)
        projection_y = (1/k)*(projection_x-point_x) + point_y
    return calDis_point2point(projection_x,projection_y,point_x,point_y)

#计算点到线段的距离
def calDis_point2segment(point_x, point_y, line_x1, line_y1, line_x2, line_y2):
    projection_x = 0
    projection_y = 0
    if line_x1 == line_x2:
        projection_x = line_x1
        projection_y = point_y
    else:
        k = (line_y1 - line_y2)/(line_x1-line_x2)
        if k==0:
            projection_x = point_x
            projection_y = line_y1
        else:
            projection_x = (k * line_x1 + point_x/k + point_y-line_y1)/(1/k + k)
            projection_y = (1/k)*(projection_x-point_x) + point_y
    if line_x1 == line_x2:
        if min(line_y1, line_y2) <= projection_y <= max(line_y1, line_y2):
            return calDis_point2point(point_x,point_y,projection_x,projection_y)
        else:
            return min(calDis_point2point(line_x1,line_y1,point_x,point_y),calDis_point2point(line_x2,line_y2,point_x,point_y))
    elif (line_y1 - line_y2)/(line_x1-line_x2) == 0:
        if min(line_x1, line_x2) <= projection_x <= max(line_x1, line_x2):
            return calDis_point2point(point_x,point_y,projection_x,projection_y)
        else:
            return min(calDis_point2point(line_x1,line_y1,point_x,point_y),calDis_point2point(line_x2,line_y2,point_x,point_y))
    if min(line_x1, line_x2) <= projection_x <= max(line_x1, line_x2):
        return calDis_point2point(point_x,point_y,projection_x,projection_y)
    else:
        return min(calDis_point2point(line_x1,line_y1,point_x,point_y),calDis_point2point(line_x2,line_y2,point_x,point_y))

#判断线段和线段是否相交
def segmentIntersection(segment1_x1, segment1_y1, segment1_x2, segment1_y2, segment2_x1, segment2_y1, segment2_x2, segment2_y2):
    #两条线段都垂直
    if segment1_x1 == segment1_x2 and segment2_x1 == segment2_x2:
        if segment1_x1 == segment2_x1:
            if min(segment2_y1, segment2_y2) <= min(segment1_y1, segment1_y2) <= max(segment2_y1, segment2_y2) or min(segment1_y1, segment1_y2) <= min(segment2_y1, segment2_y2) <= max(segment1_y1, segment1_y2):
                return True
            else:
                return False
        else:
            return False
    #其中一条线段垂直
    if segment1_x1 == segment1_x2:
        k2 = (segment2_y1 - segment2_y2)/(segment2_x1 - segment2_x2)
        b2 = segment2_y1 - k2 * segment2_x1
        insection_y = k2 * segment1_x1 + b2
        if min(segment1_y1, segment1_y2) <= insection_y <= max(segment1_y1, segment1_y2) and min(segment2_y1, segment2_y2) <= insection_y <= max(segment2_y1, segment2_y2):
            return True
        else:
            return  False
    if segment2_x1 == segment2_x2:
        k1 = (segment1_y1 - segment1_y2)/(segment1_x1 - segment1_x2)
        b1 = segment1_y1 - k1 * segment1_x1
        insection_y = k1 * segment2_x1 + b1
        if min(segment1_y1, segment1_y2) <= insection_y <= max(segment1_y1, segment1_y2) and min(segment2_y1, segment2_y2) <= insection_y <= max(segment2_y1, segment2_y2):
            return True
        else:
            return  False
    #两条线段都不垂直
    k1 = (segment1_y1 - segment1_y2)/(segment1_x1 - segment1_x2)
    b1 = segment1_y1 - k1 * segment1_x1
    k2 = (segment2_y1 - segment2_y2)/(segment2_x1 - segment2_x2)
    b2 = segment2_y1 - k2 * segment2_x1
    #两条线都水平
    if k1 == k2:
        if b1 != b2:
            return False
        else:
            if min(segment2_x1, segment2_x2) <= min(segment1_x1, segment1_x2) <= max(segment2_x1, segment2_x2) or min(segment1_x1, segment1_x2) <= min(segment2_x1, segment2_x2) <= max(segment1_x1, segment1_x2):
                return True
            else:
                return False
    #只有一条线水平
    if k1 == 0:
        insection_x = (segment1_y1 - b2)/k2
        if min(segment1_x1, segment1_x2) <= insection_x <= max(segment1_x1, segment1_x2) and min(segment2_x1, segment2_x2) <= insection_x <= max(segment2_x1, segment2_x2):
            return True
        else:
            return False
    if k2 == 0:
        insection_x = (segment2_y1 - b1)/k1
        if min(segment1_x1, segment1_x2) <= insection_x <= max(segment1_x1, segment1_x2) and min(segment2_x1, segment2_x2) <= insection_x <= max(segment2_x1, segment2_x2):
            return True
        else:
            return False
    #两条线都不水平
    if k1 == k2:
        if b1 == b2:
            return T
    insection_x = (b2 - b1)/(k1 - k2)
    if min(segment1_x1, segment1_x2) <= insection_x <= max(segment1_x1, segment1_x2) and min(segment2_x1, segment2_x2) <= insection_x <= max(segment2_x1, segment2_x2):
        return True
    else:
        return False

#计算线段到矩形的最短距离，相交或包含返回0，否则返回最短距离
def calDis_segment2rect(segment_x1, segment_y1, segment_x2, segment_y2, rect_upleft_x, rect_upleft_y, rect_downright_x, rect_downright_y):
    #线段的端点是否在矩形的内部
    if rect_upleft_x <= segment_x1 <= rect_downright_x and rect_downright_y <= segment_y1 <= rect_upleft_y:
        return 0
    if rect_upleft_x <= segment_x2 <= rect_downright_x and rect_downright_y <= segment_y2 <= rect_upleft_y:
        return 0
    #判断线段是否和矩形的四条边相交
    if segmentIntersection(segment_x1, segment_y1, segment_x2, segment_y2, rect_upleft_x, rect_upleft_y, rect_downright_x, rect_upleft_y):
        return 0
    if segmentIntersection(segment_x1, segment_y1, segment_x2, segment_y2, rect_downright_x, rect_upleft_y, rect_downright_x, rect_downright_y):
        return 0
    if segmentIntersection(segment_x1, segment_y1, segment_x2, segment_y2, rect_downright_x, rect_downright_y, rect_upleft_x, rect_downright_y):
        return 0
    if segmentIntersection(segment_x1, segment_y1, segment_x2, segment_y2, rect_upleft_x, rect_downright_y, rect_upleft_x, rect_upleft_y):
        return 0
    #矩形四个顶点到线段的距离
    a1 = calDis_point2segment(rect_upleft_x, rect_upleft_y, segment_x1, segment_y1, segment_x2, segment_y2)
    a2 = calDis_point2segment(rect_downright_x, rect_upleft_y, segment_x1, segment_y1, segment_x2, segment_y2)
    a3 = calDis_point2segment(rect_downright_x, rect_downright_y, segment_x1, segment_y1, segment_x2, segment_y2)
    a4 = calDis_point2segment(rect_upleft_x, rect_downright_y, segment_x1, segment_y1, segment_x2, segment_y2)
    #线段两个端点到矩形四条边的距离
    a5 = calDis_point2segment(segment_x1, segment_y1, rect_upleft_x, rect_upleft_y, rect_downright_x, rect_upleft_y)
    a6 = calDis_point2segment(segment_x1, segment_y1, rect_downright_x, rect_upleft_y, rect_downright_x, rect_downright_y)
    a7 = calDis_point2segment(segment_x1, segment_y1, rect_downright_x, rect_downright_y, rect_upleft_x, rect_downright_y)
    a8 = calDis_point2segment(segment_x1, segment_y1, rect_upleft_x, rect_downright_y, rect_upleft_x, rect_upleft_y)

    a9 = calDis_point2segment(segment_x2, segment_y2, rect_upleft_x, rect_upleft_y, rect_downright_x, rect_upleft_y)
    a10 = calDis_point2segment(segment_x2, segment_y2, rect_downright_x, rect_upleft_y, rect_downright_x, rect_downright_y)
    a11 = calDis_point2segment(segment_x2, segment_y2, rect_downright_x, rect_downright_y, rect_upleft_x, rect_downright_y)
    a12 = calDis_point2segment(segment_x2, segment_y2, rect_upleft_x, rect_downright_y, rect_upleft_x, rect_upleft_y)

    return min(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)

if __name__ == '__main__':
    s = calDis_point2point(114.364888,30.533125,114.368211,30.533113)
    print(s)
    ss = calDis_point2segment(114.364888,30.533125,114.368256,30.536162,114.368616,30.536154)
    print(ss)
    b = segmentIntersection(114.365588,30.543868,114.366873,30.542783,114.366873,30.542783,114.366145,30.540975)
    print(b)
    c = calDis_segment2rect(114.368256,30.536162,114.368616,30.536154,114.368616,30.536154,114.369195,30.535971)
    print(c)

