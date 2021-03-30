# Subdivision Intersection

The next algorithm to construct will be one that outputs the intersection of subdivisions (polygons or figures).

## General Ideas

This algorithm will require three basic classes: Vertex, Edge and Face. Each of these objects' properties will be described in the example files with extennsions `.ver`, `.ari` and `.car` respectively for each object.<br />

### Mates

However, in the Edge object there is a property called **mate**. A mate of an Edge is an Edge that is the same as the current Edge, but with different orientation, as shown below. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/res/mates-diag.png?raw=true) <br />

### Faces: Internals and Externals

Another idea used for this algorithm is that a Face object contains **External** and **Internal** Edges as a property. 
- **Internal** contains the first Edge of each shape that is inside the Face. If there is a list, the first Edges of each insider figure are there. 
- **External** contains the first Edge of each shape that is outside the line's Face. There cannot be lists.

These ideas can be best understood with the drawing below, where one face (F1) is the area of the figure and contains F2' first edge as external, and F2 would be a face containing the area surrounding the shape, while having F1's first edge as internal. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/res/faces-diag.png?raw=true) <br />

## Data Structures Needed

### 1.1 Edge Linked List (Map)

The input for the program will be with 3 files: 
- `.ver` file: Vertex object file. The format is shown in the [example](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/03/layer01.ver) below.
    - **Incident** is an Edge that *begins* at that line's vertex.
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

- `.ari` file: Edge object file. The format is shown in the [example](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/03/layer01.ari).
    - **Origin** is a Vertex where the Edge begins.
    - **Mate** is an Edge that is the same as the line's Edge, but with different orientation.
    - **Face** is a Face where the Edge belongs to.
    - **Next** is an Edge that goes next from this Edge in a shape's sequence.
    - **Prev** is an Edge that goes before this Edge in a shape's sequence.
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
    - **Internal** contains the first Edge of each shape that is inside the line's Face. If there is a list, the first Edges of each figure are there.
    - **External** contains the first Edge of each shape that is outside the line's Face. There cannot be lists.
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

In order to output the intersection faces of two layers or more, we need to perform a layer superposition. <br />

Two layers superposition will involve updating their Edge file, Vertex file and Face file according to the intersections of the faces of each layers. We will use a simpler example of layers so that the concept is understood.

The f1 face (a line) from [layer 01 from example 01](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/01/layer01.car) looks as follows: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/f1-i01.png?raw=true) <br />

With the files:

- `.ver` file (layer01.ver):

```
Vertex file
#################################
Name    x       y       Incident
#################################
p1      0       10      s11
p2      10      0       s12
```

- `.ari` file (layer01.ari):

```
Edge file
#############################################
Name    Origin  Mate    Face    Next    Prev
#############################################
s11     p1      s12     f1      s12     s12
s12     p2      s11     f1      s11     s11
```

- `.car` file (layer01.car):

```
Face file
#######################
Name    Internal  External
#######################
f1      s11     None
```

The f2 face (another line) from [layer 02 from example 01](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/input/01/layer02.car) looks as follows: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/f2-i01.png?raw=true)<br />

With the files:

- `.ver` file (layer02.ver):

```
Vertex file
#################################
Name    x       y       Incident
#################################
p1      0       10      s11
p2      10      0       s12
```

- `.ari` file (layer02.ari):

```
Edge file
#############################################
Name    Origin  Mate    Face    Next    Prev
#############################################
s21     p3      s22     f2      s22     s22
s22     p4      s21     f2      s21     s21
```

- `.car` file (layer02.car):

```
Face file
#######################
Name    Internal External
#######################
f2      s21     None
```

Which basically have the information as follows. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/res/layer01-02-diag.png?raw=true) <br />

Now, what is next is to perform: <br />

| **layer01 + layer 02 = layer03** |
|     :---:      |

With all three files of each layer, and output a third layer (layer03) with its three files. Layer 03 will basically look as below. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/res/layer03-diag.png?raw=true) <br />

### 1.2.1 Vertices & Edges Update

Source Code: [code main.py](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/main.py)

1. We check for intersections with the Segment Intersection algorithm. If there are intersections, each hit point becomes a new Vertex. Add it to Vertex file, with Incident as None.

2. For each intersection point, we gather the two involved segments and its two mates. Then, each of these gathered Edges will be split into two Edges: the original will now be smaller, called *prime*, and the other half which we call *bprime* ("pp" named Edges).

3. Pattern: primes take its original Edge's Prev Edge, while bprimes take its original Edge's Next Edge. Now, we just update these Prev and Next originals in the new map with the new Edge as Next and Prev, respectively.

4. We build a **Circular List** for primes and another for bprimes: taking the new vertex as p1, and p2 will be the endpoint of the Edges there (cross's extremes, in the example), order the Edges in the list by the `atan2(p2.y - p1.y, p2.x - p1.x)` value (Edge endpoint's angle with respect to the new Vertex), and finally create a final Circular List by appending one prime and then one bprime and so on from each of the previously sorted lists.

5. Use the Circular List to update to the prime Edges its Next and to each of the bprime Edges its Prev, which were the values that were not taken from the old list during step 3.

6. Update the None Incident property of the new Vertex we left in the first step. Summarizing:
    - Primes get old Prev, but take Next from the Circular List.
    - BPrimes get old Next, but take Prev from the Circular List.

### 1.2.2 Face Update

1. Loop over the Edge map to find **cycles**, that represent possible faces.
    -  A cycle is made by finding the next *unvisited* Edge in the map that makes a shape.
