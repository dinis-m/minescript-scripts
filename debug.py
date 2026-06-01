import minescript as m
from minescript_plus import Client
from time import sleep
from java import JavaClass

Minecraft = JavaClass("net.minecraft.class_310")
mc = Minecraft.getInstance()
m.player_press_use(True)
sleep(2)

RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(491), True)

m.player_press_use(False)

m.execute("\\killjob -1")