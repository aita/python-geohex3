# coding: utf-8
# GeoHex by @sa2da (http://geogames.net) is licensed under Creative Commons BY-SA 2.1 Japan License.

import math

def round_int(n):
    return int(round(n))

def floor_int(n):
    return int(math.floor(n))

def ceil_int(n):
    return int(math.ceil(n))

def base_convert(temp, base):
    dchar = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    result = []
    while temp != 0:
        result.append(dchar[temp % base])
        temp /= base
    return ''.join(reversed(result))

