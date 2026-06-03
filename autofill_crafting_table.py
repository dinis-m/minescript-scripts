import minescript as m
from recipe_helper import get_recipes_id
from java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")
ServerboundPlaceRecipePacket = JavaClass("net.minecraft.network.protocol.game.ServerboundPlaceRecipePacket")
mc = Minecraft.getInstance() # type: ignore

def autofill_recipe(item_name: str):
    """
    item_name must be a valid ItemStack.item
    """
    try:
        mc.getConnection().send(ServerboundPlaceRecipePacket(mc.player.containerMenu.containerId, RecipeDisplayId(get_recipes_id(item_name)), True)) # type: ignore
    except Exception as e:
        m.echo(f"Error: {e}")
