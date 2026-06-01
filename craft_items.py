import minescript as m
from minescript_plus import Client, Inventory, Screen
from inventory_handle import inventory_count
from time import sleep
from java import JavaClass
from math import ceil


Minecraft = JavaClass("net.minecraft.class_310")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance()

craft_for = ceil((inventory_count("minecraft:emerald") // 9) / 64)

def craft_emerald_blocks():
    m.echo("crafting emerald blocks...")
    m.player_press_use(True)
    Screen.wait_screen("", 2000)
    for _ in range(craft_for):
        sleep(0.3)
        Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(491), True)
        sleep(0.1)
        Inventory.shift_click_slot(0)
    Screen.close_screen()
