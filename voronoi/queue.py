import heapq

class Event():
    def __init__(self, value, center=None, radius=0, pointer=None):
        # no matter the type of event, always a point
        self.value = value
        # in case is a circle event
        self.center = center
        self.radius = radius
        self.pointer = pointer


    def __repr__(self):
        return f"E[value = {self.value}]"

    def __lt__(self, other):
        return self.value < other.value

class Q():
    def __init__(self, data=[]):
        heapq.heapify(data)
        self.data = data

    def pop(self):
        return heapq.heappop(self.data)

    def push(self, node):
        heapq.heappush(self.data, node)

    def isEmpty(self):
        return not bool(len(self.data))

    def printq(self):
        print(self.data)




