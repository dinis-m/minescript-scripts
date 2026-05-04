import system.lib.minescript as m
from minescript_plus import Screen
from rotation import rotate_relative
from trade_process import process_trade
from inventory_handle import fill_to_target
from time import sleep

result_name = ["minecraft:golden_carrot"]
cost_name = ["minecraft:emerald"]
villager_type = "Farmer"
teleport_to = "/home farmers"


TARGET = 43*12
complete = False

m.echo(f"Require {TARGET} total \n{cost_name} \n({(TARGET + 63 ) // 64} stacks(rounded) required)")
#first called container MUST be opened first
while not complete:
    while not Screen.wait_screen():
        sleep(0.05)
    #break loop if player has sufficient items in inventory for trades
    complete = fill_to_target(cost_name[0], TARGET)


last_trade = [x.position for x in m.entities(name=villager_type, max_distance=1.4)]
trading = True

m.echo("DONT MOVE")
m.player_press_forward(False)
sleep(0.5)
if teleport_to != "":
    m.execute(teleport_to)
sleep(3) # wait to finish teleporting
m.player_press_forward(True)

while True:
    m.flush()

    if m.screen_name() == "Crafting":
        m.execute("\\killjob -1")
    
    if m.player_get_targeted_entity(max_distance=2) is not None:
        if m.player_get_targeted_entity(max_distance=2).name == villager_type: # type: ignore
            if m.player_get_targeted_entity(max_distance=2) is not None:
                if m.player_get_targeted_entity().position != last_trade: # type: ignore
                    last_trade = m.player_get_targeted_entity().position # type: ignore
                    m.player_press_forward(False)
                    m.player_press_use(True)
                    sleep(0.3)
                    process_trade(result_name[0])
                    Screen.close_screen()
                    sleep(0.05)
                    trading = False
                else:
                    rotate_relative(90,0)

    if not trading:
        m.player_press_forward(True)
        sleep(0.4)
        trading = True
