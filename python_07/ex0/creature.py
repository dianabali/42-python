from abc import ABC, abstractmethod


class Creature(ABC):
    """Abstract class for Creature"""

    def __init__(self, name: str, typee: str) -> None:
        self.name: str = name
        self.typee: str = typee

    @abstractmethod
    def attack(self) -> str:
        """Creature attack"""
        pass

    def describe(self) -> str:
        """Creature description"""
        return f"{self.name} is a {self.typee} type Creature"


class Flameling(Creature):
    """Base fire creature"""

    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    """Evolved fire creature"""
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    """Base water creature"""

    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    """Evolved water creature"""

    def __init__(self) -> None:
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        return f"{self.name} uses Hydro Pump!"