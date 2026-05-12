import system.lib.minescript as m
from minescript_plus import Inventory, Screen
from time import sleep

#Currently only works if first called container in script is opened first

def inventory_count(item_name: str):
    return sum(
        stack.count for stack in m.player_inventory()
        if stack.item == item_name
    )


def fill_to_target(item_name: str, target: int) -> bool:
    """Return True if the player has target amount of item_name"""
    if not m.screen_name():
        return False
    
    m.echo("Require container holding " + item_name)

    count = inventory_count(item_name)

    if count >= target:
        return True

    missing = target - count
    stacks_needed = (missing + 63) // 64

    for _ in range(stacks_needed):
        num = Inventory.find_item(item_name, container=True)
        if num is None or num >= 27:
            break
        Inventory.shift_click_slot(slot=num)
        sleep(0.1)

    Screen.close_screen()
    return inventory_count(item_name) >= target
