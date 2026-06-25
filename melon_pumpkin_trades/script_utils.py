from time import sleep
from threading import Thread

from minescript import echo, execute, player_position, screen_name


DEBUG = False


def decho(*args) -> None:
    if DEBUG:
        echo(*args)


def player_block_pos() -> tuple[int, int, int]:
    return tuple(int(float(str(x))) for x in player_position())


def wait_until_position(
    *valid_positions: tuple[int, int, int],
    poll_seconds: float = 0.05,
) -> None:
    valid = set(valid_positions)

    while player_block_pos() not in valid:
        sleep(poll_seconds)


def start_exit_watcher() -> None:
    def exit_script() -> None:
        while True:
            if screen_name() == "Game Menu":
                execute(r"\killjob -1")
                return

            sleep(0.1)

    Thread(target=exit_script, daemon=True).start()


def announce_once(message: str, flag: bool) -> bool:
    if not flag:
        echo(message)
        return True

    return flag