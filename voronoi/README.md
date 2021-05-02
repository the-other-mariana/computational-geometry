# Voronoi Diagram

The last implementation of this couse will be the Voronoi Diagram of a given set of points. The return value is an image with said diagram.

## 1. Data Structures Needed

### 1.1 Priority Queue

This will be a queue of Event objects, where each Event is basically a Node. The value of an Event is a Point object, where all events in the Priority Queue will be ordered their value's Y coordinate, where the biggest Y needs to be the first and if there's an equal Y, we take the one with smallest X value. <br />

To implement this, we will use `heapq` built-in structure from Python.

## 2. Algorithm