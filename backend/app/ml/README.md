# CrimeTrace AI — Machine Learning Integration Guide

This directory provides the architectural foundation, interfaces, and contracts for integrating machine learning models into **CrimeTrace AI** for predicting likely ATM cash-out locations.

## Architecture

The ML subsystem decouples model training, serialization, and inference from the core web service:

```
app/ml/
├── __init__.py
├── base.py             <- BasePredictor interface
├── schemas.py          <- MLFeatureVector & MLPredictionResponse schemas
├── stub_predictor.py   <- Operational heuristic baseline (active by default)
├── weights/            <- Place trained model weights (.onnx, .joblib, .pt)
└── README.md
```

## How to Plug in a Trained ML Model

1. **Train your model** (e.g., using CatBoost, XGBoost, Scikit-Learn, or Graph Neural Networks / PyTorch) on historical complaints and withdrawal data.
2. **Export model weights** to ONNX or Joblib into `app/ml/weights/`.
3. **Implement `BasePredictor`**:

```python
from app.ml.base import BasePredictor
from app.ml.schemas import MLPredictionResponse, ATMPredictionScore
import joblib

class ProductionMLPredictor(BasePredictor):
    def __init__(self, model_path: str = "app/ml/weights/model.joblib"):
        self.model = joblib.load(model_path)

    @property
    def model_name(self) -> str:
        return "CatBoost-Withdrawal-v1.0"

    def is_ready(self) -> bool:
        return self.model is not None

    async def extract_features(self, complaint_data, candidate_atms):
        # Feature extraction logic matching training preprocessing
        ...

    async def predict_withdrawal_locations(self, complaint_data, candidate_atms, top_k=5):
        # Model inference & probabilities
        ...
```

4. Set `ML_MODEL_ENABLED=true` in `.env`.
