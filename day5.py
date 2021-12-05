# --- Day 5: Hydrothermal Venture ---

# You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

# They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

# 0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2
# Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

# - An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
# - An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
# For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

# So, the horizontal and vertical lines from the above list would produce the following diagram:

# .......1..
# ..1....1..
# ..1....1..
# .......1..
# .112111211
# ..........
# ..........
# ..........
# ..........
# 222111....
# In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

# To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

# Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

data = []
with open('input/day5', 'r') as f:
    data = f.read().splitlines()


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '{},{}'.format(self.x, self.y)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def from_vector(data):
        (a, b) = data.split('->')
        ax, ay = a.split(',')
        bx, by = b.split(',')
        return (Point(int(ax), int(ay)), Point(int(bx), int(by)))

    def isAlignedWith(self, other, axis=None):
        if axis == 'horizontal':
            return self.y == other.y
        if axis == 'vertical':
            return self.x == other.x
        if axis == 'diagonal':
            return self.distanceTo(other, axis='horizontal') == self.distanceTo(other, axis='vertical')
        return self.isAlignedWith(other, axis='horizontal') or self.isAlignedWith(other, axis='vertical') or self.isAlignedWith(other, axis='diagonal')

    def deltaOf(self, other, axis=None):
        if axis == 'horizontal':
            return self.x - other.x
        if axis == 'vertical':
            return self.y - other.y
        return self.deltaOf(other, axis='horizontal') + self.deltaOf(other, axis='vertical')

    def distanceTo(self, other, axis=None):
        return abs(self.deltaOf(other, axis=axis))

    def pathTo(self, other, axis=None):
        all = ['horizontal', 'vertical', 'diagonal']
        filter = [axis] if type(axis) == str else all
        filter = [str(o) for o in axis] if type(axis) == list else all
        if axis == 'horizontal':
            polarity = -1 if self.x > other.x else 1
            return [Point(x, self.y) for x in range(self.x, other.x + polarity, polarity)]
        if axis == 'vertical':
            polarity = -1 if self.y > other.y else 1
            return [Point(self.x, y) for y in range(self.y, other.y + polarity, polarity)]
        if axis == 'diagonal' and self.isAlignedWith(other, axis='diagonal'):
            order_x = [p.x for p in self.pathTo(other, axis='horizontal')]
            order_y = [p.y for p in self.pathTo(other, axis='vertical')]
            return [Point(x, y) for x, y in zip(order_x, order_y)]
        if self.isAlignedWith(other, axis='horizontal') and 'horizontal' in filter:
            return self.pathTo(other, axis='horizontal')
        if self.isAlignedWith(other, axis='vertical') and 'vertical' in filter:
            return self.pathTo(other, axis='vertical')
        if self.isAlignedWith(other, axis='diagonal') and 'diagonal' in filter:
            return self.pathTo(other, axis='diagonal')


class Vector:
    
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __str__(self):
        return '{} -> {}'.format(self.a, self.b)

    def __repr__(self):
        return str(self)

    @staticmethod
    def from_data(data):
        vectors = []
        for vector in data:
            (a, b) = Point.from_vector(vector)
            vectors.append(Vector(a, b))
        return vectors

    def getPath(self):
        return self.a.pathTo(self.b)


def count_overlapping_points(vectors, axis=None):
    points = {}
    for vector in vectors:
        path = vector.a.pathTo(vector.b, axis=axis)
        if path is None:
            continue
        for point in path:
            if point not in points:
                points[point] = 0
            points[point] += 1
    return points


def print_diagram(points):
    diagram = '\n'
    y_max = max([p.y for p in points]) + 1
    x_max = max([p.x for p in points]) + 1
    for y in range(y_max):
        for x in range(x_max):
            point = Point(x, y)
            if point in points:
                diagram += str(points[point])
            else:
                diagram += '.'
        diagram += '\n'
    print(diagram)


vectors = Vector.from_data(data)

points_hv = count_overlapping_points(vectors, axis=['horizontal', 'vertical'])

points_high_overlap = [p for p in points_hv if points_hv[p] > 1]

print_diagram(points_hv)

print('High overlap: {}\n'.format(len(points_high_overlap)))


# --- Part Two ---

# Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

# Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

# - An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
# - An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
# Considering all lines from the above example would now produce the following diagram:

# 1.1....11.
# .111...2..
# ..2.1.111.
# ...1.2.2..
# .112313211
# ...1.2....
# ..1...1...
# .1.....1..
# 1.......1.
# 222111....
# You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

# Consider all of the lines. At how many points do at least two lines overlap?

points_hvd = count_overlapping_points(vectors, axis=['horizontal', 'vertical', 'diagonal'])

points_high_overlap = [p for p in points_hvd if points_hvd[p] > 1]

print_diagram(points_hvd)

print('High overlap: {}'.format(len(points_high_overlap)))