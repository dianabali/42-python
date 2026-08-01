import sys

print("=== Player Score Analytics ===")

scores: list[int] = []

i = 1
while i < len(sys.argv):
    try:
        score = int(sys.argv[i])
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
