import minescript as m
from minescript_plus import Client, Inventory, Screen
from inventory_handle import inventory_count
from time import sleep
from java import JavaClass
from math import ceil


Minecraft = JavaClass("net.minecraft.class_310")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance()

def craft_emerald_block():
    m.player_press_use(True)
    Screen.wait_screen()
    m.player_press_use(False)
    Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(491), True)
    Inventory.shift_click_slot(0)


m.echo(ceil((inventory_count("minecraft:emerald") // 9) / 64))
craft_for = ceil((inventory_count("minecraft:emerald") // 9) / 64)

m.player_press_use(True)
Screen.wait_screen()
m.player_press_use(False)
for i in range(craft_for):
    sleep(0.01)
    Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(491), True)
    Inventory.shift_click_slot(0)