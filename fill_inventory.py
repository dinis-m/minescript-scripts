import minescript as m
import rotation_1 as r
import pathfinding as p
from time import sleep

sleep(0.5)

shulker = [-2183, 50, 1064]
pumpkin_chest = [-2182, 49, 1065]
melon_chest = [-2182, 49, 1066]

p.pathfind_to(-2181, 50, 1064, True)
sleep(3)
r.look_at_block(shulker[0], shulker[1], shulker[2])
sleep(1)
r.look_at_block(pumpkin_chest[0], pumpkin_chest[1], pumpkin_chest[2])
sleep(1)
r.look_at_block(melon_chest[0], melon_chest[1], melon_chest[2])
