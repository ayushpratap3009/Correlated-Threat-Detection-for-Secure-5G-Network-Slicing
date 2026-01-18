# src/models/urllc_model.py

from sklearn.ensemble import RandomForestClassifier
from src.models.base_model import BaseModel
from src.config import config


class URLLCModel(BaseModel):
    def __init__(self, version: str = "v1.0"):
        super().__init__("urllc", version)

    def build_model(self):
        params = config.MODEL_PARAMS["urllc"]

        return RandomForestClassifier(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            min_samples_split=params["min_samples_split"],
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )
