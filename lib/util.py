from typing import List, Tuple
import datetime
import hashlib
import json
import os

import requests

def formated_str_now_date():
    return datetime.datetime.now().strftime('%m/%d %H:%M')

def least_squares(data: List[List[int]]) -> Tuple[int, int]:
    """
    Parameters
    ----------
    data : list[list]
        list of { list of raw sensor value and theoretical value }
        e.g. 
        data = [
            [740, 23],
            [750, 23.2],
            [760, 23.34],
            ...
        ]

    Returns
    ----------
    int
        a
    int
        b
        [expected value] = a * [raw sensor value] + b
    """
    sum_xy = sum_x = sum_y = sum_x2 = 0
    N = len(data)

    for x_y in data:
	    sum_xy += x_y[0] * x_y[1]
	    sum_x += x_y[0]
	    sum_y += x_y[1]
	    sum_x2 += x_y[0] ** 2	
    
    a = (N * sum_xy - sum_x * sum_y)/float(N * sum_x2 -  sum_x ** 2)
    b = (sum_x2 * sum_y - sum_xy * sum_x)/float(N * sum_x2 - sum_x ** 2)

    return a, b

def get_now_device_should_be_on_by_timer(on_hour: int, on_minute: int, off_hour: int, off_minute: int) -> bool:
    device_on_time = datetime.time(hour = on_hour, minute = on_minute)
    device_off_time = datetime.time(hour = off_hour, minute = off_minute)
    now_time = datetime.datetime.now().time()

    on_and_off_times = [device_on_time, device_off_time]

    if min(on_and_off_times) <= now_time < max(on_and_off_times):
        return device_on_time < device_off_time
    return device_off_time <= device_on_time

def connected_to_internet(url: str, timeout: int):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        pass
    return False

def timeout_time_generator(default: float, default_repeat_times: int, r: float, th: int) -> float:
    timeout = default
    # step 1
    for _ in range(default_repeat_times): yield timeout
    # step 2
    while timeout < th:
        timeout *= r
        yield timeout
    # step 3
    while True: yield timeout

def make_dir(dir_path: str) -> bool:
    # dir already exist
    if os.path.isdir(dir_path):
        return False
    
    # make new dir
    os.makedirs(dir_path)
    return True

def is_exist_file(file_path: str) -> bool:
    return os.path.isfile(file_path)

def ls(path: str) -> list:
    return os.listdir(path)

def get_json_file(file_path: str) -> dict:
    with open(file_path) as f:
        return json.load(f)

def set_json_file(file_path: str, data: dict) -> None:
    with open(file_path, 'w') as f:
        json.dump(data, f, indent = 4)

def generate_md5_hash(key: str) -> str:
    return hashlib.md5(key.encode()).hexdigest()

def zero_padding(num: int, length: int) -> str:
    return str(num).zfill(length)

def zero_padding_month(month: int) -> str:
    if not 1 <= month <= 12:
        raise ValueError('This month does not meet 1 <= month <= 12')

    return zero_padding(month, 2)

# foo[bar]baz -> foo{bar}baz
def bracket_to_brace(text: str) -> str:
    return text.replace('[', '{').replace(']', '}')
