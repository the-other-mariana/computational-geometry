import heapq

class Node():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"N[value = {self.value}]"

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




