from minescript import echo, player_press_use
from minescript_plus import Client, Inventory, Screen
from inventory_handle import inventory_count
from time import sleep
from java import JavaClass
from math import ceil

Minecraft = JavaClass("net.minecraft.class_310")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance() # type: ignore

def craft_emerald_blocks():
    craft_for = ceil((inventory_count("minecraft:emerald") // 9) / 64)
    player_press_use(True)
    Screen.wait_screen("", 1500)
    for _ in range(craft_for):
        sleep(0.1)
        Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(491), True) # type: ignore
        sleep(0.05)
        Inventory.shift_click_slot(0)
    Screen.close_screen()

#craft_emerald_blocks()