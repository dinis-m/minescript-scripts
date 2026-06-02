"""
    Autonomous melon and pumpkin trading script for 1.21+ versions of Minecraft. 
    Trades with farmers to acquire emeralds, then crafts them into blocks. 
    Must set a teleportation point to the villagers.
"""
from minescript import echo, entities, execute, flush, player_position, player_press_forward, player_press_use, player_get_targeted_entity, screen_name
from minescript_plus import Screen, Inventory
from rotation_1 import rotate_relative, look_at_block
from trade_process import process_trade
from inventory_handle import fill_to_target, inventory_count, get_slots
from craft_items import craft_emerald_blocks
import pathfinding as p
from time import sleep

VERSION = "1.3.2"
MAX_TRADES = 12
VILLAGER_COUNT = 63
echo(f"Melon and Pumpkin Auto Trade Script v{VERSION}")
# TODO: complete autonomous functionality of script; auto crafting emerald blocks, sleeping when night.

target = VILLAGER_COUNT * MAX_TRADES
cost_name = ["minecraft:pumpkin", "minecraft:melon"]
villager_type = "Farmer"
teleport_to = "/home farmers"
pumpkin_chest = [-2182, 49, 1065]
melon_chest = [-2182, 49, 1066]
pre_trade = [x.position for x in entities(name=villager_type, max_distance=1.4)]
first_trade: list[int] = []

complete = False

# Set to True to debug
debug = False

if debug:
    echo("§aDEBUGGING ENABLED FOR: melon_pumpkin_auto_trade.py")

def decho(*args):
    if debug:
        echo(*args)

if inventory_count(cost_name[0]) >= target and inventory_count(cost_name[1]) >= target:
    complete = True
else:
    execute(teleport_to)
    sleep(3) # wait to finish teleporting
    p.pathfind_to(-2181, 50, 1064, True)
    while True:
        sleep(0.05)
        if [int(x) for x in player_position()] == [-2181, 50, 1064] or [int(x) for x in player_position()] == [-2180, 50, 1064]:
            break

echo(f"Require {target} total \n{cost_name} \nRequire {(target + 63 ) // 64} stacks(rounded) each")
# get items from chests until target is reached
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

Screen.close_screen()
echo("DONT MOVE")
sleep(0.5)
player_press_forward(False)
sleep(0.5)
if teleport_to != "":
    execute(teleport_to)
sleep(3) # wait to finish teleporting
player_press_forward(True)

trading = True

while True:
    flush()

    if screen_name() == "Crafting":
        break

    # wrap this in try except
    try:
        if player_get_targeted_entity(max_distance=2) is not None:
            if player_get_targeted_entity(max_distance=2).name == villager_type: # type: ignore
                if player_get_targeted_entity(max_distance=2) is not None:
                    if player_get_targeted_entity().position != pre_trade: # type: ignore
                        pre_trade = player_get_targeted_entity().position # type: ignore
                        player_press_forward(False)
                        if first_trade == [int(float(str(x))) for x in pre_trade]:
                            p.pathfind_to(-2174, 50, 1064, True)
                            # wait until player is in position
                            while True: # separate function?
                                sleep(0.05)
                                if [int(float(str(x))) for x in player_position()] == [-2173, 50, 1064]:
                                    break
                            look_at_block(-2173, 50, 1064)
                            decho("attempting to craft")
                            craft_emerald_blocks()
                            look_at_block(-2173, 50, 1066)
                            player_press_use(True)
                            Screen.wait_screen()
                            slots = get_slots("minecraft:emerald_block")
                            decho(f"slots: {slots}")
                            for slot in range(0, len(slots)-1):
                                sleep(0.1)
                                Inventory.shift_click_slot(slots[slot])
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

execute("\\killjob -1")
