# coding: utf-8
# GeoHex by @sa2da (http://geogames.net) is licensed under Creative Commons BY-SA 2.1 Japan License.

from base import Point, Coord
from base import Zone as ZoneBase
from utils import round_int, floor_int, ceil_int, base_convert

import math

__all__ = ['Zone', 'getZoneByLocation', 'getZoneByCode']

H_KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
H_BASE = 20037508.34
H_DEG = math.pi * (30.0 / 180.0)
H_K = math.tan(H_DEG)

def calcHexSize(level):
    return H_BASE / math.pow(3, level + 1)

class Zone(ZoneBase):

    def getLevel(self):
        return len(self.code) - 2

    def getHexSize(self):
        return calcHexSize(self.getLevel() + 2)

    def getHexCoords(self):
        h_lat = self.lat
        h_lon = self.lon
        h_xy = loc2xy(h_lon, h_lat)
        h_x = h_xy[0]
        h_y = h_xy[1]
        h_deg = math.tan(math.pi * (60.0 / 180.0))

        h_size = self.getHexSize()
        h_top = xy2loc(h_x, h_y + h_deg *  h_size)[1]
        h_btm = xy2loc(h_x, h_y - h_deg *  h_size)[1]

        h_l = xy2loc(h_x - 2 * h_size, h_y)[0]
        h_r = xy2loc(h_x + 2 * h_size, h_y)[0]
        h_cl = xy2loc(h_x - 1 * h_size, h_y)[0]
        h_cr = xy2loc(h_x + 1 * h_size, h_y)[0]
        return (
            Coord(h_lat, h_l),
            Coord(h_top, h_cl),
            Coord(h_top, h_cr),
            Coord(h_lat, h_r),
            Coord(h_btm, h_cr),
            Coord(h_btm, h_cl)
        )

def getZoneByLocation(lat, lon, level):
    level += 2
    h_size = calcHexSize(level)

    z_xy = loc2xy(lon, lat)
    lon_grid = z_xy.x
    lat_grid = z_xy.y
    unit_x = 6 * h_size
    unit_y = 6 * h_size * H_K
    h_pos_x = (lon_grid + lat_grid / H_K) / unit_x
    h_pos_y = (lat_grid - H_K * lon_grid) / unit_y
    h_x_0 = floor_int(h_pos_x)
    h_y_0 = floor_int(h_pos_y)
    h_x_q = h_pos_x - h_x_0 
    h_y_q = h_pos_y - h_y_0
    h_x = round_int(h_pos_x)
    h_y = round_int(h_pos_y)

    if h_y_q > -h_x_q + 1:
        if (h_y_q < 2 * h_x_q) and (h_y_q > 0.5 * h_x_q):
            h_x = h_x_0 + 1
            h_y = h_y_0 + 1
    elif h_y_q < -h_x_q + 1:
        if (h_y_q > (2 * h_x_q) - 1) and (h_y_q < (0.5 * h_x_q) + 0.5):
            h_x = h_x_0
            h_y = h_y_0

    h_lat = (H_K * h_x * unit_x + h_y * unit_y) / 2
    h_lon = (h_lat - h_y * unit_y) / H_K

    z_loc = xy2loc(h_lon, h_lat)
    z_loc_x = z_loc.lon
    z_loc_y = z_loc.lat
    if H_BASE - h_lon < h_size:
        z_loc_x = 180
        h_xy = h_x
        h_x = h_y
        h_y = h_xy

    h_code = ""
    code3_x = [0] * (level + 1)
    code3_y = [0] * (level + 1)
    code3 = ""
    code9 = ""
    mod_x = h_x
    mod_y = h_y

    for i in range(level + 1):
        h_pow = math.pow(3, level - i)
        if mod_x >= ceil_int(h_pow/2):
            code3_x[i] = 2
            mod_x -= h_pow
        elif mod_x <= -ceil_int(h_pow/2):
            code3_x[i] = 0
            mod_x += h_pow
        else:
            code3_x[i] = 1

        if mod_y >= ceil_int(h_pow/2):
            code3_y[i] =2
            mod_y -= h_pow
        elif mod_y <= -ceil_int(h_pow/2):
             code3_y[i] =0
             mod_y += h_pow
        else:
            code3_y[i] = 1

    for i in range(len(code3_x)):
        code3 += "%s%s" % (code3_x[i], code3_y[i])
        code9 += str(int(code3, 3))
        h_code += code9
        code9 = ""
        code3 = ""

    h_2 = h_code[3:]
    h_1 = h_code[0:3]
    h_a1 = floor_int(int(h_1) / 30)
    h_a2 = int(h_1) % 30
    h_code = (H_KEY[h_a1] + H_KEY[h_a2]) + h_2

    return Zone(z_loc_y, z_loc_x, h_x, h_y, h_code)

def getZoneByCode(code):
    level = len(code)
    h_size =  calcHexSize(level)
    unit_x = 6 * h_size;
    unit_y = 6 * h_size * H_K
    h_x = 0;
    h_y = 0;
    h_dec9 = str(H_KEY.find(code[0]) * 30 + H_KEY.find(code[1]) + int(code[2:]))
    if h_dec9[0] in "15" and h_dec9[1] not in "125" and h_dec9[2] not in "125":
        if h_dec9[0] == '5':
            h_dec9 = "7" + h_dec9[1:len(h_dec9)]
        elif h_dec9[0] == 1:
            h_dec9 = "3" + h_dec9[1:len(h_dec9)]

    d9xlen = len(h_dec9)
    for i in range(level + 1 - d9xlen):
        h_dec9 = "0" + h_dec9
        d9xlen += 1
    h_dec3 = ""
    for i in range(d9xlen):
        h_dec0 = base_convert(int(h_dec9[i]), 3)
        if not h_dec0:
            h_dec3 += "00"
        elif len(h_dec0) == 1:
            h_dec3 += "0"
        h_dec3 += h_dec0;


    h_decx = [0] * (len(h_dec3) / 2)
    h_decy = [0] * (len(h_dec3) / 2)
    
    for i in range(len(h_dec3) / 2):
        h_decx[i] = h_dec3[i * 2]
        h_decy[i] = h_dec3[i * 2 + 1]

    for i in range(level):
        h_pow = math.pow(3, level-i)
        if h_decx[i] == 0:
            h_x -= h_pow
        elif h_decx[i] == 2:
            h_x += h_pow
        if h_decy[i] == 0:
            h_y -= h_pow
        elif h_decy[i] == 2:
            h_y += h_pow

    h_lat_y = (H_K * h_x * unit_x + h_y * unit_y) / 2
    h_lon_x = (h_lat_y - h_y * unit_y) / H_K

    h_loc = xy2loc(h_lon_x, h_lat_y);
    if h_loc.lon > 180:
         h_loc.lon -= 360;
         h_x -= math.pow(3, level)
         h_y += math.pow(3, level)
    elif h_loc.lon < -180:
         h_loc.lon += 360;
         h_x += math.pow(3, level)
         h_y -= math.pow(3, level)
         
    return Zone(h_loc.lat, h_loc.lon, h_x, h_y, code)

def loc2xy(lon, lat):
    x = lon * H_BASE / 180.0
    y = math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / (math.pi / 180.0)
    y *= H_BASE / 180.0
    return Point(x, y)

def xy2loc(x, y):
    lon = (x / H_BASE) * 180
    lat = (y / H_BASE) * 180
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180)) - math.pi / 2)
    return Coord(lon, lat)



