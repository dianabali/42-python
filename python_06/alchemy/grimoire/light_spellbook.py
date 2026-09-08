# Same technique as light_validator.py: import the module, resolve the
# attribute lazily inside the function body.
from . import light_validator


def light_spell_allowed_ingredients() -> list:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    result = light_validator.validate_ingredients(ingredients)
    if result.endswith("VALID") and not result.endswith("INVALID"):
        return f"Spell recorded: {spell_name} ({result})"
    return f"Spell rejected: {spell_name} ({result})"
