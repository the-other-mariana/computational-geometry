import heapq

class Event():
    def __init__(self, value, center=None, radius=0, pointer=None):
        # no matter the type of event, always a point and a pointer
        self.value = value
        # site event has a pointer?
        # in case is a circle event
        self.pointer = pointer # must be an Event obj
        self.center = center
        self.radius = radius


    def __repr__(self):
        return f"E[value = {self.value}]"

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value and self.pointer == other.pointer and abs(self.center - other.center) and abs(self.center - other.center)

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

    def show(self):
        return self.data[0]

    def printq(self):
        print(self.data)

    def delete(self, node):
        self.data.remove(node)
        heapq.heapify(self.data)






