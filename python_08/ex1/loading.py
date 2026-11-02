import importlib # for dynamic imports
import importlib.metadata
import sys

REQUIRED_PACKAGES = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def check_package(name: str, description: str) -> bool:
    try:
        importlib.import_module(name)
    except ImportError:
        print(f"[MISSING] {name} - {description}")
        return False

    try:
        version = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        version = "????"

    print(f"[OK] {name} ({version}) - {description}")
    return True


def show_install_help() -> None:
    print()
    print("Some packages are missing. Install them with pip:")
    print("    pip install -r requirements.txt")
    print()
    print("Or with Poetry:")
    print("    pip install poetry")
    print("    poetry install")
    print("    poetry run python loading.py")


def analyze_data() -> None:
    import numpy as n # random nums + ops
    import pandas as p # org into tabs + avg
    import matplotlib # creates graph
    matplotlib.use("Agg")  # to save images without opening a window
    import matplotlib.pyplot as m # draw graph

    print()
    print("Analyzing Matrix data...")

    # Make 1000 random numbers
    values = n.random.normal(0, 1, 1000)
    print(f"Processing {len(values)} data points...")

    # Put them in a table and calculate the average
    # DataFrame - table
    data = p.DataFrame({"signal": values})

    # Calculate the average
    # Create a window with 10 consecutive values
    data["rolling_mean"] = data["signal"].rolling(window=10).mean()

    # Draw and save the chart
    # plot - creates a line graph
    print("Generating visualization...")
    m.plot(data["signal"], label="signal") # values  + line name
    m.plot(data["rolling_mean"], label="rolling mean") # avg line
    m.legend()
    m.title("Matrix Data Analysis")
    m.savefig("matrix_analysis.png")
    m.close()

    print()
    print("Analysis complete!")
    print("Results saved to: matrix_analysis.png")


def pip_vs_poetry() -> None:
    print("=== Pip vs. Poetry ===")
    print("Pip is Python's standard package management tool.")
    print("It is good for installing single packages.")
    print("Poetry a dependency and package management tool for Python.")
    print("Automates package management.")
    print("Manages the entire project dependencies (installing, versions, venvs).")


def main() -> None:
    print("LOADING STATUS: Loading programs...")
    print()
    print("Checking dependencies:")

    all_installed = True
    for name, description in REQUIRED_PACKAGES.items():
        if not check_package(name, description):
            all_installed = False

    if not all_installed:
        show_install_help()
        sys.exit(1)

    analyze_data()
    pip_vs_poetry()


if __name__ == "__main__":
    main()
