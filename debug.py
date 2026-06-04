from minescript import echo, player_press_use
#from minescript_plus import Client, Inventory, Screen
#from inventory_handle import inventory_count
from autofill_crafting_table import autofill_recipe
from time import sleep
from java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance() # type: ignore

#player_press_use(True)
#Screen.wait_screen()
sleep(1)
#Client.send_packet("ServerboundPlaceRecipePacket", mc.player.containerMenu.containerId, RecipeDisplayId(1039), True) # type: ignore

#autofill_recipe("minecraft:diamond")

def debug_all_game_mode_methods():
    cls = mc.gameMode.getClass()

    while cls is not None:
        echo("CLASS:", cls.getName())

        for method in cls.getDeclaredMethods():
            name = str(method.getName()).lower()
            text = str(method)

            if (
                "mouse" in name
                or "slot" in name
                or "inventory" in name
                or "container" in name
                or "click" in name
            ):
                echo("METHOD:", text)

                for i, param in enumerate(method.getParameterTypes()):
                    echo("  PARAM", i, ":", param.getName())

        cls = cls.getSuperclass()

debug_all_game_mode_methods()
