from . import building_data_requests as bdr

import pandas as pd
import pathlib

# import numbers
# import time

cd = pathlib.Path(__file__).parent
data_key = pd.read_csv(str(cd / "ahs_air.csv"))


def temp_room(room_number) -> float:
    """
    :param room_number: Number of room to get temperature from
    :return: Temperature of room in degrees Fahrenheit
    """
    room_key = data_key.loc[data_key["Label"] == str(room_number)]
    return bdr.get_value(
        room_key['Facility'],
        room_key['Temperature'])[0]  # returns only first item in tuple


def temp_wing(floor, wing) -> float:
    """
    :param floor: Floor of school
    :param wing: Wing of floor to average room temperatures (all = 0, west = 1, north = 2, east = 3, south = 4)
    :return: Average temperature of wing
    """
    average_temp = 0.0  # type: float
    wing_key = pd.DataFrame()
    # declare lists of wing row ranges
    floor2 = [[24, 109], [24, 33], [34, 50], [51, 63],
              [64, 72]]  # all, 201-215, 217-235, 237-253, 255-260
    floor3 = [[110, 170], [110, 121], [122, 139], [140, 148],
              [149, 157]]  # all, 301-313, 315-333, 335-351, 353-369

    if floor == 2:
        wing_key = data_key.truncate(*(floor2[wing]))
    elif floor == 3:
        wing_key = data_key.truncate(*(floor3[wing]))

    room_count = 0  # type: int
    for index, row in wing_key.iterrows():
        temp_value = bdr.get_value(row["Facility"], row["Temperature"])[0]
        if temp_value is not None and temp_value != 0.0:
            average_temp += temp_value
            room_count += 1
    average_temp /= room_count

    return average_temp
