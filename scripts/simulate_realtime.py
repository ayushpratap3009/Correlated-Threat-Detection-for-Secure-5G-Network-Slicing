import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import DataLoader
from src.runtime.realtime_engine import Realtime5GEngine


def main():

    print("\n========== REALTIME TRAFFIC SIMULATION ==========")

    loader = DataLoader()
    df = loader.load_5g_flow_data(inject_attacks=True)

    engine = Realtime5GEngine()

    print("\nStarting traffic stream...\n")

    for _, row in df.iterrows():

        flow = row.to_dict()

        engine.process_flow(flow)

        time.sleep(0.25)


if __name__ == "__main__":
    main()