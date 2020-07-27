from numpy import (
    sin, cos, tan,
    arcsin, arccos, arctan2,
    pi
)


# ALL FUCNTIONS ACCEPT DESERIALIZED VALUES IN RADIANS


# function returns local equatorial coordinates
# hour angle is returned in range 0 - 24h
def hor_to_loc_eql(azim, zen_dist, lat):
    sin_dec = sin(lat) * cos(zen_dist) - sin(zen_dist) * cos(lat) * cos(azim)
    dec = arcsin(sin_dec)

    sin_t = - sin(zen_dist) * sin(azim) / cos(dec)
    cos_t = (cos(zen_dist) * cos(lat) + sin(zen_dist)
             * sin(lat) * cos(azim)) / cos(dec)

    t = arctan2(sin_t, cos_t)

    # this maybe unneeded
    if t < 0:
        t + 2 * pi
    elif t > 2 * pi:
        t -= 2 * pi

    return t, dec


def loc_eql_to_hor(hour, dec, lat):
    zen_dist = sin(dec) * sin(lat) + cos(dec) * cos(lat) * cos(hour)
    zen_dist = arccos(zen_dist)

    sin_azim = sin(hour) * cos(dec)
    cos_azim = -(sin(dec) * cos(lat) - sin(lat) * cos(dec) * cos(hour))

    if abs(cos_azim) < 1e-16 and abs(sin_azim) < 1e-16:
        azim = None
    elif abs(cos_azim) < 1e-16 and sin_azim > 0:
        azim = pi / 2
    elif abs(cos_azim) < 1e-16 and sin_azim < 0:
        azim = 1.5 * pi
    else:
        azim = arctan2(sin_azim, cos_azim)

    if azim and azim < 0:
        azim += 2 * pi
    elif azim and azim > 2 * pi:
        azim -= 2 * pi

    return azim, zen_dist


def eql_loc_to_cel(hour, dec, star_time):
    ra = star_time - hour

    if ra < 0:
        ra += 2 * pi
    elif ra > 2 * pi:
        ra -= 2 * pi

    return ra, dec


def eql_cel_to_loc(ra, dec, star_time):
    hour = star_time - ra

    if hour < 0:
        hour += 2 * pi
    elif hour > 2 * pi:
        hour -= 2 * pi

    return hour, dec


def cel_eql_to_hor(ra, dec, star_time, lat):
    hour, dec = eql_cel_to_loc(ra, dec, star_time)

    azim, zen = loc_eql_to_hor(hour, dec, lat)

    return azim, zen


def hor_to_cel_eql(azim, zen_dist, star_time, lat):
    hour, dec = hor_to_loc_eql(azim, zen_dist, lat)

    ra, dec = eql_loc_to_cel(hour, dec, star_time)

    return ra, dec


# TODO: Implement Ecliptic coordinate system transformations
def hor_to_ecl():
    pass


def ecl_to_hor():
    pass


def ecl_to_cel_eql():
    pass


def ecl_to_loc_eql():
    pass


def loc_eql_to_ecl():
    pass


def cel_eql_to_ecl():
    pass