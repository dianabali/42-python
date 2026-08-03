"""
Sets are unordered, immutable (but you can add/remove), unindexed, and don't allow duplicates.
Syntax: my_set = {}
Example:
    my_set = {"hello", "world", "this is a set", "hello") -> 2nd hello is not printed
    my_set = {1, 2, 3, 4, 5}
    my_set = {"hello", 42, True, 1, "yoo"}

NOTE: True = 1 and False = 0. They are treated as duplicates.

The set constructor: set()
Example:
    my_set = set(("hello", "world", 42))
"""

import random

ACHIEVEMENTS = [
    "First Steps",
    "Speed Runner",
    "Master Explorer",
    "Treasure Hunter",
    "Crafting Genius",
    "Boss Slayer",
    "World Savior",
    "Collector Supreme",
    "Untouchable",
    "Unstoppable",
    "Strategist",
    "Sharp Mind",
    "Hidden Path Finder"
]

def gen_player_achievements():
    count = random.randint(3, len(ACHIEVEMENTS))
    return set(random.sample(ACHIEVEMENTS, count))

print("=== Achievement Tracker System ===")

print()

players = {
    "Alice": gen_player_achievements(),
    "Bob": gen_player_achievements(),
    "Charlie": gen_player_achievements(),
    "Dylan": gen_player_achievements()
}

# Each player's achievements
for name in players:
    print(f"Player {name}: {players[name]}")

print()

# All distinct achievements
all_achievements = set()
for achievements in players.values():
    all_achievements = all_achievements.union(achievements)

print("All distinct achievements:", all_achievements)

print()

# Common achievements
common_achievements = None
for achievements in players.values():
    if common_achievements is None:
        common_achievements = achievements
    else:
        common_achievements = common_achievements.intersection(achievements)

print("Common achievements:", common_achievements)

print()

# Unique achievements
for name in players:
    others = set()
    for other_name in players:
        if other_name != name:
            others = others.union(players[other_name])

    unique = players[name].difference(others)
    print(f"Only {name} has:", unique)

print()

# Missing achievements
for name in players:
    missing = set(ACHIEVEMENTS).difference(players[name])
    print(f"{name} is missing:", missing)
