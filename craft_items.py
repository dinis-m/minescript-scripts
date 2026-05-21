import minescript as m
from minescript_plus import Inventory
from time import sleep
from java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")
CraftingInput = JavaClass("net.minecraft.world.item.crafting.CraftingInput")
CraftingMenu = JavaClass("net.minecraft.world.inventory.CraftingMenu")
RecipeManager = JavaClass("net.minecraft.world.item.crafting.RecipeManager")
mc = Minecraft.getInstance() # type: ignore

def craft_item(item_name: str):
    """
        Craft the specified item if possible.

        Precondition: The item name must be in the crafting recipe book.
            Player must be in the crafting screen.
    """
    m.echo(f"Attempting to craft {item_name}...")


sleep(1)

if str(mc.screen).split("@")[0] == "net.minecraft.class_479": # type: ignore
    pass
print("start")
item_name = "minecraft:pumpkin"
item_slots = [
    item.slot for item in m.container_get_items() 
    if item.item == item_name and item.slot < 27
]
item_slots.reverse()
for i in range(0, 9):
    if len(item_slots) <= 27:
        print(item_slots[i])
        Inventory.shift_click_slot(item_slots[i])
        sleep(0.1)
print("end")
