import logging
from src.correlation.engine import CorrelationEngine

logger = logging.getLogger("AlertManager")


class AlertManager:

    def __init__(self):
        self.correlation_engine = CorrelationEngine()

    def add_alert(self, slice_type, attack_type, confidence, features=None):

        logger.info(
            f"Alert added | slice={slice_type} attack={attack_type} conf={confidence:.2f}"
        )

        event = self.correlation_engine.add_alert(
            slice_type,
            attack_type,
            confidence,
            features
        )

        if event:
            logger.warning(f"CORRELATED ATTACK EVENT: {event}")