# src/slice_creator.py

import logging
from typing import Dict
from src.config import config

# -----------------------------
# Logging configuration
# -----------------------------
logger = logging.getLogger("SliceCreator")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class SliceCreator:
    """
    Deterministic slice classifier for 5G traffic.
    Priority order:
        1. URLLC
        2. eMBB
        3. mIoT (default)
    """

    def __init__(self):
        self.thresholds = config.SLICE_THRESHOLDS

    def classify(self, features: Dict) -> str:
        """
        Classify traffic into a 5G slice based on features.

        Returns:
            'urllc', 'embb', or 'miot'
        """

        try:
            # -----------------------------
            # 1. URLLC — highest priority
            # -----------------------------
            if self._is_urllc(features):
                return "urllc"

            # -----------------------------
            # 2. eMBB — high throughput
            # -----------------------------
            if self._is_embb(features):
                return "embb"

            # -----------------------------
            # 3. mIoT — default fallback
            # -----------------------------
            return "miot"

        except Exception as e:
            logger.exception("Slice classification failed")
            # Fail-safe: never crash pipeline
            return "miot"

    # =============================
    # Internal classification rules
    # =============================
    def _is_urllc(self, f: Dict) -> bool:
        """
        URLLC: ultra-low latency, high reliability
        """
        latency = f.get("src_inter_arrival", float("inf"))
        reliability = f.get("reliability", 1.0)

        return (
            latency <= self.thresholds["urllc"]["max_latency"]
            and reliability >= self.thresholds["urllc"]["min_reliability"]
        )

    def _is_embb(self, f: Dict) -> bool:
        """
        eMBB: high throughput traffic
        """
        src_load = f.get("src_load", 0)
        dst_load = f.get("dst_load", 0)

        return (
            src_load >= self.thresholds["embb"]["min_throughput"]
            or dst_load >= self.thresholds["embb"]["min_throughput"]
        )
