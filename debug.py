from minescript import echo, player_press_use
from minescript_plus import Client, Inventory, Screen
from inventory_handle import inventory_count
from time import sleep
from java import JavaClass

Minecraft = JavaClass("net.minecraft.class_310")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance() # type: ignore

player_press_use(True)
Screen.wait_screen()

Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(1039), True) # type: ignore
