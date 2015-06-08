class stable_bus(object):
    def __init__(self, s_id, location, people, coincide_bus_count=None, routes=None, line_num='0', direction=0):
        '''id，位置，车上的人，重合的公交车计数，可能的路径集合,目前所在的线段编号'''
        self.s_id = s_id
        self.location = location
        self.people = people
        if coincide_bus_count is None:
            coincide_bus_count = []
        self.coincide_bus_count = coincide_bus_count
        if routes is None:
            routes = []
        self.routes = routes
        self.line_num=line_num
        self.direction=direction


