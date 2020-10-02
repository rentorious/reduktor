import numpy as np
from astropy.time import Time
from astroquery.jplhorizons import Horizons
from numpy import (
    sin,
    cos,
    arcsin,
    arccos,
    sqrt
)
radsec=206264.8062470952



def precession(a0, d0, t2):

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
    
    # a0 i d0 u radijanima, time u formatu '2019-05-17 15:55:23'    
    # funkcija vraca a i d u radijanima
        
    jd = Time(time).jd
    t = (jd - 2451545)/36525
    kl, klp, kf, kd, komega, kai, bi, kci, di = np.loadtxt('nut.dat', unpack = True, max_rows = 30)
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
    
    kl, klp, kf, kd, komega, kai, bi, kci, di = np.loadtxt('nut.dat', unpack = True, skiprows = 30)
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

