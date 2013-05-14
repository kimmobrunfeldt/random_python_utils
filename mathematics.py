"""
Collection of random mathematical functions.
"""


import math


def rotate(x, y, rotation, rotationOrigin=(0, 0)):
    """Rotate coordinates around specified origin.

    Args:
    x, y: Coordinates.
    rotation: Rotation counter clockwise in radians.

    Kwargs:
    rotationOrigin: Coordinates are rotated relative to this
                    coordinate.
    """
    sin = math.sin
    cos = math.cos
    rotationOriginX, rotationOriginY = rotationOrigin

    # Rotate
    new_x = (cos(rotation) * x - (sin(rotation) * y))
    new_y = (sin(rotation) * x + cos(rotation) * y)

    # Move relative to the rotation origin
    new_x += rotationOriginX
    new_y += rotationOriginY

    return new_x, new_y


def distanceBetweenPoints(pointA, pointB):
    """Calculates distance ebtween A and B in 2-dimensional space.
    Points are in format (x, y) which is tuple.
    """
    xDiff = pointA[0] - pointB[0]
    yDiff = pointA[1] - pointB[1]
    return math.sqrt(xDiff ** 2 + yDiff ** 2)


def angleBetween(centerPoint, pointA, pointB):
    """Calculates the angle and returns it in radians.
    Works in 2-dimensional space. C is centerPoint.

                      b
                C -------- A
                 \ )     /
                  \     /
                a  \   /  c
                    \ /
                     B

    """
    a = distanceBetweenPoints(centerPoint, pointB)
    b = distanceBetweenPoints(centerPoint, pointA)
    c = distanceBetweenPoints(pointA, pointB)

    cosAngle = (c**2 - a**2 - b**2) / (2 * a * b)
    angle = math.acos(cosAngle)
    return angle


def radToDeg(angle):
    return angle * 180 / math.pi
