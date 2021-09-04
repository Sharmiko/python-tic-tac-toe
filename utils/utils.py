import curses
from typing import Union, List

from conf import DEFAULT_ENCODING


std_scr = curses.initscr()
curses.echo()
curses.cbreak()


def print_flush(sequence: Union[List, str]) -> None:
    std_scr.clear()
    if isinstance(sequence, str):
        std_scr.addstr(0, 0, sequence)
        std_scr.refresh()
    elif isinstance(sequence, list):
        for idx, line in enumerate(sequence):
            std_scr.addstr(idx, 0, line)
        std_scr.refresh()


def std_input() -> str:
    res = std_scr.getstr()
    return res.decode(encoding=DEFAULT_ENCODING)


def reset_scr():
    curses.nocbreak()
    std_scr.keypad(False)
    curses.echo()
    curses.endwin()
