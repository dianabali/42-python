class Plant:
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
        print(f"Plant created: {self._name}: {self._height}cm, {self._age} days old")

    def get_height(self):
        return self._height

    def get_age(self):
        return self._age

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

    def show(self):
        print(f"Current state: {self._name}: {self._height}cm, {self._age} days old")


def main():
    print("=== Garden Security System ===")
    plant = Plant("Rose", 15.0, 10)
    plant.set_height(25)
    plant.set_age(30)
    plant.set_height(-5)
    plant.set_age(-5)
    plant.show()


if __name__ == "__main__":
    main()