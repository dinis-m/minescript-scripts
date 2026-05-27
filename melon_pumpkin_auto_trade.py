"""
    Autonomous melon and pumpkin trading script for 1.20+ versions of Minecraft. 
    Trades with farmers to acquire emeralds, then crafts them into blocks. 
    Must set a teleportation point to the villagers.
"""
import minescript as m
from minescript_plus import Screen
from rotation_1 import rotate_relative, look_at_block
from trade_process import process_trade
from inventory_handle import fill_to_target, inventory_count
import pathfinding as p
from time import sleep
from java import JavaClass

VERSION = "1.2.0"
MAX_TRADES = 12
VILLAGER_COUNT = 42
print(f"Melon and Pumpkin Auto Trade Script v{VERSION}")
# TODO: complete autonomous functionality of script; auto crafting emerald blocks, sleeping when night, pathfinding to item chests.

Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance() # type: ignore

cost_name = ["minecraft:pumpkin", "minecraft:melon"]
villager_type = "Farmer"

teleport_to = "/home farmers"

target = VILLAGER_COUNT * MAX_TRADES
complete = False

pumpkin_chest = [-2182, 49, 1065]
melon_chest = [-2182, 49, 1066]

m.execute(teleport_to)
sleep(3) # wait to finish teleporting

m.echo(f"Require {target} total \n{cost_name} \n({(target + 63 ) // 64} stacks(rounded) required)")

p.pathfind_to(-2181, 50, 1064, True)
# wait until player is in position
while True:
    sleep(0.05)
    if [int(float(str(x))) for x in m.player_position()] == [-2181, 50, 1064]:
        break

# get items from chests until target is reached
while not complete:
    if inventory_count(cost_name[0]) >= target and inventory_count(cost_name[1]) >= target:
        break
    sleep(0.15)
    # open container and fill inventory with pumpkins
    look_at_block(pumpkin_chest[0], pumpkin_chest[1], pumpkin_chest[2])
    m.player_press_use(True)
    Screen.wait_screen()
    pumpkins = fill_to_target(cost_name[0], target)
    sleep(0.15)
    # open container and fill inventory with melons
    look_at_block(melon_chest[0], melon_chest[1], melon_chest[2])
    m.player_press_use(True)
    Screen.wait_screen()
    melons = fill_to_target(cost_name[1], target)
    complete = pumpkins and melons

#forces camera to turn if facing the same villager.
pre_trade = [x.position for x in m.entities(name=villager_type, max_distance=1.4)]
first_trade: list[int] = []
trading = True

Screen.close_screen()
m.echo("DONT MOVE")
m.player_press_forward(False)
sleep(0.5)
if teleport_to != "":
    m.execute(teleport_to)
sleep(3) # wait to finish teleporting
m.player_press_forward(True)

while True:
    m.flush()
    
    # crafting table class: net.minecraft.class_479
    if str(mc.screen).split("@")[0] == "net.minecraft.class_479": # type: ignore
        #craft emerald blocks
        pass

    if m.screen_name() == "Crafting":
        break

    if m.player_get_targeted_entity(max_distance=2) is not None:
        if m.player_get_targeted_entity(max_distance=2).name == villager_type: # type: ignore
            if m.player_get_targeted_entity(max_distance=2) is not None:
                if m.player_get_targeted_entity().position != pre_trade: # type: ignore
                    pre_trade = m.player_get_targeted_entity().position # type: ignore
                    m.player_press_forward(False)
                    if first_trade == [int(float(str(x))) for x in pre_trade]:
                        break
                    m.player_press_use(True)
                    Screen.wait_screen()
                    process_trade(cost_name[0])
                    process_trade(cost_name[1])
                    sleep(0.05)
                    Screen.close_screen()
                    trading = False
                else:
                    rotate_relative(90,0)

    if not trading:
        if len(first_trade) == 0:
            first_trade = [int(float(str(x))) for x in pre_trade]
            print("first trade logged")
        m.player_press_forward(True)
        sleep(0.4)
        trading = True

m.execute("\\killjob -1")
