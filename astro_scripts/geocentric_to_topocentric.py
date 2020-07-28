import numpy as np
from numpy import (
    sqrt,
    sin,
    cos,
    tan,
    arccos,
    arcsin,
    arctan2,
)
import math

f = 1 / 298.28642 # Earth flattening factor
a = 6378.1366 # Earth radius (km)
e = sqrt(2 * f - f**2) # Eccentricity

def geo_to_topo(ra, dec, r, lat, lon, h):

    # ra, dec, lat, lon (radians)
    # h, r (km)

    N = a / sqrt(a - e**2 * sin(lat)**2)

    x_t = r * cos(dec) * cos(ra) - (N + h) * cos(lat) * cos(lon)
    y_t = r * cos(dec) * sin(ra) - (N + h) * cos(lat) * sin(lon)
    z_t = r * sin(dec) - ((1 - e**2) * N + h) * sin(lat)

    r_t = sqrt(x_t**2 + y_t**2 + z_t**2)
    dec_t = arcsin(z_t / r_t)
    ra_t = arctan2(y_t, x_t)

    if ra_t < 0:
        ra_t += 2*np.pi

    return ra_t, dec_t
