# coding: utf-8
# GeoHex by @sa2da (http://geogames.net) is licensed under Creative Commons BY-SA 2.1 Japan License.

from collections import namedtuple

class Point(namedtuple('Point', 'x y')):
    pass

class Coord(namedtuple('Coord', 'lon lat')):
    pass

class Zone(object):
    
    def __init__(self, lat, lon, x, y, code):
        self.coord = Coord(lon, lat)
        self.point = Point(x, y)
        self.code = code

    def getLevel(self):
        raise NotImplementedError

    def getHexSize(self):
        raise NotImplementedError

    def getHexCoords(self):
        raise NotImplementedError

    @property
    def lon(self):
        return self.coord.lon

    @property
    def lat(self):
        return self.coord.lat

    @property
    def x(self):
        return self.point.x

    @property
    def y(self):
        return self.point.y
