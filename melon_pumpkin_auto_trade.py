"""
    Autonomous melon and pumpkin trading script for 1.21+ versions of Minecraft. 
    Trades with farmers to acquire emeralds, then crafts them into blocks. 
    Must set a teleportation point to the villagers.
"""
from minescript import echo, entities, execute, flush, player_position, player_press_forward, player_press_use, player_get_targeted_entity, screen_name, world_info
from minescript_plus import Screen, Inventory
from rotation_1 import rotate_relative, look_at_block
from trade_process import process_trade
from inventory_handle import fill_to_target, inventory_count, get_slots
from craft_items import craft_items
import pathfinding as p
from time import sleep

VERSION = "1.4.3"
MAX_TRADES = 12
VILLAGER_COUNT = 63
echo(f"Melon and Pumpkin Auto Trade Script v{VERSION}")
# TODO: complete autonomous functionality of script: 
# auto craft emerald blocks. Done
# sleeping when night.
# repeat entire script once, if activated during the day. Done

target = VILLAGER_COUNT * MAX_TRADES
cost_name = ["minecraft:pumpkin", "minecraft:melon"]
villager_type = "Farmer"
teleport_spot = "/home farmers"
pumpkin_chest = [-2182, 49, 1065]
melon_chest = [-2182, 49, 1066]
craft_spot = [-2174, 50, 1064, True]
bed_spot = [-2175, 50, 1067, True]
bed = [-2176, 50, 1069]
trades_today = 0
warned = False
sleeping = False
last_ticks = world_info().day_ticks

# Set True to debug
debug = False

def decho(*args):
    if debug:
        echo(*args)

def check_inv():
    complete = False
    if inventory_count(cost_name[0]) >= target and inventory_count(cost_name[1]) >= target:
        complete = True
    else:
        execute(teleport_spot)
        while not [int(float(str(x))) for x in player_position()] == [-2176, 49, 1059]:
            sleep(0.05)
        sleep(0.5)
        p.pathfind_to(-2181, 50, 1064, True)
        while not [int(x) for x in player_position()] == [-2181, 50, 1064] or [int(x) for x in player_position()] == [-2180, 50, 1064]:
            sleep(0.05)
    echo(f"Require {target} total \n{cost_name} \nRequire {(target + 63 ) // 64} stacks(rounded) each")
    # get items from chests until target is reached
    # BUG: sometimes will infinitely loop melons chest, maybe add inventory checking helper function to fix? will fix in future update
    while not complete:
        sleep(0.05)
        # open container and fill inventory with pumpkins
        look_at_block(pumpkin_chest[0], pumpkin_chest[1], pumpkin_chest[2])
        player_press_use(True)
        Screen.wait_screen()
        pumpkins = fill_to_target(cost_name[0], target)
        decho(f"pumpkins filled: {inventory_count(cost_name[0])}")
        sleep(0.15)
        # open container and fill inventory with melons
        look_at_block(melon_chest[0], melon_chest[1], melon_chest[2])
        player_press_use(True)
        Screen.wait_screen()
        melons = fill_to_target(cost_name[1], target)
        decho(f"melons filled: {inventory_count(cost_name[1])}")
        complete = pumpkins and melons

def teleport_to_base_point(teleport_to):
        Screen.close_screen()
        echo("DONT MOVE")
        sleep(0.5)
        player_press_forward(False)
        sleep(0.5)
        if teleport_to != "":
            execute(teleport_to)
        while not [int(float(str(x))) for x in player_position()] == [-2176, 49, 1059]:
            sleep(0.05)
        player_press_forward(True)

def trade():
    pre_trade = [x.position for x in entities(name=villager_type, max_distance=1.4)]
    first_trade: list[int] = []
    trading = True

    teleport_to_base_point(teleport_spot)

    while True:
        flush()

        if screen_name() == "Crafting":
            break

        try:
            if player_get_targeted_entity(max_distance=2) is not None:
                if player_get_targeted_entity(max_distance=2).name == villager_type: # type: ignore
                    if player_get_targeted_entity(max_distance=2) is not None:
                        if player_get_targeted_entity().position != pre_trade: # type: ignore
                            pre_trade = player_get_targeted_entity().position # type: ignore
                            player_press_forward(False)
                            if first_trade == [int(float(str(x))) for x in pre_trade]:
                                p.pathfind_to(*craft_spot)
                                # wait until player is in position
                                while not [int(float(str(x))) for x in player_position()] == [-2173, 50, 1064]:
                                    sleep(0.05)
                                look_at_block(-2173, 50, 1064)
                                decho("attempting to craft")
                                craft_items("minecraft:emerald_block")
                                look_at_block(-2173, 50, 1066)
                                player_press_use(True)
                                Screen.wait_screen()
                                slots = get_slots("minecraft:emerald_block")
                                decho(f"slots: {slots}")
                                for slot in range(len(slots)):
                                    sleep(0.1)
                                    Inventory.shift_click_slot(slots[slot])
                                Screen.close_screen()
                                break
                            player_press_use(True)
                            Screen.wait_screen()
                            process_trade(cost_name[0])
                            process_trade(cost_name[1])
                            sleep(0.05)
                            Screen.close_screen()
                            trading = False
                        else:
                            rotate_relative(90,0)
        except Exception as e:
            decho(f"Error: {e}")

        if not trading:
            if len(first_trade) == 0:
                first_trade = [int(float(str(x))) for x in pre_trade]
                decho("first trade logged")
            player_press_forward(True)
            sleep(0.4)
            trading = True

while True:
    sleep(0.1)

    if screen_name() == "Game Menu":
        execute(r"\killjob -1")

    ticks = world_info().day_ticks

    # Detect new Minecraft day / after sleeping.
    if ticks < last_ticks:
        trades_today = 0
        warned = False
        sleeping = False

    last_ticks = ticks

    # First restock window: do up to 2 trade rounds.
    if 2100 <= ticks <= 5999:
        warned = False
        sleeping = False

        while trades_today < 2 and 2100 <= world_info().day_ticks <= 5999:
            check_inv()
            trade()
            if trades_today >= 1:
                break
            trades_today += 1
            echo("Giving enough time for all\nvillagers to restock.")
            sleep(7.5)
        echo("§cTrades depleted for the day,\nwaiting for new day.")

    # Later daytime: if we somehow missed the first window, trade once.
    elif 6000 <= ticks <= 11999:
        warned = False
        sleeping = False

        if trades_today < 1:
            check_inv()
            trade()
            trades_today += 1
            echo("§cTrades depleted for the day,\nwaiting for new day.")

    # Nighttime: if no trade happened at all, trade once, then sleep.
    elif 12550 <= ticks <= 20000:
        warned = False

        if trades_today < 1:
            check_inv()
            trade()
            trades_today += 1

        if not sleeping:
            p.pathfind_to(*bed_spot)
            look_at_block(bed[0], bed[1], bed[2])
            player_press_use(True)
            sleep(0.2)
            player_press_use(False)
            sleeping = True

    # Early morning / invalid waiting period.
    else:
        if not warned:
            echo("§aWaiting for daytime")
            warned = True
