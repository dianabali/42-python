class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age_days = age

    def show(self):
        print(f"{self.name}: {self.height}cm, {self.age} days old")

    def grow(self):
        self.height += 2

    def age(self):
        self.age_days += 1

def main():
    plant = Plant("Rose", 25, 30)
    starting_height = plant.height

    print("=== Plant Growth Simulation ===")
    print(f"Starting: {plant.name} is {plant.height}cm tall")

    for day in range(7):
        plant.grow()
        plant.age()

    total_growth = plant.height - starting_height

    print(f"After 7 days: {plant.name} is {plant.height}cm tall")
    print(f"Total growth: +{total_growth}cm")
    print(f"Final age: {plant.age_days} days old")

if __name__ == "__main__":
    main()
