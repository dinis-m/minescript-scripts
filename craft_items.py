from minescript import echo, player_press_use
from minescript_plus import Client, Inventory, Screen
from inventory_handle import inventory_count
from time import sleep
from java import JavaClass
from math import ceil

Minecraft = JavaClass("net.minecraft.class_310")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance() # type: ignore

debug = False

if debug:
    echo("§aDEBUGGING ENABLED FOR: craft_items.py")

def decho(*args):
    if debug:
        echo(*args)

def craft_emerald_blocks():
    craft_for = ceil((inventory_count("minecraft:emerald") // 9) / 64)
    decho("crafting emerald blocks...")
    player_press_use(True)
    Screen.wait_screen("", 1500)
    decho("crafting screen opened")
    decho(f"craft_for: {craft_for}")
    for _ in range(craft_for):
        sleep(0.1)
        decho("sending recipe packet...")
        Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(491), True) # type: ignore
        decho("recipe packet sent")
        sleep(0.05)
        Inventory.shift_click_slot(0)
        decho("Emerald blocks stored")
    Screen.close_screen()

#craft_emerald_blocks()