# src/models/base_model.py

import joblib
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from src.config import config

logger = logging.getLogger("BaseModel")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class BaseModel(ABC):
    """
    Abstract base class for all slice-specific ML models.
    Enforces a strict interface.
    """

    def __init__(self, slice_type: str, version: str = "v1.0"):
        self.slice_type = slice_type
        self.version = version
        self.model = None

        self.model_path = (
            Path(config.MODELS_DIR) / f"{slice_type}_model_{version}.pkl"
        )

    @abstractmethod
    def build_model(self) -> Any:
        """
        Create and return the ML model instance.
        """
        pass

    def train(self, X, y):
        logger.info(f"Training model for slice: {self.slice_type}")
        self.model = self.build_model()
        self.model.fit(X, y)
        logger.info("Training completed")

    def predict(self, X):
        self._ensure_model_loaded()
        return self.model.predict(X)

    def predict_proba(self, X):
        self._ensure_model_loaded()
        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(X)
        raise RuntimeError("Model does not support probability prediction")

    def save(self):
        self.model_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, self.model_path)
        logger.info(f"Model saved to {self.model_path}")

    def load(self):
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        self.model = joblib.load(self.model_path)
        logger.info(f"Model loaded from {self.model_path}")

    def _ensure_model_loaded(self):
        if self.model is None:
            raise RuntimeError(
                f"Model for slice '{self.slice_type}' is not loaded or trained"
            )
