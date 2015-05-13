class person(object):
    #p_GPS_location = [0, 0]
    __p_bus_id = 0;
    __p_bus_location = [0, 0]
    p_seat_location = [0, 0]
    def __init__(self, p_id):
        self.p_id = p_id

    def set_bus_Info(self, bus_id, seat_location):
        self.__p_bus_id = bus_id
        self.p_seat_location = seat_location

    def get_bus_Info(self):
        return self.__p_bus_id, self.p_seat_location

