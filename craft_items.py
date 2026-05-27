import minescript as m
from minescript_plus import Server
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
# temporary test area
print("end")
