import math


def get_player_pos() -> tuple[float, float, float]:
    while True:
        coordinates: str = input(
            "Enter new coordinates as floats in format 'x,y,z': "
        )

        try:
            values: list[str] = coordinates.split(",")

            if len(values) != 3:
                print("Invalid syntax")
                continue

            x: float = float(values[0].strip())
            y: float = float(values[1].strip())
            z: float = float(values[2].strip())

            return (x, y, z)
        except ValueError:
            print("Invalid syntax")


def calculate_distance(
        point1: tuple[float, float, float],
        point2: tuple[float, float, float]
    ) -> float:
        return math.sqrt(
            (point2[0] - point1[0]) ** 2 +
            (point2[1] - point1[1]) ** 2 +
            (point2[2] - point1[2]) ** 2
        )


print("=== Game Coordinate System ===")

print()

print("Get a first set of coordinates")
first_pos: tuple[float, float, float] = get_player_pos()

print(f"Got a first tuple: {first_pos}")
print(
    "It includes: X=" + str(first_pos[0]) +
    ", Y=", str(first_pos[1]) +
    ", Z=", str(first_pos[2])
)

center: tuple[float, float, float] = (0.0, 0.0, 0.0)
print(
    "Distance to center:",
    round(calculate_distance(first_pos, center), 4)
)

print()

print("Get a second set of coordinates")
second_pos: tuple[float, float, float] = get_player_pos()
print(
    "Distance between the 2 sets of coordinates:",
    round(calculate_distance(first_pos, second_pos), 4)
)
