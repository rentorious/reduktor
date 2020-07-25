import numpy as np
import re


# transform angle from radians to a string
def serialize(angle, hour=False):
    angle = np.degrees(angle)

    if hour:
        angle /= 15

    degrees = int(angle)
    minutes = (angle - degrees) * 60
    seconds = (minutes - int(minutes)) * 60
    minutes = int(minutes)

    return f"{degrees}° {minutes}' {seconds}\""


# parse an angle represented as a string to a numerical value in radians
def deserialize(angle_str, hour=False):
    pattern = "(\d{1,3})(\.\d*)?[d|D| |°|h|H]?(\d{0,2})(\.\d+)?[m|M| |']?(\d{0,2})(\.\d+)?[s|S| |\"]?"

    match = re.search(pattern, angle_str)

    if not match:
        raise ValueError("Can't match angle format")

    angle = deg_from_groups(match.groups())

    if hour:
        angle *= 15

    angle = np.radians(angle)

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
