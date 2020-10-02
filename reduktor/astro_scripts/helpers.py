from numpy import degrees as deg, radians
import re
import reduktor.astro_scripts.transformations as trans
import json

# Coordinate system names
NEBESKO_EKVATORSKI = "Nebesko ekvatorski"
MESNO_EKVATORSKI = "Mesno Ekvatorski"
EKLIPTICKI = "Ekliptički"
HORIZONTSKI = "Horizontski"

RA = "rektascenzija"
DEC = "deklinacija"
STAR_TIME = "zvezdano vreme"
LAT = "geografksa širina"
HOUR = "časovni ugao"
E_LAT = "latituda"
E_LONG = "longituda"
AZIM = "azimut"
ZEN_DIST = "zenitksa daljina"

GEO_TOPO = "GEO_TOPO"
NUT = "NUT"
PREC = "PREC"

system_informations = {
    NEBESKO_EKVATORSKI: {
        "inputs": [RA, DEC, STAR_TIME, LAT],
        "outputs": [RA, DEC]
    },
    MESNO_EKVATORSKI: {
        "inputs": [HOUR, DEC, STAR_TIME, LAT],
        "outputs": [HOUR, DEC]
    },
    EKLIPTICKI: {
        "inputs": [E_LONG, E_LAT, STAR_TIME, LAT],
        "outputs": [E_LONG, E_LAT],
    },
    HORIZONTSKI: {
        "inputs": [AZIM, ZEN_DIST, STAR_TIME, LAT],
        "outputs": [AZIM, ZEN_DIST],
    }
}


# transform angle from radians to a string
def serialize(angle, hour=False):
    if not angle:
        return "Nedefinisan"

    angle = deg(angle)

    if hour:
        angle /= 15

    degrees = int(angle)
    minutes = (angle - degrees) * 60
    seconds = (minutes - int(minutes)) * 60
    minutes = int(minutes)

    if hour:
        return f"{degrees}h {minutes}m {seconds:.3f}s"

    return f"{degrees}° {minutes}' {seconds:.3f}\""


# parse an angle represented as a string to a numerical value in radians
def deserialize(angle_str, hour=False):
    if angle_str == "":
        return 0

    pattern = "(\d{1,3})(\.\d*)?[d|D| |°|h|H]?(\d{0,2})(\.\d+)?[m|M| |']?(\d{0,2})(\.\d+)?[s|S| |\"]?"

    match = re.search(pattern, angle_str)

    if not match:
        raise ValueError("Can't match angle format")

    angle = deg_from_groups(match.groups())

    if hour:
        angle *= 15

    angle = radians(angle)

    return angle

def serialize_dict(result_dict):
    for key in result_dict:
        hour = False
        # check if angle should be serialized to hour values
        if key == HOUR or key == RA or key == STAR_TIME:
            hour = True

        result_dict[key] = serialize(result_dict[key], hour=hour)

    return json.dumps(result_dict)


def deserialize_dict(dict_str):
    new_dict = {}

    print(dict_str)


    for key in dict_str:
        hour = False
        if key == HOUR or key == STAR_TIME or key == RA:
            hour = True

        new_dict[key] = deserialize(dict_str[key], hour=hour)

    return new_dict

def from_hour(angle, serialized=False):
    if serialized:
        angle = deserialize(angle)

    angle *= 15

    return angle


def to_hour(angle, serialized=False):
    if serialized:
        angle = deserialize(angle)

    angle /= 15

    return angle


def deg_from_groups(groups):
    angle = 0
    weight = 1

    for i in range(0, len(groups) - 1, 2):
        if groups[i] == '':
            continue

        tmp = float(groups[i])

        if groups[i + 1] and groups[i + 1] != '':
            tmp += float(groups[i + 1])

        angle += tmp / weight
        weight *= 60

    return angle


def get_system_info(system):
    return system_informations[system]


def get_all_systems_info():
    return system_informations


# Ovo ce biti pakleno
def transform_system(data):
    options = data["options"]
    start_name = data["startName"]
    start_data = deserialize_dict(data["startData"])
    end_name = data["endName"]
    # Check if the names are valid
    if start_name not in system_informations or end_name not in system_informations:
        raise ValueError("Unknown coordinate system")

    lat = start_data[LAT]
    start_time = start_data[STAR_TIME]

    # Transform any coordinate system into Celestial equatorial
    ra, dec = any_to_cel(start_name, start_data)
    print(ra, dec)
    # Adjust coordinates for nutation, precession...
    ra, dec = adjust_to_now(ra, dec, lat, options)
    print(ra, dec)
    # Transform those coordinates to the output system
    result = cel_to_any(end_name, ra, dec, start_data)


    # Serialize the results
    result = serialize_dict(result)


    return result


def any_to_cel(sys_name, sys_data):
    star_time = sys_data[STAR_TIME]
    lat = sys_data[LAT]

    if sys_name == NEBESKO_EKVATORSKI:
        return sys_data[RA], sys_data[DEC]
    elif sys_name == MESNO_EKVATORSKI:
        return trans.eql_loc_to_cel(sys_data[HOUR], sys_data[DEC], star_time)
    elif sys_name == HORIZONTSKI:
        return trans.hor_to_cel_eql(sys_data[AZIM], sys_data[ZEN_DIST], star_time, lat)
    elif sys_name == EKLIPTICKI:
        return trans.ecl_to_cel_eql()
    else:
        raise ValueError("Unknown coordinate system (any_to_cel)")


def cel_to_any(sys_name, ra, dec, start_data):
    result = {}

    if sys_name == NEBESKO_EKVATORSKI:
        result[RA] = ra
        result[DEC] = dec
    elif sys_name == MESNO_EKVATORSKI:
        result[HOUR], result[DEC] = trans.eql_cel_to_loc(ra, dec, start_data[STAR_TIME])
    elif sys_name == HORIZONTSKI:
        result[AZIM], result[ZEN_DIST] = trans.cel_eql_to_hor(ra, dec, start_data[STAR_TIME], start_data[LAT])
    elif sys_name == EKLIPTICKI:
        result[E_LONG], result[E_LAT] = trans.cel_eql_to_ecl()
    else:
        raise ValueError("Unknown system (cel_to_any)")

    return result


def adjust_to_now(ra, dec, lat, options):
    if options[GEO_TOPO]:
        geo_topo = deserialize_dict(options[GEO_TOPO])

        r = geo_topo["r"]
        h = geo_topo["h"]
        lon = geo_topo["lon"]

        ra, dec = trans.geo_topo(ra, dec, r, lat, lon, h)

    if PREC in options:
        date = options[PREC]["date"] + " " + options[PREC]["time"] + ":00";
        ra, dec = trans.precession(ra, dec, date)

    if NUT in options:
        date = options[NUT]["date"] + " " + options[NUT]["time"] + ":00";
        ra, dec = trans.nutation(ra, dec, date)
        

    return ra, dec



