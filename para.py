people_on_bus = []    #在公交车上的人
people_idle = []    #没有上公交车的人

predicted_buses = []

stable_buses = []
unstable_buses = []
undetermined = []
"""待定用户的集合
    example:
    [ [pid1,[bus_id1,bus_id2]], [pid2,[bus_id1, bus_id2]], ... ]
"""

disappeared = []
