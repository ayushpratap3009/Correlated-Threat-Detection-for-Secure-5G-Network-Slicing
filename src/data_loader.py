# src/data_loader.py

import pandas as pd
import hashlib
import logging
from typing import Tuple
from src.config import config

# -----------------------------
# Logging configuration
# -----------------------------
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
    """
    Production-grade data loader for UNSW-NB15.
    Handles:
    - Validation
    - Preprocessing
    - Reproducibility
    """

    REQUIRED_COLUMNS = {"label"}

    def __init__(self):
        self.config = config

    # =============================
    # Public API
    # =============================
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load and preprocess train & test datasets.
        """
        logger.info("Loading UNSW-NB15 datasets")

        train_df = self._safe_read_csv(self.config.UNSW_TRAIN_PATH)
        test_df = self._safe_read_csv(self.config.UNSW_TEST_PATH)

        logger.info(f"Train shape before processing: {train_df.shape}")
        logger.info(f"Test  shape before processing: {test_df.shape}")

        self._validate_schema(train_df)
        self._validate_schema(test_df)

        train_df = self._preprocess(train_df)
        test_df = self._preprocess(test_df)

        logger.info("Dataset preprocessing completed")

        self._log_dataset_fingerprint(train_df, dataset_type="train")

        return train_df, test_df

    def get_features_and_labels(
        self, df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Split features (X) and labels (y).
        """
        if "attack" not in df.columns:
            raise RuntimeError("Label column 'attack' missing after preprocessing")

        X = df.drop(columns=["attack"])
        y = df["attack"]

        return X, y

    # =============================
    # Internal helpers
    # =============================
    def _safe_read_csv(self, path):
        try:
            return pd.read_csv(path)
        except FileNotFoundError:
            logger.error(f"Dataset not found: {path}")
            raise
        except Exception as e:
            logger.exception("Failed to read dataset")
            raise

    def _validate_schema(self, df: pd.DataFrame):
        missing = self.REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Dataset missing required columns: {missing}")

    def _preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        # -----------------------------
        # Feature mapping
        # -----------------------------
        df = df.rename(columns=self.config.FEATURE_MAPPING)

        # -----------------------------
        # Binary label creation
        # -----------------------------
        df["attack"] = df["label"].apply(lambda x: 0 if x == 0 else 1)
        df.drop(columns=["label"], inplace=True)

        # -----------------------------
        # Drop non-numeric features
        # -----------------------------
        non_numeric = df.select_dtypes(include=["object"]).columns
        df.drop(columns=non_numeric, inplace=True)

        # -----------------------------
        # Missing value handling
        # -----------------------------
        df.fillna(0, inplace=True)

        return df

    def _log_dataset_fingerprint(self, df: pd.DataFrame, dataset_type: str):
        """
        Hash dataset schema for reproducibility tracking.
        """
        schema_str = ",".join(sorted(df.columns))
        fingerprint = hashlib.sha256(schema_str.encode()).hexdigest()[:12]

        logger.info(
            f"{dataset_type.upper()} dataset fingerprint: {fingerprint}"
        )
