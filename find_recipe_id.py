import re
import minescript as m
from time import sleep
from java import JavaClass

sleep(2)

def J(*names):
    """Try multiple class names because mappings are inconsistent in Minescript/Fabric."""
    last_error = None

    for name in names:
        try:
            return JavaClass(name)
        except Exception as e:
            last_error = e

    raise last_error


def get_field(obj, *names):
    """Get a private Java field by trying several mapped names."""
    cls = obj.getClass()

    for name in names:
        try:
            field = cls.getDeclaredField(name)
            field.setAccessible(True)
            return field
        except Exception:
            pass

    raise Exception("Could not find field: " + str(names))


Minecraft = J(
    "net.minecraft.client.Minecraft",
    "net.minecraft.class_310"
)

ServerboundPlaceRecipePacket = J(
    "net.minecraft.network.protocol.game.ServerboundPlaceRecipePacket",
    "net.minecraft.class_2840"
)

mc = Minecraft.getInstance()
player = mc.player
connection = mc.method_1562()  # getConnection()
menu = player.containerMenu
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")

container_id = menu.containerId

m.echo("Container ID:", container_id)

# Newer 1.21.x route:
# player.getRecipeBook()
recipe_book = player.method_3130()

# ClientRecipeBook has a private map:
# Map<RecipeDisplayId, RecipeDisplayEntry>
known_field = get_field(recipe_book, "field_54810", "recipes", "b")
known_recipes = known_field.get(recipe_book)

import re

text = str(known_recipes)

pairs = [
    (item, int(index))
    for index, item in re.findall(
        r"class_10298\[index=(\d+)\]=.*?result=.*?stack=\d+\s+(minecraft:[a-z0-9_]+)",
        text,
        flags=re.DOTALL
    )
]

s = str(pairs)

m.echo(s)

with open("known_recipes.txt", "w") as f:
    f.write(s)