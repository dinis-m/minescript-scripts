from time import sleep

from minescript import echo, player_press_use
from minescript_plus import Screen

from rotation_1 import look_at_block
from inventory_handle import fill_to_target, inventory_count

from melon_pumpkin_trades.trade_config import TradeConfig
from melon_pumpkin_trades.movement import go_to_storage_area
from melon_pumpkin_trades.script_utils import decho


def has_required_trade_items(config: TradeConfig) -> bool:
    return all(
        inventory_count(item) >= config.target_per_item
        for item in config.trade_items
    )


def open_chest_and_fill(
    chest_pos: tuple[int, int, int],
    item_name: str,
    target_amount: int,
) -> bool:
    look_at_block(*chest_pos)
    player_press_use(True)

    Screen.wait_screen()

    filled = fill_to_target(item_name, target_amount)

    sleep(0.15)
    Screen.close_screen()

    return filled


def ensure_trade_items(config: TradeConfig) -> None:
    echo(
        f"Require {config.target_per_item} total\n"
        f"{list(config.trade_items)}\n"
        f"Require {config.required_stacks} stacks rounded each"
    )

    if has_required_trade_items(config):
        return

    go_to_storage_area(config)

    while not has_required_trade_items(config):
        sleep(0.05)

        pumpkins_filled = open_chest_and_fill(
            config.pumpkin_chest,
            config.trade_items[0],
            config.target_per_item,
        )

        decho(f"Pumpkins filled: {inventory_count(config.trade_items[0])}")

        melons_filled = open_chest_and_fill(
            config.melon_chest,
            config.trade_items[1],
            config.target_per_item,
        )

        decho(f"Melons filled: {inventory_count(config.trade_items[1])}")

        if pumpkins_filled and melons_filled:
            break