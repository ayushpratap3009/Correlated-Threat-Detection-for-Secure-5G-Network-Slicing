import pandas as pd
import joblib
import logging

from src.runtime.alert_storage import save_alert
from src.correlation.engine import CorrelationEngine

logger = logging.getLogger("RealtimeEngine")
logger.setLevel(logging.INFO)


class Realtime5GEngine:

    def __init__(self):

        logger.info("Initializing realtime 5G detection engine...")

        self.model = joblib.load("models/embb_multiclass_model.pkl")

        self.correlation_engine = CorrelationEngine()

        self.attack_map = {
            0: "normal",
            1: "flood",
            2: "dos",
            3: "packet_spike"
        }

        logger.info("Realtime engine ready.")

    def calculate_severity(self, confidence):

        confidence = float(confidence)

        if confidence > 0.90:
            return "CRITICAL"

        elif confidence > 0.75:
            return "HIGH"

        elif confidence > 0.55:
            return "MEDIUM"

        else:
            return "LOW"

    def process_flow(self, flow):

        df = pd.DataFrame([flow])

        slice_type = str(df["slice_type"].iloc[0])

        model_df = df.drop(columns=["slice_type"])

        raw_prediction = int(self.model.predict(model_df)[0])

        attack_type = self.attack_map.get(raw_prediction, "unknown")

        confidence = float(max(self.model.predict_proba(model_df)[0]))

        severity = self.calculate_severity(confidence)

        print(
            f"Flow processed → Slice: {slice_type} | "
            f"Attack: {attack_type} | "
            f"Confidence: {confidence:.2f}"
        )

        if attack_type != "normal":

            alert = {
                "slice": slice_type,
                "attack": attack_type,
                "confidence": confidence,
                "severity": severity
            }

            save_alert(alert)

            self.correlation_engine.add_alert(
                slice_type,
                attack_type,
                confidence
            )