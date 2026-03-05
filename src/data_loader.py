# src/data_loader.py

import pandas as pd
import numpy as np
import hashlib
import logging
from typing import Tuple
from src.config import config


logger = logging.getLogger("DataLoader")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class DataLoader:

    def __init__(self):
        self.config = config

    # =====================================================
    # 5G FLOW LOADER
    # =====================================================

    def load_5g_flow_data(self, inject_attacks=True) -> pd.DataFrame:

        logger.info("Loading 5G flow dataset")

        df = pd.read_csv(self.config.FLOW_DATASET_PATH)

        logger.info(f"Original Flow Shape: {df.shape}")

        # Drop Flow_ID if exists
        if "Flow_ID" in df.columns:
            df.drop(columns=["Flow_ID"], inplace=True)

        # Fill missing
        df.fillna(0, inplace=True)

        if inject_attacks:
            df = self._inject_synthetic_attacks(df)

        self._log_dataset_fingerprint(df, "5G_FLOW")

        return df

    # =====================================================
    # MULTI-CLASS ATTACK INJECTION
    # =====================================================

    def _inject_synthetic_attacks(self, df: pd.DataFrame) -> pd.DataFrame:

        logger.info("Injecting synthetic multi-class attack patterns")

        df = df.copy()
        df["attack"] = 0  # 0 = normal

        attack_ratio = 0.20

        attack_indices = np.random.choice(
            df.index,
            size=int(len(df) * attack_ratio),
            replace=False
        )

        for idx in attack_indices:

            attack_type = np.random.choice(
                ["dos", "flood", "packet_spike"]
            )

            if attack_type == "dos":
                if "Total_Packets" in df.columns:
                    df.loc[idx, "Total_Packets"] *= 8
                df.loc[idx, "attack"] = 1

            elif attack_type == "flood":
                if "Total_Bytes" in df.columns:
                    df.loc[idx, "Total_Bytes"] *= 6
                df.loc[idx, "attack"] = 2

            elif attack_type == "packet_spike":
                if "Average_Packet_Size" in df.columns:
                    df.loc[idx, "Average_Packet_Size"] *= 5
                df.loc[idx, "attack"] = 3

        logger.info(f"Injected {len(attack_indices)} multi-class attack samples")

        return df

    # =====================================================
    # FEATURE / LABEL SPLIT
    # =====================================================

    def get_features_and_labels(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series]:

        if "attack" not in df.columns:
            raise RuntimeError("Label column 'attack' missing")

        X = df.drop(columns=["attack"])
        y = df["attack"]

        return X, y

    # =====================================================
    # FINGERPRINT
    # =====================================================

    def _log_dataset_fingerprint(self, df: pd.DataFrame, name: str):
        schema_str = ",".join(sorted(df.columns))
        fingerprint = hashlib.sha256(schema_str.encode()).hexdigest()[:12]
        logger.info(f"{name} dataset fingerprint: {fingerprint}")