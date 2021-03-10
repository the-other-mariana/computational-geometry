# Subdivision Intersection

The next algorithm to construct will be one that outputs the intersection of subdivisions (polygons or figures).

## Data Structures Needed

### 1.1 Edge Linked List (Map)

The input for the program will be with 3 files: 
- `.ver` file: Vertex file. The format is shown in the [example](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/03/layer01.ver).

```
Vertex file
#################################
Name   x       y       Incident
#################################
A      3       5        g1
B      5       5        h1
C      5       8        i1
D      3       9        f1
E      8       4        l1
F      8       2        j1
G      10      3        k1
H      9       11       r1
I      8       9        m1
J      10.1    7        n1
K      13      8        p1
L      13      10.5     q1
```

- `.ari` file: Edge file. The format is shown in the [example](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/03/layer01.ari).

```
Edge file
#############################################
Name    Origin  Mate    Face    Next   Prev
#############################################
f1      A       f2      CARA1   i1      g1
f2      D       f1      CARA2   g2      i2
i1      D       i2      CARA1   h1      f1
i2      C       i1      CARA2   f2      h2
h1      C       h2      CARA1   g1      i1
h2      B       h1      CARA2   i2      g2
g1      B       g2      CARA1   f1      h1
g2      A       g1      CARA2   h2      f2
l1      E       l2      CARA1   k1      j1
l2      G       l1      CARA3   j2      k2
k1      G       k2      CARA1   j1      l1
k2      F       k1      CARA3   l2      j2
j1      F       j2      CARA1   l1      k1
j2      E       j1      CARA3   k2      l2
m1      I       m2      CARA1   r1      n1
m2      H       m1      CARA4   n2      r2
r1      H       r2      CARA1   q1      m1
r2      L       r1      CARA4   m2      q2
q1      L       q2      CARA1   p1      r1
q2      K       q1      CARA4   r2      p2
p1      K       p2      CARA1   n1      q1
p2      J       p1      CARA4   q2      n2
n1      J       n2      CARA1   m1      p1
n2      I       n1      CARA4   p2      m2
```

- `.car` file: Face file. The format is shown in the [example](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/03/layer01.car).

```
Face file
#######################
Name    Internal        External
#######################
CARA1   [f1,q1,l1]     None
CARA2   None           g2
CARA3   None           j2
CARA4   None           m2  
```

These files will connect within each other, because faces contain edges, which contain vertices. Edges are supposed to have a **mate or pair**, which is also an edge starting and ending in the same points, but pointing in another orientation. This is because the faces can be the area of, for example, a polygon, or the area **surrounding** that polygon. <br />

The three files shown above represent the following set: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/diagram.jpeg?raw=true)

### 1.1.1 Edge Linked List Queries

To test the correct organization of the map (Edge Linked List), the [ELL.py](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/ELL.py) works as following:

- for CARA1:

```
Enter face:
CARA1
```
Outputs the plot: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/FACE1.png?raw=true)

- for CARA2:

```
Enter face:
CARA2
```
Outputs the plot: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/FACE2.png?raw=true)

- for CARA3:

```
Enter face:
CARA3
```
Outputs the plot: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/FACE3.png?raw=true)

- for CARA4:

```
Enter face:
CARA4
```
Outputs the plot: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/FACE4.png?raw=true)

## 1.2 Layer Superposition

Two layers superposition will involve updating their edges according to the intersections of the faces of each layers.

The f1 face (a line) from [layer 01 from example 01](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/01/layer01.car) looks as follows: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/f1-i01.png?raw=true) <br />

The f2 face (another line) from [layer 02 from example 01](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/01/layer02.car) looks as follows: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/f2-i01.png?raw=true)<br />

The [code main.py](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/main.py) now joins the vertices, edges and faces present each layer from an N number of layers. If we take [folder 01 (2 layers)](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/01/) and plot all the combined faces, we get the following. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/f1-f2-i01.png?raw=true)<br />