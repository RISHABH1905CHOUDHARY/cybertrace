"""Heuristic baseline / stub predictor implementing BasePredictor."""

from datetime import datetime, timezone
from typing import Any, Dict, List
from app.ml.base import BasePredictor
from app.ml.schemas import ATMPredictionScore, MLFeatureVector, MLPredictionResponse
from app.utils.geo import haversine_distance_km


class StubPredictor(BasePredictor):
    """
    Default rule-based predictor that serves as an operational baseline
    prior to training and deploying full ML/Deep Learning weights.
    """

    @property
    def model_name(self) -> str:
        return "HeuristicSpatial-Baseline-v1.0"

    def is_ready(self) -> bool:
        return True

    async def extract_features(
        self,
        complaint_data: Dict[str, Any],
        candidate_atms: List[Dict[str, Any]],
    ) -> List[MLFeatureVector]:
        vectors = []
        c_lat = complaint_data.get("latitude", 0.0)
        c_lon = complaint_data.get("longitude", 0.0)
        c_amt = complaint_data.get("amount", 0.0)

        for atm in candidate_atms:
            dist = haversine_distance_km(c_lat, c_lon, atm.get("latitude", 0.0), atm.get("longitude", 0.0))
            vectors.append(
                MLFeatureVector(
                    complaint_amount=c_amt,
                    fraud_type_encoded=1,
                    hour_of_day=datetime.now().hour,
                    day_of_week=datetime.now().weekday(),
                    latitude=c_lat,
                    longitude=c_lon,
                    distance_to_atm_km=dist,
                    atm_historical_fraud_count=atm.get("fraud_count", 0),
                    atm_historical_fraud_volume=atm.get("fraud_volume", 0.0),
                    district_risk_index=0.75,
                )
            )
        return vectors

    async def predict_withdrawal_locations(
        self,
        complaint_data: Dict[str, Any],
        candidate_atms: List[Dict[str, Any]],
        top_k: int = 5,
    ) -> MLPredictionResponse:
        c_lat = complaint_data.get("latitude", 0.0)
        c_lon = complaint_data.get("longitude", 0.0)
        complaint_id = complaint_data.get("complaint_id", "N/A")

        scores: List[ATMPredictionScore] = []
        for atm in candidate_atms:
            dist = haversine_distance_km(c_lat, c_lon, atm.get("latitude", 0.0), atm.get("longitude", 0.0))
            # Distance decay: closer ATM -> higher baseline probability
            proximity_score = max(0.05, 1.0 - (dist / 15.0))
            fraud_history_score = min(0.4, (atm.get("fraud_count", 0) * 0.1))
            prob = round(min(0.98, max(0.05, (proximity_score * 0.6) + fraud_history_score)), 3)

            scores.append(
                ATMPredictionScore(
                    atm_id=atm.get("atm_id", ""),
                    bank_name=atm.get("bank_name", ""),
                    branch_name=atm.get("branch_name", ""),
                    latitude=atm.get("latitude", 0.0),
                    longitude=atm.get("longitude", 0.0),
                    distance_km=round(dist, 2),
                    withdrawal_probability=prob,
                    predicted_rank=0,  # will assign below
                    estimated_time_window_hours="2 to 4 hours post-incident",
                    feature_importances={
                        "proximity_decay": round(proximity_score, 2),
                        "historical_fraud_pattern": round(fraud_history_score, 2),
                    },
                )
            )

        # Sort descending by probability
        scores.sort(key=lambda s: s.withdrawal_probability, reverse=True)
        for rank, s in enumerate(scores[:top_k], 1):
            s.predicted_rank = rank

        top_candidates = scores[:top_k]
        top_atm_name = top_candidates[0].atm_id if top_candidates else "None"
        
        return MLPredictionResponse(
            complaint_id=complaint_id,
            model_version=self.model_name,
            prediction_timestamp=datetime.now(timezone.utc),
            top_candidate_atms=top_candidates,
            summary_insight=f"Identified {len(top_candidates)} priority cash withdrawal targets. Top candidate: {top_atm_name}.",
        )
