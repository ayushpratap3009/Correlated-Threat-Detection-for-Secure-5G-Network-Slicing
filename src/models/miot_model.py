# src/models/miot_model.py

from lightgbm import LGBMClassifier
from src.models.base_model import BaseModel
from src.config import config


class MIOTModel(BaseModel):
    def __init__(self, version: str = "v1.0"):
        super().__init__("miot", version)

    def build_model(self):
        params = config.MODEL_PARAMS["miot"]

        return LGBMClassifier(
            n_estimators=params["n_estimators"],
            num_leaves=params["num_leaves"],
            learning_rate=params["learning_rate"],
            random_state=42,
            n_jobs=-1
        )
