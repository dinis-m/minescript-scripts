from minescript import container_get_items, echo, player_inventory, screen_name
from minescript_plus import Inventory, Screen
from time import sleep
from java import JavaClass

VERSION = "1.1.0"

Minecraft = JavaClass("net.minecraft.client.Minecraft")
ContainerInput = JavaClass("net.minecraft.world.inventory.ContainerInput")
mc = Minecraft.getInstance() # type:ignore

def inventory_count(item_name: str) -> int:
    """
    Return the total count of item_name in the player's inventory.

    Pre-condition: item_name must be valid ItemStack.item.
    """
    return sum(
        stack.count for stack in player_inventory()
        if stack.item == item_name
    )

def fill_to_target(item_name: str, target: int) -> bool:
    """
    Return True if the player has target amount of item_name.
    
    Pre-condition: item_name must be valid ItemStack.item.
    """
    if not screen_name():
        return False

    count = inventory_count(item_name)

    if count >= target:
        return True
    else:
        echo("Require container holding " + item_name)

    missing = target - count
    stacks_needed = (missing + 63) // 64

    # only store slots of items within the container 0-26
    item_slots = [
        item.slot for item in container_get_items()
        if item.item == item_name and item.slot < 27
    ]

    for slot in range(0, stacks_needed):
        try:
            if count >= target:
                return True
            if stacks_needed == 1:
                Inventory.shift_click_slot(item_slots[slot+1])
                break
            Inventory.shift_click_slot(item_slots[slot])
            sleep(0.1)
        except IndexError:
            echo(f"{item_name} not found.")
            break

    Screen.close_screen()
    return inventory_count(item_name) >= target

def get_slots(item_name: str) -> list[int]:
    """
    Return a list of slots in the player's inventory that contain item_name.

    Pre-condition: item_name must be valid ItemStack.item.
    """
    item_slots = [
        item.slot for item in container_get_items()
        if item.item == item_name
    ]
    return item_slots
