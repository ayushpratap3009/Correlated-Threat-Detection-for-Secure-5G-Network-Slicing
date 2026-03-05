import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

from src.data_loader import DataLoader
from src.models.embb_model import EMBBModel
from src.models.urllc_model import URLLCModel
from src.models.miot_model import MIOTModel


def evaluate(model, X, y, name):
    y_pred = model.predict(X)

    acc = accuracy_score(y, y_pred)
    prec = precision_score(y, y_pred)
    rec = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    cm = confusion_matrix(y, y_pred)

    print(f"\n===== {name} MODEL RESULTS =====")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)

    # False Positive Rate
    fp = cm[0][1]
    tn = cm[0][0]
    fpr = fp / (fp + tn)

    print(f"False Positive Rate: {fpr:.4f}")

    return {
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1-score": f1,
        "False Positive Rate": fpr
    }


def main():
    print("\n[INFO] Loading dataset...")
    loader = DataLoader()
    train_df, _ = loader.load_data()
    X, y = loader.get_features_and_labels(train_df)

    print("\n[INFO] Loading trained models...")
    embb = EMBBModel()
    embb.load()

    urllc = URLLCModel()
    urllc.load()

    miot = MIOTModel()
    miot.load()

    results = []
    results.append(evaluate(embb, X, y, "eMBB"))
    results.append(evaluate(urllc, X, y, "URLLC"))
    results.append(evaluate(miot, X, y, "mIoT"))

    df = pd.DataFrame(results)
    print("\n===== FINAL COMPARISON TABLE =====")
    print(df)


if __name__ == "__main__":
    main()