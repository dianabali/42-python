# Absolute import: fully qualified dotted path starting from the top-level
# package. Works regardless of where recipes.py itself lives in the tree.
from alchemy.elements import create_air

# Relative import: '..' walks back up from alchemy.transmutation to the
# alchemy package, then down into potions.py.
from ..potions import strength_potion

# The root elements.py (fire, water) is reachable the same way potions.py
# reaches it: the entry script's directory is on sys.path.
import elements as root_elements


def lead_to_gold() -> str:
    air = create_air()
    strength = strength_potion()
    fire = root_elements.create_fire()
    return (
        f"Recipe transmuting Lead to Gold: brew '{air}' and "
        f"'{strength}' mixed with '{fire}'"
    )
