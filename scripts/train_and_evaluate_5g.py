import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import numpy as np
import joblib
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)
from xgboost import XGBClassifier
from src.data_loader import DataLoader


def main():

    print("\n========== 5G MULTI-CLASS ATTACK CLASSIFICATION ==========")

    loader = DataLoader()
    df = loader.load_5g_flow_data(inject_attacks=True)

    X, y = loader.get_features_and_labels(df)

    model = XGBClassifier(
        objective="multi:softprob",
        num_class=4,
        eval_metric="mlogloss",
        random_state=42,
        n_estimators=150,
        max_depth=6,
        learning_rate=0.05,
        n_jobs=-1
    )

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    acc_scores = []
    f1_scores = []

    fold = 1

    for train_idx, val_idx in skf.split(X, y):

        print(f"\n--- Fold {fold} ---")

        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)

        acc = accuracy_score(y_val, y_pred)
        f1 = f1_score(y_val, y_pred, average="weighted")

        acc_scores.append(acc)
        f1_scores.append(f1)

        print(f"Accuracy : {acc:.4f}")
        print(f"F1-score : {f1:.4f}")
        print("Confusion Matrix:")
        print(confusion_matrix(y_val, y_pred))

        fold += 1

    print("\n========== FINAL MULTI-CLASS RESULTS ==========")
    print(f"Accuracy : {np.mean(acc_scores):.4f}")
    print(f"F1-score : {np.mean(f1_scores):.4f}")

    # ================================
    # Train on full dataset
    # ================================

    print("\nTraining final production model on full dataset...")
    model.fit(X, y)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/embb_multiclass_model.pkl")

    print("Model saved to models/embb_multiclass_model.pkl")

    # ================================
    # Feature Importance
    # ================================

    print("\n========== FEATURE IMPORTANCE ==========")

    importances = model.feature_importances_

    feature_importance = sorted(
        zip(X.columns, importances),
        key=lambda x: x[1],
        reverse=True
    )

    for feature, score in feature_importance:
        print(f"{feature:25s} : {score:.4f}")


if __name__ == "__main__":
    main()