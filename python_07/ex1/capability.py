from abc import ABC, abstractmethod
from typing import Any, Optional

# Optional -> smth or none (str or none)

class HealCapability(ABC):
    """Abstract class for Healing"""

    @abstractmethod
    def heal(self, target: Optional[Any] = None) -> str:
        """Healing description"""
        pass


class TransformCapability(ABC):
    """Abstract class for Transform"""

    def __init__(self) -> None:
        self.transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        """Transformation desc"""
        pass

    @abstractmethod
    def revert(self) -> str:
        """Reversion desc"""
        pass
