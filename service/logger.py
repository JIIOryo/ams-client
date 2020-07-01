import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from lib.color import Color, color_text

DEBUG = "DEBUG"
INFO = "INFO"
WARN = "WARN"
ERROR = "ERROR"
FATAL = "FATAL"

LOG_LEVEL = {
    "DEBUG": {
        "LEVEL": 1,
        "COLOR": Color.CYAN
    },
    "INFO": {
        "LEVEL": 2,
        "COLOR": Color.GREEN
    },
    "WARN": {
        "LEVEL": 3,
        "COLOR": Color.YELLOW
    },
    "ERROR": {
        "LEVEL": 4,
        "COLOR": Color.RED
    },
    "FATAL": {
        "LEVEL": 5,
        "COLOR": Color.PURPLE
    },
}
MIN_FILE_OUTPUT_LEVEL = 2

