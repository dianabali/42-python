from ex0 import CreatureFactory
from ex0.creature import Creature
from .creature import Sproutling, Bloomelle, Shiftling, Morphagon

class HealingCreatureFactory(CreatureFactory):
    """Factory for Healing"""

    def create_base(self) -> Creature:
        return Sproutling()

    def create_evolved(self) -> Creature:
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    """Factory for Transform"""

    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
