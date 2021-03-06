from numpy import (
    sin, cos, tan,
    arcsin, arccos, arctan2,
    pi, e,
    sqrt
)
import numpy as np
from astropy.time import Time
from astroquery.jplhorizons import Horizons

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


def geo_topo(ra, dec, r, lat, lon, h):
    f = 1 / 298.28642  # Earth flattening factor
    a = 6378.1366  # Earth radius (km)
    e = sqrt(2 * f - f ** 2)  # Eccentricity

    # ra, dec, lat, lon (radians)
    # h, r (km)

    N = a / sqrt(a - e ** 2 * sin(lat) ** 2)

    x_t = r * cos(dec) * cos(ra) - (N + h) * cos(lat) * cos(lon)
    y_t = r * cos(dec) * sin(ra) - (N + h) * cos(lat) * sin(lon)
    z_t = r * sin(dec) - ((1 - e ** 2) * N + h) * sin(lat)

    r_t = sqrt(x_t ** 2 + y_t ** 2 + z_t ** 2)
    dec_t = arcsin(z_t / r_t)
    ra_t = arctan2(y_t, x_t)

    if ra_t < 0:
        ra_t += 2 * pi

    return ra_t, dec_t


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


def precession(a0, d0, t2):
    radsec=206264.8062470952

    # a0 i d0 u radijanima, t2 u formatu '2019-05-17 15:55:23'    
    # funkcija vraca a i d u radijanima
    
    t1 = Time(t2[:5] + '01-01 00:00:00').jd
    t2 = Time('2019-05-17 15:55:23').jd
    t=(t1-2451545.0)/36525 
    tau=(t2-t1)/36525
    
    # Jednacine 6.21 i 6.36 iz knjige "Explanatory Supplement to the Astronomical Almanac - THIRD EDITION"
    zeta = (23035.545 + 139.72 * t + 0.06 * t**2) * tau + (30.24 - 0.27 * t) * tau**2 + 17.995 * tau**3
    z = (23035.545 + 139.72 * t + 0.06 * t**2) * tau + (109.48 + 0.39 * t) * tau**2 + 18.325 * tau**3
    teta = (20051.12 - 85.29 * t - 0.37 * t**2) * tau + (-42.65 - 0.37 * t) * tau**2 - 41.80 * tau**3
    
    #conversion to radians
    zeta /= radsec
    z /= radsec
    teta /= radsec
    
    p11 = cos(z)*cos(teta)*cos(zeta) - sin(z)*sin(zeta)
    p12 = -cos(z)*cos(teta)*sin(zeta) - sin(z)*cos(zeta)
    p13 = -cos(z)*sin(teta)
    p21 = sin(z)*cos(teta)*cos(zeta) + cos(z)*sin(zeta)
    p22 = -sin(z)*cos(teta)*sin(zeta) + cos(z)*cos(zeta)
    p23 = -sin(z)*sin(teta)
    p31 = sin(teta)*cos(zeta)
    p32 = -sin(teta)*sin(zeta)
    p33 = cos(teta)
    
    P = [[p11, p12, p13],
        [p21, p22, p23],
        [p31, p32, p33]]
        
    s0 = np.array([[cos(d0)*cos(a0)],
        [cos(d0)*sin(a0)],
        [sin(d0)]])
        
    s = np.dot(P,s0)
    d = np.arcsin(s[2][0])
    a = np.arctan2(s[1][0], s[0][0])
    
    return a, d 

def nutation(a0, d0, time):
    radsec=206264.8062470952
    # a0 i d0 u radijanima, time u formatu '2019-05-17 15:55:23'    
    # funkcija vraca a i d u radijanima
        
    jd = Time(time).jd
    t = (jd - 2451545)/36525
    kl, klp, kf, kd, komega, kai, bi, kci, di = np.loadtxt('reduktor/astro_scripts/nut.dat', unpack = True, max_rows = 30)
    ai = kai*1e-4
    bi = bi*1e-4
    ci = kci*1e-4
    di = di*1e-4 
    
    al = (485866.733 + (1325*1296000+715922.633)*t + 31.310*t**2 + 0.064*t**3)/radsec
    alp = (1287099.804 + (99*1296000 + 1292581.224)*t - 0.577*t**2-0.012*t**3)/radsec
    f = (335778.877 +(1342*1296000 + 295263.137)*t - 13.257*t**2+0.011*t**3)/radsec
    d = (1072261.307 + (1236*1296000 + 1105601.328)*t - 6.891*t**2+0.019*t**3)/radsec
    omega = (450160.280 - (5*1296000 + 482890.539 )*t + 7.455*t**2+0.008*t**3)/radsec
    
    deltapsi = np.sum((ai+bi*t)*sin(kl*al+klp*alp+kf*f+kd*d+komega*omega))/radsec
    deltaeps = np.sum((ci+di*t)*cos(kl*al+klp*alp+kf*f+kd*d+komega*omega))/radsec
    
    kl, klp, kf, kd, komega, kai, bi, kci, di = np.loadtxt('reduktor/astro_scripts/nut.dat', unpack = True, skiprows = 30)
    ai = kai*1e-4
    bi = bi*1e-4
    ci = kci*1e-4
    di = di*1e-4 
    dpsi = np.sum((ai+bi*t)*sin(kl*al+klp*alp+kf*f+kd*d+komega*omega))/radsec
    deps = np.sum((ci+di*t)*cos(kl*al+klp*alp+kf*f+kd*d+komega*omega))/radsec
    eps = ((23*3600+26*60+21.448-46.8150*t-0.00059*t**2+0.001813*t**3))/radsec
    
    n11 = cos(deltapsi+dpsi)
    n12 = -cos(eps)*sin(deltapsi+dpsi)
    n13 = -sin(eps)*sin(deltapsi+dpsi)
    n21 = cos(eps+deltaeps+deps)*sin(deltapsi+dpsi)
    n22 = cos(eps)*cos(eps+deltaeps+deps)*cos(deltapsi+dpsi)+sin(eps)*sin(eps+deltaeps+deps)                     
    n23 = sin(eps)*cos(eps+deltaeps+deps)*cos(deltapsi+dpsi)-cos(eps)*sin(eps+deltaeps+deps)
    n31 = sin(eps+deltaeps+deps)*sin(deltapsi+dpsi)
    n32 = cos(eps)*sin(eps+deltaeps+deps)*cos(deltapsi+dpsi)-sin(eps)*cos(eps+deltaeps+deps)                    
    n33 = sin(eps)*sin(eps+deltaeps+deps)*cos(deltapsi+dpsi)+cos(eps)*cos(eps+deltaeps+deps)
    
    
    N = [[n11, n12, n13],
        [n21, n22, n23],
        [n31, n32, n33]]
        
    s0 = np.array([[cos(d0)*cos(a0)],
        [cos(d0)*sin(a0)],
        [sin(d0)]])
        
    s = np.dot(N,s0)
    d = np.arcsin(s[2][0])
    a = np.arctan2(s[1][0], s[0][0])
    
    return a, d