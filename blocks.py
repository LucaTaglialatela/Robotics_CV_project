class Block(object):
    def __init__(self, color, shape, centroid, orientation, mode):
        self.color = color
        self.shape = shape
        self.centroid = centroid
        self.orientation = orientation
        self.mode = mode

    def getHeight(self):
        pass

    def getX(self):
        return self.centroid[0]

    def getY(self):
        return self.centroid[1]

    def printBlock(self):
        print(self.color, self.shape, self.centroid, self.orientation, "mode=", self.mode)

class Square(Block):
    def __init__(self, color, shape, centroid, orientation, mode = 0):
        super(Square, self).__init__(color, shape, centroid, orientation, mode)

    def getHeight(self):
        return 2.5

class Rectangle(Block):
    def __init__(self, color, shape, centroid, orientation, mode = 0):
        super(Rectangle, self).__init__(color, shape, centroid, orientation, mode)

    def getHeight(self):
        return 2.5

class Circle(Block):
    def __init__(self, color, shape, centroid, orientation, mode = 0):
        super(Circle, self).__init__(color, shape, centroid, orientation, mode)

    def getHeight(self):
        return 3.2

class Triangle(Block):
    def __init__(self, color, shape, centroid, orientation, mode = 0):
        super(Triangle, self).__init__(color, shape, centroid, orientation, mode)

    def getHeight(self):
        return 3