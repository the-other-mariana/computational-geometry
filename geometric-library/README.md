# Geometric Library v1.0

This is a first exercise where a custom library is to be done in order to perform further geometric operations. <br />

## Content

The `tests.py` file uses `glibrary.py` file as library to perform geometric operations. <br />

The `glibrary.py` file contains the following: <br />

- Points 2D
  - Constructor
  - Equals override
  - String override
  - Rotation
  - Distance (static)
- Line 2D
  - Constructor
  - String override
  - Points2Line (static)
  - Parallel
  - Intersection
  - Equivalence
  - Distance from Point to Line (static)
  - Distance from Point to Segment (static)
- Vector 2D
  - Constructor
  - Points2Vector (static)
  - Scale
  - Translate (static, returns Point)
  - Dot Product (static)
  - Cross Product (static)
  - Square Norm (static)
  - Angle (static)
  - Counter Clock Wise (static)
  - Collinear (static)

## Problem Set 01

### Problem 1

Given a set of mountain peak coordinates (x,y) return an image that shows the mountain segments that are illuminated by a sun on the right, that functions as a horizontal *directional light* from right to left. <br />

#### Test Case 1: [test file](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/1.in)

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/output-img/output-p1-i1.png?raw=true) <br />

#### Test Case 2: [test file](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/2.in)

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/output-img/output-p1-i2.png?raw=true) <br />

### Problem 1

Given a set of points that join a train track and a robber's position, show the shortest point in the train tracks to the robber's hiding place. <br />

#### Test Case 1: [test file](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/3.in)

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/output-img/output_p2_i1.png?raw=true) <br />

#### Test Case 2: [test file](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/4.in)

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/geometric-library/output-img/output_p2_i2.png?raw=true) <br />