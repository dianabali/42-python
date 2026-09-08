# Deliberately partial: create_earth() from alchemy/elements.py is NOT
# re-exported here, so `alchemy.create_earth()` raises AttributeError even
# though `alchemy.elements.create_earth()` works fine.
from .elements import create_air  # noqa: F401

from .potions import strength_potion  # noqa: F401
from .potions import healing_potion as heal  # noqa: F401

# Pulls in the transmutation and grimoire subpackages so that, once
# `import alchemy` has run, `alchemy.transmutation` / `alchemy.grimoire`
# are already available as attributes.
from . import transmutation  # noqa: F401
from . import grimoire  # noqa: F401

__all__ = [
    "create_air",
    "strength_potion",
    "heal",
    "transmutation",
    "grimoire",
]
