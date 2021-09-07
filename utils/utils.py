import curses

from conf import DEFAULT_ENCODING


std_scr = curses.initscr()
curses.echo()
curses.cbreak()


def print_flush(text: str) -> None:
    std_scr.clear()
    if isinstance(text, str):
        std_scr.addstr(0, 0, text)
        std_scr.refresh()


def std_input() -> str:
    res = std_scr.getstr()
    return res.decode(encoding=DEFAULT_ENCODING)


def reset_scr():
    curses.nocbreak()
    std_scr.keypad(False)
    curses.echo()
    curses.endwin()
