from ex0 import CreatureFactory, FlameFactory, AquaFactory

def test_factory(factory: CreatureFactory) -> None:
    """Verify that a factory can create a Creature
    and each creature can be described and attack"""

    print("=== Testing Factory ===")

    base = factory.create_base()
    print(base.describe())
    print(base.attack())

    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory_a: CreatureFactory, factory_b: CreatureFactory) -> None:
    """Base A vs. Base B"""

    print("=== Testing Battle ===")

    creature_a = factory_a.create_base()
    creature_b = factory_b.create_base()

    print(f"{creature_a.describe()} vs. {creature_b.describe()} fight!")
    print(creature_a.attack())
    print(creature_b.attack())


def main() -> None:
    flame_factory = FlameFactory()
    aqua_factory = AquaFactory()

    test_factory(flame_factory)
    print()
    test_factory(aqua_factory)
    print()
    test_battle(flame_factory, aqua_factory)


if __name__ == "__main__":
    main()
