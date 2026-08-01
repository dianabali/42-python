import sys

print("=== Command Quest ===")
print("Program name:", sys.argv[0])

if len(sys.argv) == 1:
    print("No arguments provided!")
else:
    print("Arguments received:", len(sys.argv) - 1)

    i = 1
    while i < len(sys.argv):
        print("Argument:", i, ":", sys.argv[i])
        i += 1

print("Total arguments:", len(sys.argv))
