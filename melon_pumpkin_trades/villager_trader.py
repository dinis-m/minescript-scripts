from time import sleep

from minescript import (
    flush,
    player_get_targeted_entity,
    player_press_forward,
    player_press_use,
    screen_name,
)

from minescript_plus import Screen, Inventory

from rotation_1 import rotate_relative, look_at_block
from trade_process import process_trade
from inventory_handle import get_slots
from melon_pumpkin_trades.craft_items import craft_items

from melon_pumpkin_trades.trade_config import TradeConfig
from melon_pumpkin_trades.movement import teleport_to_base, go_to_crafting_area
from melon_pumpkin_trades.script_utils import decho


def entity_block_pos(entity) -> tuple[int, int, int]:
    return tuple(int(float(str(x))) for x in entity.position)


def get_targeted_villager(config: TradeConfig):
    entity = player_get_targeted_entity(max_distance=2)

    if entity is None:
        return None

    if entity.name != config.villager_type:
        return None

    return entity


def trade_with_open_villager(config: TradeConfig) -> None:
    player_press_use(True)
    Screen.wait_screen()

    for item in config.trade_items:
        process_trade(item)

    sleep(0.05)
    Screen.close_screen()


def craft_and_store_emerald_blocks(config: TradeConfig) -> None:
    go_to_crafting_area(config)

    look_at_block(*config.craft_block)

    decho("Attempting to craft emerald blocks")
    craft_items(config.emerald_block)

    look_at_block(*config.emerald_storage_chest)
    player_press_use(True)

    Screen.wait_screen()

    slots = get_slots(config.emerald_block)
    decho(f"Emerald block slots: {slots}")

    for slot in slots:
        sleep(0.1)
        Inventory.shift_click_slot(slot)

    Screen.close_screen()


def trade_round(config: TradeConfig) -> None:
    teleport_to_base(config)

    first_villager_pos = None
    last_villager_pos = None

    while True:
        flush()

        if screen_name() == "Crafting":
            return

        villager = get_targeted_villager(config)

        if villager is None:
            sleep(0.05)
            continue

        current_villager_pos = entity_block_pos(villager)

        if current_villager_pos == last_villager_pos:
            rotate_relative(90, 0)
            sleep(0.05)
            continue

        last_villager_pos = current_villager_pos
        player_press_forward(False)

        if first_villager_pos == current_villager_pos:
            craft_and_store_emerald_blocks(config)
            return

        trade_with_open_villager(config)

        if first_villager_pos is None:
            first_villager_pos = current_villager_pos
            decho("First villager logged")

        player_press_forward(True)
        sleep(0.4)