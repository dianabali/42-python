"""
Exception - the base class in Python for most errors that happen while a program is running.
Example:
    try:
        x = 10 / 0
    except Exception as error:
        print("An error occurred:", error)

You can also create your own exception:
    class MyError(Exception):
        pass
    raise MyError("Something went wrong")

Custom built-in exception classes:
- Exception - base class for most common exceptions
- ValueError - wrong value: int("hi")
- TypeError - wrong type: "2" + 4
- IndexError - invalid list index
- KeyError - missing dictionary key
- FileNotFoundError - file doesn't exist
- ZeroDivisionError - division by zero

Hierarchy:
    BaseException
        ├── Exception
        │   ├── ValueError
        │   ├── TypeError
        │   ├── IndexError
        │   └── ...
        ├── KeyboardInterrupt
        └── SystemExit
"""

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
