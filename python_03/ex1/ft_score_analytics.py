"""
List items are indexed, ordered, changeable, and allow duplicates.
Synatx: list = []
Example:
    my_str_list = ["hello", "world", "cool stuff", "this is a list"]
    my_int_list = [1, 2, 3, 4, 5]
    my_whatever_list = ["hello", True, 1, "world", 42]

List constructor: list() - used to make a list.
Example:
    my_list = list(("hello", "world", "cool"))
"""

import sys

print("=== Player Score Analytics ===")

scores: list[int] = []

i: int = 1
while i < len(sys.argv):
    try:
        score: int = int(sys.argv[i])
        scores = scores + [score]
    except ValueError:
        print("Invalid parameter:", "'" + sys.argv[i] + "'")
    i += 1

if len(scores) == 0:
    print(
        "No scores provided. Usage: python3 ft_score_analytics.py "
        "<score1> <score2> ..."
    )
else:
    print("Scores processed:", scores)
    print("Total players:", len(scores))
    print("Total score:", sum(scores))
    print("Average score:", sum(scores) / len(scores))
    print("High score:", max(scores))
    print("Low score:", min(scores))
    print("Score range:", max(scores) - min(scores))
