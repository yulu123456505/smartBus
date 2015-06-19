import math
#计算点到点的距离
def calDis_point2point(a2,a1,b2,b1):
    """calculate the distance from a point to another.

    Args:
        a2,a1: the Longitude and Latitude of point1.
        b2,b1: the Longitude and Latitude of point2.
    Returns:
        a float which is the real distance between point1 to point2.
    """
    radLat1 = math.radians(a1)
    radLat2 = math.radians(b1)
    a = math.radians(a1)-math.radians(b1)
    b = math.radians(a2)-math.radians(b2)

    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) + math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2),2)))
    s *= 6371393    #the average radius of earth
    s = round(s*10000)/10000
    return s
#计算点到直线的距离
def calDis_point2line(point_x, point_y, line_x1, line_y1, line_x2, line_y2):
    """calculate the distance from a point to a straight line.

    first calculate the projection point which the point project to the straight line, then calculate the distance
    between the point and the projection point.

    Args:
        point_x, point_y: the Longitude and Latitude of point
        line_x1, line_y1, line_x2, line_y2: the Longitude and Latitude of two points which can determine a
            straight line.
    Returns:
        a float which is the real distance between the point and the straight line.
    """
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
    """calculate the distance from a point to a segment

    first calculate the projection point which the point project to the straight line that the segment belong to.
    If the projection point is on the segment, return the distance between the projection point and the point. If not,
    find the endpoint of the segment which is closer to the point, calculate the distance and return.

    Args:
        point_x, point_y: the Longitude and Latitude of point
        line_x1, line_y1, line_x2, line_y2: the Longitude and Latitude of two points which are the endpoints
            of the segment.
    Returns:
        a float which is the real distance between the point and the segment.
    """
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
            projection_y = (1/k)*(point_x - projection_x) + point_y

    dis1 = calDis_point2point(projection_x, projection_y, line_x1, line_y1)
    dis2 = calDis_point2point(projection_x, projection_y, line_x2, line_y2)
    dis3 = calDis_point2point(line_x1, line_y1, line_x2, line_y2)
    if max(0, dis3 - 0.1) <= dis1 + dis2 <= dis3 + 0.1:
        '''投影点在线段上'''
        return calDis_point2point(projection_x, projection_y, point_x, point_y), (projection_x, projection_y)
    else:
        if dis1 < dis2:
            return calDis_point2point(line_x1, line_y1, point_x, point_y), (line_x1, line_y1)
        else:
            return calDis_point2point(line_x2, line_y2, point_x, point_y), (line_x2, line_y2)


#判断线段和线段是否相交
def segmentIntersection(segment1_x1, segment1_y1, segment1_x2, segment1_y2, segment2_x1, segment2_y1, segment2_x2, segment2_y2):
    """judge if two segment is intersection

    Args:
        segment1_x1, segment1_y1, segment1_x2, segment1_y2:the Longitude and Latitude of endpoints of segment1
        segment2_x1, segment2_y1, segment2_x2, segment2_y2:the Longitude and Latitude of endpoints of segment2
    Returns:
        true or false
    """
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
    """calculate the distance from a segment to a rectangular

    Args:
        segment_x1, segment_y1, segment_x2, segment_y2:the Longitude and Latitude of endpoints of segment
        rect_upleft_x, rect_upleft_y: the Longitude and Latitude of the left_up point of the rectangular
        rect_downright_x, rect_downright_y: the Longitude and Latitude of the right_down point of the rectangular
    Returns:
        if the segment and the rectangular insects, return 0, else return the nearest distance from the segment to
        the rectangular
    """
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
    a1 = calDis_point2segment(rect_upleft_x, rect_upleft_y, segment_x1, segment_y1, segment_x2, segment_y2)[0]
    a2 = calDis_point2segment(rect_downright_x, rect_upleft_y, segment_x1, segment_y1, segment_x2, segment_y2)[0]
    a3 = calDis_point2segment(rect_downright_x, rect_downright_y, segment_x1, segment_y1, segment_x2, segment_y2)[0]
    a4 = calDis_point2segment(rect_upleft_x, rect_downright_y, segment_x1, segment_y1, segment_x2, segment_y2)[0]
    #线段两个端点到矩形四条边的距离
    a5 = calDis_point2segment(segment_x1, segment_y1, rect_upleft_x, rect_upleft_y, rect_downright_x, rect_upleft_y)[0]
    a6 = calDis_point2segment(segment_x1, segment_y1, rect_downright_x, rect_upleft_y, rect_downright_x, rect_downright_y)[0]
    a7 = calDis_point2segment(segment_x1, segment_y1, rect_downright_x, rect_downright_y, rect_upleft_x, rect_downright_y)[0]
    a8 = calDis_point2segment(segment_x1, segment_y1, rect_upleft_x, rect_downright_y, rect_upleft_x, rect_upleft_y)[0]

    a9 = calDis_point2segment(segment_x2, segment_y2, rect_upleft_x, rect_upleft_y, rect_downright_x, rect_upleft_y)[0]
    a10 = calDis_point2segment(segment_x2, segment_y2, rect_downright_x, rect_upleft_y, rect_downright_x, rect_downright_y)[0]
    a11 = calDis_point2segment(segment_x2, segment_y2, rect_downright_x, rect_downright_y, rect_upleft_x, rect_downright_y)[0]
    a12 = calDis_point2segment(segment_x2, segment_y2, rect_upleft_x, rect_downright_y, rect_upleft_x, rect_upleft_y)[0]

    return min(a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12)

if __name__ == '__main__':
    s = calDis_point2point(114.366494,30.543094,114.366808,30.5429)
    print(s)
    ss = calDis_point2segment(114.364888,30.533125,114.368256,30.536162,114.368616,30.536154)
    print(ss[0])
    b = segmentIntersection(114.365588,30.543868,114.366873,30.542783,114.366873,30.542783,114.366145,30.540975)
    print(b)
    c = calDis_segment2rect(114.368256,30.536162,114.368616,30.536154,114.368616,30.536154,114.369195,30.535971)
    print(c)

