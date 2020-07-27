from numpy import degrees as deg, radians
import re
import json
import astro_scripts.transformations as trans

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


# TODO: IMPLEMENT EQUATORIAL
# Ovo ce biti pakleno
def transform_system(data):
    startName = data["startName"]
    startData = data["startData"]
    endName = data["endName"]

    # Check if the names are valid
    if startName not in system_informations or endName not in system_informations:
        raise ValueError("Unknown coordinate system")

    result = {}

    # Check all system transformation combinations
    if startName == NEBESKO_EKVATORSKI:
        # Load and deserialize
        ra = deserialize(startData[RA], hour=True)
        dec = deserialize(startData[DEC])
        star_time = deserialize(startData[STAR_TIME], hour=True)
        lat = deserialize(startData[LAT])

        print(ra, dec, star_time, lat)

        # Check which system is chosen for output
        if endName == MESNO_EKVATORSKI:
            result[HOUR], result[DEC] = trans.eql_cel_to_loc(ra, dec, star_time)
        elif endName == HORIZONTSKI:
            result[AZIM], result[ZEN_DIST] = trans.cel_eql_to_hor(ra, dec, star_time, lat)
        elif endName == EKLIPTICKI:
            result[E_LONG] = result[E_LAT] = 0
    elif startName == MESNO_EKVATORSKI:
        # load and deserialize
        hour = deserialize(startData[HOUR], hour=True)
        dec = deserialize(startData[DEC])
        star_time = deserialize(startData[STAR_TIME], hour=True)
        lat = deserialize(startData[LAT])

        # Check which system is chosen for output
        if endName == NEBESKO_EKVATORSKI:
            result[RA], result[DEC] = trans.eql_loc_to_cel(hour, dec, star_time)
        elif endName == HORIZONTSKI:
            result[AZIM], result[ZEN_DIST] = trans.loc_eql_to_hor(hour, dec, lat)
        elif endName == EKLIPTICKI:
            result[E_LONG], result[E_LAT] = trans.loc_eql_to_ecl()
    elif startName == HORIZONTSKI:
        # load and deserialize
        azim = deserialize(startData[AZIM])
        zen_dist = deserialize(startData[ZEN_DIST])
        star_time = deserialize(startData[STAR_TIME])
        lat = deserialize(startData[LAT])

        # Check which system is chosen for output
        if endName == NEBESKO_EKVATORSKI:
            result[RA], result[DEC] = trans.hor_to_cel_eql(azim, zen_dist, star_time, lat)
        elif endName == MESNO_EKVATORSKI:
            result[HOUR], result[DEC] = trans.hor_to_loc_eql(azim, zen_dist, lat)
        elif endName == HORIZONTSKI:
            result[E_LONG], result[E_LAT] = trans.hor_to_ecl()
    elif startName == EKLIPTICKI:
        # load and deserialize
        e_long = deserialize(startData[E_LONG])
        e_lat = deserialize(startData[E_LAT])
        star_time = deserialize(startData[STAR_TIME], hour=True)
        lat = deserialize(startData[LAT])

        # Check which system is chosen for output
        if endName == NEBESKO_EKVATORSKI:
            result[RA], result[DEC] = trans.ecl_to_cel_eql()
        elif endName == MESNO_EKVATORSKI:
            result[HOUR], result[DEC] = trans.ecl_to_loc_eql()
        elif endName == HORIZONTSKI:
            result[AZIM], result[ZEN_DIST] = trans.ecl_to_hor()

    # Serialize the results
    for key in result:
        hour = False
        # check if angle should be serialized to hour values
        if key == HOUR or key == RA or key == STAR_TIME:
            hour = True

        print(key)
        result[key] = serialize(result[key], hour=hour)

    return result
