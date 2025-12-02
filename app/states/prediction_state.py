import reflex as rx
import logging
from typing import Optional
from datetime import datetime, timedelta
from app.states.base_state import (
    BaseState,
    MOCK_MATCHES,
    MOCK_PREDICTIONS,
    calculate_points_for_match,
)
from app.models import Match, Prediction


class PredictionState(BaseState):
    """State for managing matches and predictions."""

    matches: list[Match] = []
    my_predictions: dict[int, Prediction] = {}
    active_tab: str = "upcoming"

    @rx.var
    def upcoming_matches(self) -> list[Match]:
        return sorted(
            [m for m in self.matches if m.status == "upcoming"],
            key=lambda x: x.start_time,
        )

    @rx.var
    def live_matches(self) -> list[Match]:
        return [m for m in self.matches if m.status == "live"]

    @rx.var
    def finished_matches(self) -> list[Match]:
        return sorted(
            [m for m in self.matches if m.status == "finished"],
            key=lambda x: x.start_time,
            reverse=True,
        )

    @rx.var
    def my_prediction_list(self) -> list[Prediction]:
        """Return list of predictions for the current user to display in My Predictions page."""
        if not self.current_user:
            return []
        user_preds = [p for p in MOCK_PREDICTIONS if p.user_id == self.current_user.id]
        return sorted(user_preds, key=lambda x: x.created_at, reverse=True)

    @rx.event
    def get_match_by_id(self, match_id: int) -> Optional[Match]:
        for m in MOCK_MATCHES:
            if m.id == match_id:
                return m
        return None

    @rx.event
    def load_data(self):
        """Load matches and user predictions."""
        self.matches = MOCK_MATCHES
        self.my_predictions = {}
        if self.current_user:
            for pred in MOCK_PREDICTIONS:
                if pred.user_id == self.current_user.id:
                    self.my_predictions[pred.match_id] = pred

    @rx.event
    def submit_prediction(self, form_data: dict):
        """Submit a prediction for a match."""
        if not self.current_user:
            yield rx.toast.error("You must be logged in to predict.")
            return
        t1_raw = form_data.get("team1_score", "")
        t2_raw = form_data.get("team2_score", "")
        if t1_raw == "" or t2_raw == "":
            yield rx.toast.error("Please enter scores for both teams.")
            return
        try:
            match_id = int(form_data.get("match_id"))
            team1_pred = int(t1_raw)
            team2_pred = int(t2_raw)
        except (ValueError, TypeError) as e:
            logging.exception(f"Error parsing prediction input: {e}")
            yield rx.toast.error("Invalid input. Scores must be numbers.")
            return
        if team1_pred < 0 or team2_pred < 0:
            yield rx.toast.error("Scores cannot be negative.")
            return
        boost_active = bool(form_data.get("boost_active"))
        match = self.get_match_by_id(match_id)
        if not match:
            yield rx.toast.error("Match not found.")
            return
        start_time = datetime.fromisoformat(match.start_time)
        if datetime.now() > start_time - timedelta(minutes=5):
            yield rx.toast.error("Predictions are locked for this match.")
            return
        existing_pred_index = -1
        for i, p in enumerate(MOCK_PREDICTIONS):
            if p.user_id == self.current_user.id and p.match_id == match_id:
                existing_pred_index = i
                break
        if existing_pred_index != -1:
            p = MOCK_PREDICTIONS[existing_pred_index]
            p.team1_prediction = team1_pred
            p.team2_prediction = team2_pred
            p.boost_active = boost_active
            self.my_predictions[match_id] = p
            self.my_predictions = self.my_predictions.copy()
            yield rx.toast.success("Prediction updated!")
        else:
            new_pred = Prediction(
                id=len(MOCK_PREDICTIONS) + 1,
                user_id=self.current_user.id,
                match_id=match_id,
                team1_prediction=team1_pred,
                team2_prediction=team2_pred,
                boost_active=boost_active,
            )
            MOCK_PREDICTIONS.append(new_pred)
            self.my_predictions[match_id] = new_pred
            self.my_predictions = self.my_predictions.copy()
            yield rx.toast.success("Prediction submitted!")