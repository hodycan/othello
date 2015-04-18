

# >>> import point
# >>> p1 = point.from_frac(0.5, 0.6)
# >>> p1
# <point.Point object ...>

# >>> p1.frac()
# (0.5, 0.6)

# >>> p1.pixel(1000, 800)
# (500, 480)

# >>> p2 = point.from_pixel(400, 600, 800, 800)
# >>> p2.frac()
# (0.5, 0.75)

# >>> p2.pixel(2000, 2000)
# (1000, 1500)

import math

class Point:
    def __init__(self, frac_x: float, frac_y: float):
        '''
        Initializes a Point object, given its fractional coordinates.
        '''
        self._frac_x = frac_x
        self._frac_y = frac_y


    def frac(self) -> (float, float):
        '''
        Returns an (x, y) tuple that contains fractional coordinates
        for this Point object.
        '''
        return (self._frac_x, self._frac_y)


    def pixel(self, width: float, height: float) -> (float, float):
        '''
        Returns an (x, y) tuple that contains pixel coordinates for
        this Point object.  The total_size parameter specifies the
        total size, in pixels, of the area in which the point needs
        to be specified -- this is used to make the appropriate
        conversion, since the pixel position of a fractional point
        changes as the size changes.
        '''
        return (int(self._frac_x * width), int(self._frac_y * height))


    def frac_distance_from(self, p: 'Point') -> float:
        '''
        Given another Point object, returns the distance, in
        terms of fractional coordinates, between this Point and the
        other Point.
        '''
        return math.sqrt(
            (self._frac_x - p._frac_x) * (self._frac_x - p._frac_x)
            + (self._frac_y - p._frac_y) * (self._frac_y - p._frac_y))

    def __repr__(self):
        return 'Point({:.3f}, {:.3f})'.format(self._frac_x, self._frac_y)
    
def from_frac(frac_x: float, frac_y: float) -> Point:
    '''Builds a Point given fractional x and y coordinates.'''
    return Point(frac_x, frac_y)


def from_pixel(pixel_x: float, pixel_y: float, width: float, height: float) -> Point:
    '''
    Builds a Point given pixel x and y coordinates, along with
    the width and height of the area (necessary for conversion
    to fractional).
    '''
    return Point(pixel_x / width, pixel_y / height)
