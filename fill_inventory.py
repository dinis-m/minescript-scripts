import minescript as m
import rotation_1 as r
import pathfinding as p
import inventory_handle as i
from time import sleep

sleep(0.5)

shulker = [-2183, 50, 1064]
pumpkin_chest = [-2182, 49, 1065]
melon_chest = [-2182, 49, 1066]

def fill_inventory(target: int):
    p.pathfind_to(-2181, 50, 1064, True)
    # wait until player is in position
    r.look_at_block(shulker[0], shulker[1], shulker[2])
    i.fill_to_target("minecraft:emerald", target)
    # open container and fill inventory
    r.look_at_block(pumpkin_chest[0], pumpkin_chest[1], pumpkin_chest[2])
    # open container and fill inventory
    r.look_at_block(melon_chest[0], melon_chest[1], melon_chest[2])
    # open container and fill inventory
