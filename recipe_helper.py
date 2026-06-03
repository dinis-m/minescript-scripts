import os
import re
import minescript as m
from java import JavaClass

Minecraft = JavaClass("net.minecraft.client.Minecraft")
mc = Minecraft.getInstance()
player = mc.player
RecipeDisplayId = JavaClass("net.minecraft.world.item.crafting.display.RecipeDisplayId")

def get_field(obj, field_name):
    cls = obj.getClass()

    while cls is not None:
        try:
            field = cls.getDeclaredField(field_name)
            field.setAccessible(True)
            return field.get(obj)
        except Exception:
            cls = cls.getSuperclass()

    raise Exception(f"Could not find field: {field_name}")

recipe_book = player.getRecipeBook()
known_recipes = get_field(recipe_book, "known")

text = str(known_recipes)

recipe_pairs = [
    (str(item), int(index))
    for index, item in re.findall(
        r"RecipeDisplayId\[index=(\d+)\]=RecipeDisplayEntry\[.*?"
        r"result=ItemStackSlotDisplay\[stack=ItemStackTemplate\[.*?"
        r"=(minecraft:[a-z0-9_]+)",
        text,
        flags=re.DOTALL
    )
]

def write_recipes_to_file(path: str = r"minescript\known_recipes.txt") -> None:
    """
    Write recipe data to a text file for easier inspection.

    Args:
        path: The file path to write the recipe data to. Defaults to
            ``minescript\\known_recipes.txt``.
        content: The recipe data to write to the file.

    Returns:
        None.

    Notes:
        This function overwrites the target file if it already exists.
        The parent folder must already exist, otherwise ``open()`` will raise
        a file path error.
    """
    m.echo("Writing to:", path)
    m.echo("Text length:", len(str(recipe_pairs)))

    with open(path, "w", encoding="utf-8") as file:
        file.write(str(recipe_pairs).replace(",", ",\n"))

    m.echo("Done")
    m.echo("File exists:", os.path.exists(path))

def get_recipes_id(item_name: str) -> int | None:
    """
    Return the recipe display index for a given Minecraft item.

    Args:
        item_name: The full Minecraft item ID to search for, such as
            ``"minecraft:emerald_block"``.

    Returns:
        The recipe display index as an integer if the item is found.
        Otherwise, returns an error message string explaining that the recipe
        is not known.

    Notes:
        ``recipe_pairs`` is expected to contain pairs in the form
        ``(item_name, index)``, for example:
        ``("minecraft:stick", 1444)``.
    """
    for item, index in recipe_pairs:
        if item == item_name:
            return index

    m.echo(f"Error: item recipe not known: {item_name}")
    return None
