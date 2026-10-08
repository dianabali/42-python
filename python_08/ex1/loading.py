import sys
import importlib

"""
    (module name, purpose) - checked dynamically so a missing package
    never crashes the program with a raw ImportError.
"""
REQUIRED = [
    ("pandas", "Data manipulation"),
    ("numpy", "Numerical computation"),
    ("matplotlib", "Visualization"),
]


def check_dependencies():
    """Try to import each package. Return (loaded modules, missing names)"""
    modules = {}
    missing = []
    print("Checking dependencies:")
    for name, purpose in REQUIRED:
        try:
            mod = importlib.import_module(name)
            version = getattr(mod, "__version__", "unknown")
            print(f"[OK] {name} ({version}) - {purpose} ready")
            modules[name] = mod
        except ImportError:
            print(f"[MISSING] {name} - {purpose} unavailable")
            missing.append(name)
    return modules, missing


def print_install_help(missing):
    print()
    print(f"Missing dependencies: {', '.join(missing)}")
    print()
    print("Install with pip:")
    print("    pip install -r requirements.txt")
    print("    python3 loading.py")
    print()
    print("Install with Poetry:")
    print("    poetry install")
    print("    poetry run python loading.py")
    print("OR")
    print("    python3 -m poetry install")
    print("    python3 -m run python loading.py")


def detect_environment():
    """Guess how the current interpreter was set up, using only sys."""
    in_venv = sys.prefix != sys.base_prefix
    prefix = sys.prefix.lower()
    if "pypoetry" in prefix or "poetry" in prefix:
        return "Poetry-managed virtual environment"
    if in_venv:
        return "Virtual environment (pip / venv)"
    return "Global/system interpreter (pip)"


def compare_pip_poetry(modules):
    """Show installed versions and the pip vs Poetry differences."""
    print()
    print("=== Package versions in this environment ===")
    for name, _ in REQUIRED:
        version = getattr(modules[name], "__version__", "unknown")
        print(f"  {name:<12} {version}")
    print(f"  Python       {sys.version.split()[0]}")
    print(f"  Environment  {detect_environment()}")
    print()
    print("=== pip vs Poetry ===")
    rows = [
        ("Dependency file", "requirements.txt", "pyproject.toml"),
        ("Install command", "pip install -r ...", "poetry install"),
        ("Lock file", "none (manual freeze)", "poetry.lock (automatic)"),
        ("Dependency resolver", "basic", "full, conflict-aware"),
        ("Virtual env", "manual (venv)", "created automatically"),
        ("Run command", "python3 loading.py", "poetry run python loading.py"),
    ]
    print(f"  {'Feature':<20}{'pip':<24}{'Poetry'}")
    for feature, pip_v, poetry_v in rows:
        print(f"  {feature:<20}{pip_v:<24}{poetry_v}")


def generate_matrix_data(np, pd, n=1000):
    """Simulate Matrix data entirely with numpy."""
    rng = np.random.default_rng()
    # rng = np.random.default_rng(42) - for the same graph
    sectors = np.array(["Zion", "Nebuchadnezzar", "Construct", "Mainframe"])
    df = pd.DataFrame({
        "signal_strength": rng.normal(loc=50, scale=15, size=n),
        "anomaly_level": rng.exponential(scale=2.0, size=n),
        "sector": rng.choice(sectors, size=n),
    })
    # Correlate a latency metric with anomalies for a more interesting plot
    df["latency_ms"] = 20 + 5 * df["anomaly_level"] + rng.normal(0, 4, size=n)
    return df


def analyze_and_plot(modules, filename="matrix_analysis.png"):
    np = modules["numpy"]
    pd = modules["pandas"]
    plt = modules["matplotlib"].pyplot

    print()
    print("Analyzing Matrix data...")
    df = generate_matrix_data(np, pd)
    print(f"Processing {len(df)} data points...")

    stats = df.groupby("sector")["signal_strength"].agg(["mean", "std"])
    print(stats.round(2).to_string())

    print("Generating visualization...")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(df["signal_strength"], bins=30, color="green", edgecolor="black")
    ax.set_title("Matrix Data: Signal Strength Distribution")
    ax.set_xlabel("Signal strength")
    ax.set_ylabel("Count")
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)

    print("Analysis complete!")
    print(f"Results saved to: {filename}")


def main():
    print("LOADING STATUS: Loading programs...")
    print()
    modules, missing = check_dependencies()
    if missing:
        print_install_help(missing)
        sys.exit(1)

    # Headless-safe backend: we only save to a file
    modules["matplotlib"].use("Agg")
    modules["matplotlib.pyplot"] = importlib.import_module("matplotlib.pyplot")
    modules["matplotlib"].pyplot = modules["matplotlib.pyplot"]

    compare_pip_poetry(modules)
    analyze_and_plot(modules)


if __name__ == "__main__":
    main()
