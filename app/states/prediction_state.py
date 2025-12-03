import reflex as rx
import logging
from typing import Optional
from datetime import datetime, timedelta
from app.states.base_state import BaseState
from app.models import Match, Prediction
from app.database.database import SessionLocal
from app.database import service


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
        return sorted(
            list(self.my_predictions.values()), key=lambda x: x.created_at, reverse=True
        )

    @rx.event
    def get_match_by_id(self, match_id: int) -> Optional[Match]:
        for m in self.matches:
            if m.id == match_id:
                return m
        return None

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def load_data(self):
        """Load matches and user predictions."""
        with SessionLocal() as db:
            matches_sqla = service.get_matches(db)
            self.matches = [
                Match(
                    id=m.id,
                    team1=m.team1,
                    team2=m.team2,
                    start_time=str(m.start_time),
                    status=m.status,
                    team1_score=m.team1_score,
                    team2_score=m.team2_score,
                )
                for m in matches_sqla
            ]
            self.my_predictions = {}
            if self.current_user:
                preds_sqla = service.get_user_predictions(db, self.current_user.id)
                for p in preds_sqla:
                    self.my_predictions[p.match_id] = Prediction(
                        id=p.id,
                        user_id=p.user_id,
                        match_id=p.match_id,
                        team1_prediction=p.team1_prediction,
                        team2_prediction=p.team2_prediction,
                        points_earned=p.points_earned,
                        boost_active=p.boost_active,
                        created_at=str(p.created_at),
                    )

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
            yield rx.toast.error("Match not found locally. Please refresh.")
            return
        start_time = datetime.fromisoformat(match.start_time)
        if datetime.now() > start_time - timedelta(minutes=5):
            yield rx.toast.error("Predictions are locked for this match.")
            return
        with SessionLocal() as db:
            try:
                pred_sqla = service.create_or_update_prediction(
                    db,
                    user_id=self.current_user.id,
                    match_id=match_id,
                    team1_pred=team1_pred,
                    team2_pred=team2_pred,
                    boost_active=boost_active,
                )
                self.my_predictions[match_id] = Prediction(
                    id=pred_sqla.id,
                    user_id=pred_sqla.user_id,
                    match_id=pred_sqla.match_id,
                    team1_prediction=pred_sqla.team1_prediction,
                    team2_prediction=pred_sqla.team2_prediction,
                    points_earned=pred_sqla.points_earned,
                    boost_active=pred_sqla.boost_active,
                    created_at=str(pred_sqla.created_at),
                )
                self.my_predictions = self.my_predictions.copy()
                yield rx.toast.success("Prediction submitted!")
            except Exception as e:
                logging.exception(f"Error saving prediction: {e}")
                yield rx.toast.error("Failed to save prediction.")