# DANGER: naive top-level `from X import name`. Unlike light_validator.py,
# this tries to grab a specific attribute off dark_spellbook *immediately*,
# while dark_spellbook may still be mid-import. That's the circular-import
# trap this file is deliberately left in.
from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    allowed = dark_spell_allowed_ingredients()
    lowered = ingredients.lower()
    if any(item in lowered for item in allowed):
        return f"{ingredients}- VALID"
    return f"{ingredients}- INVALID"
