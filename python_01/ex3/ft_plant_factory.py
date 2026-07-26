class Plant:
    def __init__(self, name, height, age):
        self.name = name
        self.height = height
        self.age = age

    def show(self):
        print(f"{self.name}: {self.height:.1f}cm, {self.age} days old")

def main():
    rose = Plant("Rose", 25.0, 30)
    oak = Plant("Oak", 200.0, 365)
    cactus = Plant("Cactus", 5.0, 90)
    sunflower = Plant("Sunflower", 80.0, 45)
    fern = Plant("Fern", 15.0, 120)

    print("=== Plant Factory Output ===")

    print("Created:", end=" ")
    rose.show()

    print("Created:", end=" ")
    oak.show()

    print("Created:", end=" ")
    cactus.show()

    print("Created:", end=" ")
    sunflower.show()

    print("Created:", end=" ")
    fern.show()

if __name__ == "__main__":
    main()
