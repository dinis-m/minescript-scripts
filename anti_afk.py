import minescript as m
from time import sleep

block = m.player_get_targeted_block(2)

while True:
    m.player_press_use(True)
    if block is not None and block.type.split('[')[0] == "minecraft:note_block": 
        m.player_press_attack(True)
        m.player_press_attack(False)
    sleep(0.4)
    m.player_press_use(False)

    if m.screen_name() != None:
        print("killing job...")
        break

sleep(0.5)
m.execute("\\killjob -1")
