"""
List comprehensions - a short way to create a new list from an existing iterable.
Syntax: my_list = [expression for item in iterable]
Example w/o:
    numbers = [1, 2, 3, 4, 5]
    squares = []
    for number in numbers:
        squares.append(number * number)
    print(squares)
Example w:
    numbers = [1, 2, 3, 4, 5]
    squares = [number * number for number in numbers]
    print(squares)


Dictionary comprehensions - dictionary version of list comprehensions.
Syntax: new_dict = {key_expression: value_expression for item in iterable}
Example w/o:
    players = ["Alice", "Bob", "Charlie"]
    scores = {}
    for player in players:
        scores[player] = 0
    print(scores)
Example w:
    scores = {player: 0 for player in players}
"""

import random

print("=== Game Data Alchemist ===")

print()

players: list[str] = [
    "Alice",
    "bob",
    "Charlie",
    "dylan",
    "Emma",
    "Gregory",
    "john",
    "kevin",
    "Liam"
]

print("Initial list of players:", players)

capitalized_players: list[str] = [name.capitalize() for name in players]

print("New list with all names capitalized:", capitalized_players)

only_capitalized_players: list[str] = [name for name in players if name[0].isupper()]

print("New list of capitalized names only:", only_capitalized_players)

scores: dict[str, int] = {name: random.randint(1, 1000) for name in capitalized_players}

print()

print("Score dict:", scores)

average: float = round(sum(scores.values()) / len(scores), 2)

print("Score average is", average)

high_scores: dict[str, int] = {name: score for name, score in scores.items() if score > average}

print("High scores:", high_scores)
