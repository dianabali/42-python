def input_temperature(temp_str) -> int:
    temp = int(temp_str)
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    temp = input("Input data is: ")
    try:
        temperature = input_temperature(temp)
        print(f"Temperature is now {temperature}°C")
    except Exception as error:
        print(f"Caught input_temperature error: {error}")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()