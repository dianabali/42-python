class Plant:
    def __init__(self, name, height, age, growth_rate):
        self.name = name
        self.height = height
        self.age_days = age
        self.growth_rate = growth_rate

    def show(self):
        print(f"{self.name}: {self.height:.1f}cm, {self.age_days} days old")

    def grow(self):
        self.height += self.growth_rate

    def age(self):
        self.age_days += 1

def main():
    plant = Plant("Rose", 25.0, 30, 0.8)
    starting_height = plant.height

    print("=== Garden Plant Growth ===")
    plant.show()

    for day in range(1, 8):
        plant.grow()
        plant.age()

        print(f"=== Day {day} ===")
        plant.show()

    total_growth = plant.height - starting_height

    print(f"Growth this week: +{total_growth:.1f}cm")

if __name__ == "__main__":
    main()
