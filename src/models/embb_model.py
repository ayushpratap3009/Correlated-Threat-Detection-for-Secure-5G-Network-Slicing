# src/models/embb_model.py

from xgboost import XGBClassifier
from src.models.base_model import BaseModel
from src.config import config


class EMBBModel(BaseModel):
    def __init__(self, version: str = "v1.0"):
        super().__init__("embb", version)

    def build_model(self):
        params = config.MODEL_PARAMS["embb"]

        return XGBClassifier(
            n_estimators=params["n_estimators"],
            max_depth=params["max_depth"],
            learning_rate=params["learning_rate"],
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1
        )
