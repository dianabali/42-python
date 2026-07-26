class Plant:
    class Stats:
        def __init__(self):
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def record_grow(self):
            self._grow_calls += 1

        def record_age(self):
            self._age_calls += 1

        def record_show(self):
            self._show_calls += 1

        def display(self):
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, {self._show_calls} show")

    def __init__(self, name, height=0.0, age=0):
        self._name = name
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            self._height = 0.0
        else:
            self._height = height
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            self._age = 0
        else:
            self._age = age
        self._stats = self._create_stats()

    def _create_stats(self):
        return Plant.Stats()

    @staticmethod
    def is_older_than_year(age):
        return age > 365

    @classmethod
    def create_anonymous(cls):
        return cls("Unknown plant", 0.0, 0)

    def get_name(self):
        return self._name

    def get_height(self):
        return self._height

    def get_age(self):
        return self._age

    def get_stats(self):
        return self._stats

    def set_height(self, height):
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
            print(f"Height updated: {round(self._height)}cm")

    def set_age(self, age):
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = age
            print(f"Age updated: {self._age} days")

    def grow(self, amount):
        self._height += amount
        self._stats.record_grow()

    def age(self, days):
        self._age += days
        self._stats.record_age()

    def show(self):
        print(f"{self._name}: {self._height}cm, {self._age} days old")
        self._stats.record_show()


class Flower(Plant):
    def __init__(self, name, height=0.0, age=0, color=""):
        super().__init__(name, height, age)
        self._color = color
        self._bloomed = False

    def bloom(self):
        self._bloomed = True

    def show(self):
        super().show()
        print(f"Color: {self._color}")
        if self._bloomed:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    class Stats(Plant.Stats):
        def __init__(self):
            super().__init__()
            self._shade_calls = 0

        def record_shade(self):
            self._shade_calls += 1

        def display(self):
            super().display()
            print(f"{self._shade_calls} shade")

    def __init__(self, name, height=0.0, age=0, trunk_diameter=0.0):
        super().__init__(name, height, age)
        self._trunk_diameter = trunk_diameter

    def _create_stats(self):
        return Tree.Stats()

    def produce_shade(self):
        print(f"Tree {self._name} now produces a shade of "
              f"{self._height}cm long and {self._trunk_diameter}cm wide.")
        self._stats.record_shade()

    def show(self):
        super().show()
        print(f"Trunk diameter: {self._trunk_diameter}cm")


class Vegetable(Plant):
    def __init__(self, name, height=0.0, age=0, harvest_season="", nutritional_value=0):
        super().__init__(name, height, age)
        self._harvest_season = harvest_season
        self._nutritional_value = nutritional_value

    def grow(self):
        super().grow(2.1)

    def age(self):
        super().age(1)
        self._nutritional_value += 1

    def show(self):
        super().show()
        print(f"Harvest season: {self._harvest_season}")
        print(f"Nutritional value: {self._nutritional_value}")


class Seed(Flower):
    def __init__(self, name, height=0.0, age=0, color="", seeds=0):
        super().__init__(name, height, age, color)
        self._seeds = seeds

    def bloom(self):
        super().bloom()
        self._seeds = 42

    def show(self):
        super().show()
        print(f"Seeds: {self._seeds}")


def display_stats(plant):
    print(f"[statistics for {plant.get_name()}]")
    plant.get_stats().display()


def main():
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> {Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> {Plant.is_older_than_year(400)}")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow(8)
    rose.bloom()
    rose.show()
    display_stats(rose)

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)

    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow")
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow(30)
    sunflower.age(20)
    sunflower.bloom()
    sunflower.show()
    display_stats(sunflower)

    print("=== Anonymous")
    unknown = Plant.create_anonymous()
    unknown.show()
    display_stats(unknown)


if __name__ == "__main__":
    main()