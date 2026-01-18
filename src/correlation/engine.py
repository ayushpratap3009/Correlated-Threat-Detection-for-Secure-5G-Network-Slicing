# src/correlation/engine.py

import logging
from collections import deque
from datetime import datetime, timedelta
from typing import Dict, List
from src.config import config

logger = logging.getLogger("CorrelationEngine")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class CorrelationEngine:
    """
    Detects coordinated attacks across 5G slices using
    temporal correlation and confidence scoring.
    """

    def __init__(self):
        self.window = timedelta(seconds=config.CORRELATION_WINDOW)
        self.min_slices = config.MIN_SLICES_FOR_COORDINATION
        self.alerts = deque(maxlen=1000)

    # =============================
    # Public API
    # =============================
    def add_alert(
        self,
        slice_type: str,
        attack_type: str,
        confidence: float,
        features: Dict = None
    ) -> Dict | None:
        """
        Add a new alert and check for correlation.
        """
        alert = {
            "timestamp": datetime.utcnow(),
            "slice": slice_type,
            "attack": attack_type,
            "confidence": confidence,
            "features": features or {}
        }

        self.alerts.append(alert)
        logger.info(
            f"Alert added | slice={slice_type} attack={attack_type} conf={confidence:.2f}"
        )

        return self._check_correlation()

    # =============================
    # Internal logic
    # =============================
    def _check_correlation(self) -> Dict | None:
        """
        Check if recent alerts indicate a coordinated attack.
        """
        now = datetime.utcnow()
        recent_alerts = [
            a for a in self.alerts
            if now - a["timestamp"] <= self.window
        ]

        if len(recent_alerts) < self.min_slices:
            return None

        # Group alerts by slice
        slice_map: Dict[str, List[Dict]] = {}
        for alert in recent_alerts:
            slice_map.setdefault(alert["slice"], []).append(alert)

        if len(slice_map) < self.min_slices:
            return None

        confidence = self._compute_confidence(slice_map)

        if confidence < config.CONFIDENCE_THRESHOLD:
            return None

        correlation_event = {
            "type": "coordinated_attack",
            "timestamp": datetime.utcnow().isoformat(),
            "slices": list(slice_map.keys()),
            "confidence": round(confidence, 3),
            "alerts": recent_alerts
        }

        logger.warning(
            f"COORDINATED ATTACK DETECTED | slices={correlation_event['slices']} "
            f"confidence={correlation_event['confidence']}"
        )

        return correlation_event

    def _compute_confidence(self, slice_map: Dict[str, List[Dict]]) -> float:
        """
        Compute confidence based on:
        - Number of slices involved
        - Average alert confidence
        """
        slice_count_score = len(slice_map) / 3.0  # normalize (3 slices max)

        alert_confidences = [
            a["confidence"]
            for alerts in slice_map.values()
            for a in alerts
        ]
        avg_confidence = sum(alert_confidences) / len(alert_confidences)

        return round(0.5 * slice_count_score + 0.5 * avg_confidence, 3)
