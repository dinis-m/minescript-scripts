import minescript as m
from minescript_plus import Client, Inventory, Screen
from inventory_handle import inventory_count
from time import sleep
from java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
mc = Minecraft.getInstance() # type: ignore

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

# m.echo(m.world_info().day_ticks)
sleep(1)
m.echo(m.screen_name() == "Game Menu")