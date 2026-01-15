import argparse
from src.config import config

def main():
    parser = argparse.ArgumentParser(description="5G Slice-Aware Security System")
    parser.add_argument(
        "--mode",
        choices=["development", "simulation", "lab"],
        default=config.mode,
        help="Run mode"
    )
    args = parser.parse_args()

    print("=" * 50)
    print("5G Slice-Aware & Correlated Threat Detection")
    print(f"Running Mode: {args.mode.upper()}")
    print("=" * 50)

    if args.mode == "development":
        print("Development mode initialized")
    elif args.mode == "simulation":
        print("Simulation mode initialized")
    elif args.mode == "lab":
        print("Lab mode initialized")

if __name__ == "__main__":
    main()
