# 'elements' here is the *root* elements.py (fire, water), reachable because
# the interpreter's entry-point directory is on sys.path.
import elements as root_elements

# '.elements' is the local alchemy/elements.py (earth, air).
from .elements import create_air, create_earth


def healing_potion() -> str:
    return f"Healing potion brewed with '{create_earth()}' and '{create_air()}'"


def strength_potion() -> str:
    fire = root_elements.create_fire()
    water = root_elements.create_water()
    return f"Strength potion brewed with '{fire}' and '{water}'"
