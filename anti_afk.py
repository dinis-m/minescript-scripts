import minescript as m
from time import sleep

while True:
    m.player_press_use(True)
    sleep(0.4)
    m.player_press_use(False)

    if m.screen_name() != None:
        print("killing job...")
        break

m.execute("\\killjob -1")
