import importlib
import importlib.metadata
import sys

REQUIRED_PACKAGES = {
    "pandas": "Data manipulation ready",
    "numpy": "Numerical computation ready",
    "matplotlib": "Visualization ready",
}


def check_package(name: str, description: str) -> bool:
    """Check if a package is installed. Returns True or False."""
    try:
        importlib.import_module(name)
    except ImportError:
        print(f"[MISSING] {name} - {description}")
        return False

    version = importlib.metadata.version(name)
    print(f"[OK] {name} ({version}) - {description}")
    return True


def show_install_help() -> None:
    print("\nSome packages are missing. Install them with pip:")
    print("    pip install -r requirements.txt")
    print("\nOr with Poetry:")
    print("    poetry install")
    print("    poetry run python loading.py")


def analyze_data() -> None:
    import numpy as np
    import pandas as pd
    import matplotlib
    matplotlib.use("Agg")  # to save images without opening a window
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    # Make 1000 random numbers
    values = np.random.normal(0, 1, 1000)
    print(f"Processing {len(values)} data points...")

    # Put them in a table and calculate a rolling average
    data = pd.DataFrame({"signal": values})
    data["rolling_mean"] = data["signal"].rolling(window=10).mean()

    # Draw and save the chart
    print("Generating visualization...")
    plt.plot(data["signal"], label="signal")
    plt.plot(data["rolling_mean"], label="rolling mean")
    plt.legend()
    plt.title("Matrix Data Analysis")
    plt.savefig("matrix_analysis.png")
    plt.close()

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")
    print("Checking dependencies:")

    all_installed = True
    for name, description in REQUIRED_PACKAGES.items():
        if not check_package(name, description):
            all_installed = False

    if not all_installed:
        show_install_help()
        sys.exit(1)

    analyze_data()


if __name__ == "__main__":
    main()
