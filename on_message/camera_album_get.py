import json
import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from service.camera import (
    get_album_exist_years,
    get_album_exist_months,
    get_album_exist_days,
    get_album_pictures,
)
"""
# message 
type: json str
-----
{
    "camera_id": "camera_id",
    "year": 2020,
    "month": 8,
    "day": 10
}
"""
def get_album(message: str) -> dict:
    req = json.loads(message)

    camera_id = req['camera_id']
    year = req['year']
    month = req['month']
    day = req['day']

    if year is None:
        return get_album_exist_years(camera_id)
    elif month is None:
        # year is not None. month is None
        return get_album_exist_months(camera_id, year)
    elif day is None:
        # year and month is not None. day is None
        return get_album_exist_days(camera_id, year, month)
    else:
        # year and month and day is not None.
        return get_album_pictures(camera_id, year, month, day)
