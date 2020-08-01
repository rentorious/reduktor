from numpy import degrees as deg, radians
import re
import reduktor.astro_scripts.transformations as trans
import json

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
    start_name = data["startName"]
    start_data = data["startData"]
    endName = data["endName"]

    # Check if the names are valid
    if start_name not in system_informations or endName not in system_informations:
        raise ValueError("Unknown coordinate system")

    # Transform any coordinate system into Celestial equatorial
    ra, dec = any_to_cel(start_name, start_data)


    result = {}


    # Serialize the results
    for key in result:
        hour = False
        # check if angle should be serialized to hour values
        if key == HOUR or key == RA or key == STAR_TIME:
            hour = True

        result[key] = serialize(result[key], hour=hour)

    print(json.dumps(result))
    return json.dumps(result)

def any_to_cel(sys_name, sys_data):
    star_time = sys_data[STAR_TIME]
    lat = sys_data[LAT]