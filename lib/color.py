import sys

import pathlib
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append( str(current_dir) + '/../' )

from commons.consts import (
    LOG_TITLE_MAX_CHAR_NUM,
)

class Color:
    BLACK     = '\033[30m'
    RED       = '\033[31m'
    GREEN     = '\033[32m'
    YELLOW    = '\033[33m'
    BLUE      = '\033[34m'
    PURPLE    = '\033[35m'
    CYAN      = '\033[36m'
    WHITE     = '\033[37m'
    END       = '\033[0m'
    BOLD      = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE   = '\033[07m'

def color_text(text: str, color: str) -> str:
    """
    color text

    Parameters
    ----------
    text: str
        text
    title_color: str
        Color.color

    Returns
    ----------
    str
        colored text
    """
    return color + text + Color.END

def print_color_log(title: str, title_color: str, text: str) -> None:
    """
    print color log

    Parameters
    ----------
    title: str
        consts.LOG_TITLE
    title_color: str
        color.Color
    text: str
    """
    if len(title) > LOG_TITLE_MAX_CHAR_NUM:
        raise ValueError('Title must be smaller than {num}'.format(num = LOG_TITLE_MAX_CHAR_NUM))
    
    print( color_text( title + ' ' * (LOG_TITLE_MAX_CHAR_NUM - len(title)) + '|', title_color) + ' ' + text)
