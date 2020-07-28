import helpers as hlp
import transformations as trans
import numpy as np


lat = hlp.deserialize("55 45.5")
star_time = hlp.deserialize("5h15m", hour=True)
re = hlp.deserialize("14h12.8m", hour=True)
dec = hlp.deserialize("19d30.3'")

# print(hlp.serialize(lat))
# print(hlp.serialize(star_time, hour=True))
# print(hlp.serialize(re, hour=True))
# print(hlp.serialize(dec))

print(lat)
print(star_time)
print(re)
print(dec)

azim, zen_dist = trans.cel_eql_to_hor(re, dec, star_time, lat)

print("z:", hlp.serialize(zen_dist))
print("A:", hlp.serialize(azim))
