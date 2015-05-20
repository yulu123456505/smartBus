class unstable_bus(object):
    def __init__(self, us_id, location, people, stable_count=0):
        self.us_id = us_id
        self.location = location
        self.people = people
        self.stable_count = stable_count