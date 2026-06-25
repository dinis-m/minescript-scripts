from time import sleep

from minescript import execute, echo, player_press_forward
from minescript_plus import Screen

import pathfinding as p

from melon_pumpkin_trades.trade_config import TradeConfig
from melon_pumpkin_trades.script_utils import wait_until_position


def teleport_to_base(config: TradeConfig) -> None:
    Screen.close_screen()

    echo("DONT MOVE")
    sleep(0.5)

    player_press_forward(False)
    sleep(0.5)

    if config.teleport_command:
        execute(config.teleport_command)

    wait_until_position(config.base_pos)

    player_press_forward(True)


def go_to_storage_area(config: TradeConfig) -> None:
    execute(config.teleport_command)

    wait_until_position(config.base_pos)

    sleep(0.5)

    p.pathfind_to(*config.storage_path_pos)

    wait_until_position(*config.storage_valid_positions)


def go_to_crafting_area(config: TradeConfig) -> None:
    p.pathfind_to(*config.craft_path_pos)
    wait_until_position(config.craft_wait_pos)


def go_to_bed(config: TradeConfig) -> None:
    p.pathfind_to(*config.bed_path_pos)