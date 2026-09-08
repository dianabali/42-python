from ex0 import CreatureFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory

def test_healing_creature(factory: CreatureFactory) -> None:
    """Create base, describe, attack, heal"""

    print("=== Testing Creature with Healing Capability ===")

    base = factory.create_base()
    print(f"Base: {base.describe()}")
    print(base.attack())
    print(base.heal())

    print()

    evolved = factory.create_evolved()
    print(f"Evolved: {evolved.describe()}")
    print(evolved.attack())
    print(evolved.heal())


def test_transform_creature(factory: CreatureFactory) -> None:
    """Create evovled, describe, attack, transform, attack, revert"""

    print("=== Testing Creature with Transform Capability ===")

    base = factory.create_base()
    print(f"Base: {base.describe()}")
    print(base.attack())
    print(base.transform())
    print(base.attack())
    print(base.revert())

    print()
    
    evolved = factory.create_evolved()
    print(f"Evolved: {evolved.describe()}")
    print(evolved.attack())
    print(evolved.transform())
    print(evolved.attack())
    print(evolved.revert())


def main() -> None:
    healing_factory = HealingCreatureFactory()
    transform_factory = TransformCreatureFactory()

    test_healing_creature(healing_factory)
    print()
    test_transform_creature(transform_factory)
    print()


if __name__ == "__main__":
    main()
