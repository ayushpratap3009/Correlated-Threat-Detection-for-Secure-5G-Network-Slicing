import os
import sys
import time
import random
import logging

# -------------------------------
# Fix Python path so "src" works
# -------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

# -------------------------------
# Now imports will work
# -------------------------------
from src.runtime.realtime_engine import Realtime5GEngine
from src.runtime.slice_traffic_generator import SliceTrafficGenerator

logging.basicConfig(level=logging.INFO)


def main():

    print("\n========== ATTACK BURST SIMULATION ==========\n")

    engine = Realtime5GEngine()

    generator = SliceTrafficGenerator()

    attacks = ["flood", "dos", "packet_spike"]

    print("\nStarting simulated traffic stream...\n")

    while True:

        # Generate normal traffic
        flow = generator.generate_normal_flow()

        # Only 5% chance of attack
        if random.random() < 0.05:

            attack = random.choice(attacks)

            flow = generator.amplify_attack(flow, attack)

            print(f"\n--- ATTACK BURST START ({attack.upper()}) ---")

        engine.process_flow(flow)

        time.sleep(0.2)


if __name__ == "__main__":
    main()
    