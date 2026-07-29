def garden_operations(operation_number):
	if operation_number == 0:
		int("abc")
	elif operation_number == 1:
		5 / 0
	elif operation_number == 2:
		open("/non/existent/file")
	elif operation_number == 3:
		"abc" + 10
	else:
		return

def test_error_types():
	print("=== Garden Error Tyeps Demo ===")

	for operation_number in range(5):
		print(f"Testing operation {operation_number}...")

		try:
			garden_operations(operation_number)
		except ValueError as error:
			print(f"Caught ValueError: {error}")
		except ZeroDivisionError as error:
			print(f"Caught ZeroDivisionError: {error}")
		except FileNotFoundError as error:
			print(f"Caught FileNotFoundError: {error}")
		except TypeError as error:
			print(f"Caught TypeError: {error}")
		else:
			print("Operation completed successfully")
	print()
	print("All error types tested successfully!")

if __name__ == "__main__":
	test_error_types()