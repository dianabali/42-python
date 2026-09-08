# NOTE: we import the *module* here, not a name out of it. This is what
# lets two mutually-dependent files load safely: by the time
# `light_spellbook.light_spell_allowed_ingredients` is actually looked up
# (inside validate_ingredients, at call time), both modules have finished
# loading. A top-level `from .light_spellbook import light_spell_allowed_ingredients`
# would instead try to resolve that name *while the module is still loading*,
# which is exactly what blows up the dark grimoire below.
from . import light_spellbook


def validate_ingredients(ingredients: str) -> str:
    allowed = light_spellbook.light_spell_allowed_ingredients()
    lowered = ingredients.lower()
    if any(item in lowered for item in allowed):
        return f"{ingredients}- VALID"
    return f"{ingredients}- INVALID"
