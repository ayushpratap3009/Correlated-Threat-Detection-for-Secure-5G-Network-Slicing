import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sklearn.model_selection import train_test_split
from src.data_loader import DataLoader
from src.models.embb_model import EMBBModel
from src.models.urllc_model import URLLCModel
from src.models.miot_model import MIOTModel
from src.slice_creator import SliceCreator


def main():

    loader = DataLoader()
    df = loader.load_5g_flow_data()

    print("Splitting dataset...")
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    slice_classifier = SliceCreator()

    # Separate by slice
    slice_groups = {
        "embb": [],
        "urllc": [],
        "miot": []
    }

    for _, row in train_df.iterrows():
        slice_type = slice_classifier.classify(row.to_dict())
        slice_groups[slice_type].append(row)

    # Train models per slice
    for slice_type, rows in slice_groups.items():

        if len(rows) < 10:
            continue

        slice_df = pd.DataFrame(rows)

        # For now we create synthetic binary label
        # Later replaced with real attack labels
        slice_df["attack"] = 0

        X = slice_df.drop(columns=["attack"])
        y = slice_df["attack"]

        if slice_type == "embb":
            model = EMBBModel()
        elif slice_type == "urllc":
            model = URLLCModel()
        else:
            model = MIOTModel()

        model.train(X, y)
        model.save()

    print("5G slice models trained successfully.")


if __name__ == "__main__":
    main()