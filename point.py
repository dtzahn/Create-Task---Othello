
import math

class Point:
    def __init__(self, frac_x: float, frac_y: float):
        '''Initializes a Point object, given its fractional coordinates.'''

        self.frac_x = frac_x
        self.frac_y = frac_y

    def frac(self) -> (float, float):
        '''Returns an (x, y) tuple that contains fractional coordinates
        for this Point object.'''

        return (self.frac_x, self.frac_y)

    def pixel(self, width: float, height: float) -> (float, float):
        '''Returns an (x, y) tuple that contains pixel coordinates for
        this Point object.'''

        return (int(self.frac_x * width), int(self.frac_y * height))

    def frac_distance_from(self, p: 'Point') -> float:
        '''Returns the distance, interms of fractional coordinates,
        between the Point specified by the class and the  given Point.'''

        return math.hypot(self.frac_x - p.frac_x, self.frac_y - p.frac_y)


# Fractional/Pixel Point Alternate Genertion

def from_frac(frac_x: float, frac_y: float) -> Point:
    '''Creates a point from fractional coordinates'''

    return Point(frac_x, frac_y)

def from_pixel(pixel_x: float, pixel_y: float, width: float, height: float) -> Point:
    '''Creates a point from pixels and converts the pixels to
    fractional coordinates.'''

    return Point(pixel_x/width, pixel_y/height)
