# src/config.py
import os
from pathlib import Path


class Config:
    """
    Central configuration for the 5G Slice-Aware
    Correlated Threat Detection System
    """

    # =========================
    # PROJECT PATHS
    # =========================
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATA_DIR = BASE_DIR / "data"
    MODELS_DIR = DATA_DIR / "models"

    # =========================
    # DATASET PATHS (UNSW-NB15)
    # =========================
    UNSW_TRAIN_PATH = DATA_DIR / "raw" / "UNSW_NB15_training-set.csv"
    UNSW_TEST_PATH = DATA_DIR / "raw" / "UNSW_NB15_testing-set.csv"

    # =========================
    # FEATURE MAPPING
    # UNSW → 5G-LIKE FEATURES
    # =========================
    FEATURE_MAPPING = {
        "dur": "duration",
        "spkts": "src_packets",
        "dpkts": "dst_packets",
        "sbytes": "src_bytes",
        "dbytes": "dst_bytes",
        "rate": "packet_rate",
        "sload": "src_load",
        "dload": "dst_load",
        "sinpkt": "src_inter_arrival",
        "dinpkt": "dst_inter_arrival",
        "sttl": "src_ttl",
        "dttl": "dst_ttl",
    }

    # =========================
    # SLICE CLASSIFICATION THRESHOLDS
    # =========================
    SLICE_THRESHOLDS = {
        "urllc": {
            "max_latency": 5,
            "min_reliability": 0.999
        },
        "embb": {
            "min_throughput": 50
        },
        "miot": {
            "max_packet_size": 100,
            "max_connections": 1000
        }
    }

    # =========================
    # MODEL PARAMETERS
    # =========================
    MODEL_PARAMS = {
        "embb": {
            "model": "xgboost",
            "n_estimators": 100,
            "max_depth": 6,
            "learning_rate": 0.1
        },
        "urllc": {
            "model": "random_forest",
            "n_estimators": 150,
            "max_depth": 4,
            "min_samples_split": 20
        },
        "miot": {
            "model": "lightgbm",
            "n_estimators": 80,
            "num_leaves": 31,
            "learning_rate": 0.05
        }
    }

    # =========================
    # CORRELATION ENGINE
    # =========================
    CORRELATION_WINDOW = 5.0  # seconds
    MIN_SLICES_FOR_COORDINATION = 2
    CONFIDENCE_THRESHOLD = 0.7

    # =========================
    # ENVIRONMENT DETECTION
    # =========================
    @staticmethod
    def is_linux():
        return os.name == "posix"

    @staticmethod
    def is_lab_environment():
        lab_indicators = [
            "/etc/open5gs",
            "/var/log/open5gs",
            "/usr/bin/nrf"
        ]
        return any(os.path.exists(path) for path in lab_indicators)

    @property
    def mode(self):
        return "lab" if self.is_lab_environment() else "development"


# Global config instance
config = Config()
