# Voronoi Diagram

The last implementation of this couse will be the Voronoi Diagram of a given set of points. The return value is an image with said diagram.

## 1. Data Structures Needed

### 1.1 Priority Queue (Q)

This will be a queue of Event objects, where each Event is basically a Node. The value of an Event is a Point object, where all events in the Priority Queue will be ordered their value's Y coordinate, where the biggest Y needs to be the first and if there's an equal Y, we take the one with smallest X value. <br />

To implement this, we will use `heapq` built-in structure from Python. We will call it Q. <br />

There are two types of Events: 

- **Point (Place) Events** and circle events. Point events are basically each one of the given points the algorithm must visit. This is an event where there will be an addition in T, which represents when a new parabola is found and its added to the beach line. This type of object will store the point as its value.

- **Circle Events** are the ones where three points form a circle, and the lowest point of this circle is the circle event. This is an event where there will be a deletion from T, which represents that its parabola disappears from the beach line. This type of object will store the lowest point of the circle (circun-radius substracted in the center's Y coordinate) formed by three consecutive points as its value. Additionally to the point it will store:

    - Its center. Depends on h.
    - Its radius. Depends on h.
    - A pointer to the leaf in T this event represents

### 1.2 Beach Line (T)

This will be the Sweep Line that will travel from top to bottom, and we will call it T. This will be implemented as a Binary Search Tree, where the three can have two types of nodes:

- **Internal Node** is any node that is not a leaf. This will contain a value that will be a tuple of points (Left point, R point) that will represent the intersection of two parabolas defined by the point and the sweep line Y level. It will also hold a pointer to its edge in the diagram.

- **External Node** is any node that is a leaf in the tree, which means it does not have any child. This node will store a value of just one point, representing the parabola defined by that point and the known sweep line Y level. It will also hold a pointer to its circle event where it will disappear from the sweep line.

This is how the tree will represent the Beach Line: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/T-structure.png?raw=true) <br />

which, by looking at the tree traversals' theory:

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/tree-traversals.png?raw=true) <br />

To search in the tree

## 2. Algorithm


### Main Function

1. Add to Q all the given points.
2. For every height h of the Beach Line:
3. Check if there is an event in Q at height h.
4. If there is an event:
5. Remove the firt event of Q. Do a Q pop basically and call it p.
6. If the event is a place event: <br />
    -> *activatePlace(p)*
7. Else: it is a circle event: <br />
    -> *activateCircle(p)*
8. Draw T.
9. End for.