2. For each cycle, obtain the Edge that has the left-most Origin Vertex.
3. With this Edge obtained, called *a*, grab also its Prev Edge, called *b*, and perform a cross product *a* x *b*. If the cross product length is >= 0, their angle is larger than 180°, and therefore it is an **external**. If the cross product is < 0, then the angle is smaller than 180° and the cycle is **internal**.

### 1.2.3 Example Outputs

From the update rules above, the example at [folder 01](https://github.com/the-other-mariana/computational-geometry/tree/master/subdivision-intersection/input/01) we should have as output the following layer: <br />

Folder 01 (Cross Image) Output Layer
----

- `.ver` file (layer03.ver):

```
Vertex File
#################################
Name	x	y	Incident
#################################
p1	0	10	s11
p2	10	0	s12
p3	0	0	s21
p4	10	10	s22
p5	5.0	5.0	s11pp
```

- `.ari` file (layer03.ari):

```
Edge File
#################################
Name	Origin	Mate	Face	Next	Prev
#################################
s12	p2	s11pp	None	s22pp	s11pp
s11	p1	s12pp	None	s21pp	s12pp
s11pp	p5	s12	None	s12	s22
s12pp	p5	s11	None	s11	s21
s21	p3	s22pp	None	s12pp	s22pp
s22	p4	s21pp	None	s11pp	s21pp
s22pp	p5	s21	None	s21	s12
s21pp	p5	s22	None	s22	s11
```

- `.car` file (layer03.car):

```
Face File
#################################
Name	Internal	External
#################################
f1	s12	None
```

And when we plot this layer 03 result, we get the following image: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/layer03-ex01.png?raw=true) <br />

Folder 02 (Two Overlapped Triangles) Output Layer
----

Following this logic, we will visualize how face update works with another example located on [folder 02](https://github.com/the-other-mariana/computational-geometry/tree/master/subdivision-intersection/input/02), since the mentioned example results in new face creation. <br />

The next example has the files:

### Layer 01

- `.ver` file (layer01.ver):

```
Vertex File
#################################
Name    x       y       Incident
#################################
p1      0       0       s11
p2      0       10      s21
p3      8       5       s31
```

- `.ari` file (layer01.ari):

```
Edge file
#############################################
Name    Origin  Mate    Face    Next    Prev
#############################################
s11     p1      s12     f1      s21     s31
s12     p2      s11     f2      s32     s22
s21     p2      s22     f1      s31     s11
s22     p3      s21     f2      s12     s32
s31     p3      s32     f1      s11     s21
s32     p1      s31     f2      s22     s12
```

- `.car` file (layer01.car):

```
Face file
#######################
Name    Internal External
#######################
f1      s11     None
f2      None    s12
```

### Layer 02

- `.ver` file (layer02.ver):

```
Vertex File
#################################
Name    x       y       Incident
#################################
p4      10      10      s41
p5      10      0       s51
p6      2       5       s61
```

- `.ari` file (layer02.ari):

```
Edge file
#############################################
Name    Origin  Mate    Face    Next    Prev
#############################################
s41     p4      s42     f3      s51     s61
s42     p5      s41     f4      s62     s52
s51     p5      s52     f3      s61     s41
s52     p6      s51     f4      s42     s62
s61     p6      s62     f3      s41     s51
s62     p4      s61     f4      s52     s42
```

- `.car` file (layer02.car):

```
Face file
#######################
Name    Internal External
#######################
f3      s41     None
f4      None    s42
```

Which basically have the information as follows. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/res/02-layers-diag.png?raw=true) <br />

Then, after **Vertex, Edge and Face Map Update** due to its proper segment intersections, we get the following **layer03** output files: <br />

- `.ver` file (layer02.ver):

```
Vertex File
#################################
Name    x       y       Incident
#################################
p1	0	0	s11
p2	0	10	s21
p3	8	5	s31
p4	10	10	s62
p5	10	0	s42
p6	2	5	s52
p7	5.0	6.875	s21pp
p8	5.0	3.125	s31pp
```

- `.ari` file (layer02.ari):

```
Edge file
#############################################
Name    Origin  Mate    Face    Next    Prev
#############################################
s11	p1	s12	f1	s21	s31pp
s21	p2	s22pp	f1	s61pp	s11
s31	p3	s32pp	f2	s52pp	s21pp
s21pp	p7	s22	f2	s31	s62
s32	p1	s31pp	f3	s51pp	s12
s22	p3	s21pp	f4	s62pp	s32pp
s12	p2	s11	f3	s32	s22pp
s22pp	p7	s21	f3	s12	s61
s42	p5	s41	f2	s62	s52pp
s62	p4	s61pp	f2	s21pp	s42
s52	p6	s51pp	f4	s32pp	s62pp
s62pp	p7	s61	f4	s52	s22
s51	p5	s52pp	f1	s31pp	s41
s61	p6	s62pp	f3	s22pp	s51pp
s41	p4	s42	f1	s51	s61pp
s61pp	p7	s62	f1	s41	s21
s31pp	p8	s32	f1	s11	s51
s32pp	p8	s31	f4	s22	s52
s52pp	p8	s51	f2	s42	s31
s51pp	p8	s52	f3	s61	s32
```

- `.car` file (layer02.car):

```
Face file
#######################
Name    Internal External
#######################
f2	None	s31
f3	None	s32
f4	None	s22
f1	s11	None
```
 
And when we plot this layer 03 result, taking on account that: <br />

- **External** faces will be polygons filled with continuous colors,
- **Internal Unique** faces will be polygons filled with a hatch pattern,
- **Internal Lists** faces will be polygons filled with a hatch pattern, all with the same tone per list,

we get the following image: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/subdivision-intersection/output/layer03-ex02-legend.png?raw=true) <br />


