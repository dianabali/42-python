from abc import ABC, abstractmethod
from ex0.creature import Creature
from ex1 import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    """When act() is called"""

class BattleStrategy(ABC):
    """Abstract class for how Creature behaves in fights"""

    name: str = "generic"

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Is Creature suitable for this strategy"""
        pass

    @abstractmethod
    def act(self, creature: Creature) -> None:
        """Make Creature fight"""
        pass

    def _ensure_valid(self, creature: Creature) -> None:
        """Helper for act()"""
        if not self.is_valid(creature):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name} for this {self.name} strategy"
            )


class NormalStrategy(BattleStrategy):
    """For any Creature. Simply attacks"""

    name = "normal"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, Creature)

    def act(self, creature: Creature) -> None:
        self._ensure_valid(creature)
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    """For Creature with transform abilities"""

    name = "aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        self._ensure_valid(creature)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


class DefensiveStrategy(BattleStrategy):
    """For Creature with healing abilities"""

    name = "defensive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        self._ensure_valid(creature)
        print(creature.attack())
        print(creature.heal())
