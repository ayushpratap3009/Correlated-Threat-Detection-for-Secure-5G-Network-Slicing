from src.slice_creator import SliceCreator
from src.correlation.engine import CorrelationEngine
from src.models.embb_model import EMBBModel
from src.models.urllc_model import URLLCModel
from src.models.miot_model import MIOTModel


def simulate_pipeline(sample_features):

    slice_creator = SliceCreator()
    engine = CorrelationEngine()

    slice_type = slice_creator.classify(sample_features)

    if slice_type == "embb":
        model = EMBBModel()
    elif slice_type == "urllc":
        model = URLLCModel()
    else:
        model = MIOTModel()

    model.load()

    prediction = model.predict([list(sample_features.values())])[0]

    if prediction == 1:
        event = engine.add_alert(
            slice_type=slice_type,
            attack_type="anomaly",
            confidence=0.85,
            features=sample_features
        )

        if event:
            print("🚨 Coordinated Attack Detected:", event)