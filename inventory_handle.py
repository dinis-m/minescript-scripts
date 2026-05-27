import minescript as m
from minescript_plus import Inventory, Screen
from time import sleep

VERSION = "1.0.0"

#Currently only works if first called container in script is opened first

def inventory_count(item_name: str) -> int:
    return sum(
        stack.count for stack in m.player_inventory()
        if stack.item == item_name
    )


def fill_to_target(item_name: str, target: int) -> bool:
    """
    Return True if the player has target amount of item_name.
    
    Pre-condition: item_name must be valid ItemStack.item.
    """
    if not m.screen_name():
        return False

    count = inventory_count(item_name)

    if count >= target:
        return True
    else:
        m.echo("Require container holding " + item_name)

    missing = target - count
    stacks_needed = (missing + 63) // 64

    # only store slots of items within the container 0-26
    item_slots = [
        item.slot for item in m.container_get_items()
        if item.item == item_name and item.slot < 27
    ]

    for slot in range(0, stacks_needed):
        try:
            if stacks_needed == 1:
                Inventory.shift_click_slot(item_slots[slot+1])
                break
            Inventory.shift_click_slot(item_slots[slot])
            sleep(0.1)
        except IndexError:
            m.echo(f"{item_name} not found.")
            break

    Screen.close_screen()
    return inventory_count(item_name) >= target
