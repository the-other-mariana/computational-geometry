from queue import Event, Q
from glibrary import Point, Line, Vector, eps

def main():
    q = Q()
    s1 = Event(Point(-5, 5))
    s2 = Event(Point(7, 18))
    s3 = Event(Point(18, 0))

    q.push(s1)
    q.push(s2)
    q.push(s3)

    while not q.isEmpty():
        q.printq()
        popped = q.pop()
        print("Pop: ", popped)

if __name__ == "__main__":
    main()