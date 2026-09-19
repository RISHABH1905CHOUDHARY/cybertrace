"""Abstract Base Class and Protocol interface for Machine Learning Predictors."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.ml.schemas import MLFeatureVector, MLPredictionResponse


class BasePredictor(ABC):
    """
    Abstract Predictor defining the interface for ML models forecasting
    likely ATM withdrawal locations for cybercrime complaints.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Name and version identifier of the model."""
        pass

    @abstractmethod
    def is_ready(self) -> bool:
        """Check if model weights are loaded and ready for inference."""
        pass

    @abstractmethod
    async def extract_features(
        self,
        complaint_data: Dict[str, Any],
        candidate_atms: List[Dict[str, Any]],
    ) -> List[MLFeatureVector]:
        """Extract tabular / spatial feature vectors from complaint and ATM candidates."""
        pass

    @abstractmethod
    async def predict_withdrawal_locations(
        self,
        complaint_data: Dict[str, Any],
        candidate_atms: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> MLPredictionResponse:
        """Generate ranked ATM withdrawal predictions and probabilities."""
        pass
