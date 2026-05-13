import minescript as m
from minescript_plus import Inventory
from time import sleep
from java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")
RecipeManager = JavaClass("net.minecraft.world.item.crafting.RecipeManager")
RecipeMap = JavaClass("net.minecraft.world.item.crafting.RecipeMap")
mc = Minecraft.getInstance()

def craft_item(item_name: str):
    """
        Craft the specified item if possible.

        Precondition: The item name must be in the crafting recipe book.
            Player must be in the crafting screen.
    """
    m.echo(f"Attempting to craft {item_name}...")


print(RecipeMap.values())