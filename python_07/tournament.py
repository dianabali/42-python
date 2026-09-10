from itertools import combinations
from typing import List, Tuple
from ex0 import CreatureFactory, FlameFactory, AquaFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    BattleStrategy,
    NormalStrategy,
    AggressiveStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
)

Opponent = Tuple[CreatureFactory, BattleStrategy]

def battle(opponents: List[Opponent]) -> None:
    """Each opponent will fight once with all opponents"""

    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")

    participants = [(factory.create_base(), strategy) for factory, strategy in opponents]

    for (creature_a, strategy_a), (creature_b, strategy_b) in combinations(participants, 2):
        print("* Battle *")
        print(f"{creature_a.describe()} vs. {creature_b.describe()} now fight!")
        try:
            strategy_a.act(creature_a)
            strategy_b.act(creature_b)
            print()
        except InvalidStrategyError as error:
            print(f"Battle error, aborting tournament: {error}")
            return


def main() -> None:
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print("[ (Flameling+Normal), (Healing+Defensive) ]")
    battle([
        (FlameFactory(), normal),
        (HealingCreatureFactory(), defensive),
    ])

    print("Tournament 1 (error)")
    print("[ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([
        (FlameFactory(), aggressive),
        (HealingCreatureFactory(), defensive),
    ])

    print()

    print("Tournament 2 (multiple)")
    print("[ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]")
    battle([
        (AquaFactory(), normal),
        (HealingCreatureFactory(), defensive),
        (TransformCreatureFactory(), aggressive),
    ])

    print()


if __name__ == "__main__":
    main()
