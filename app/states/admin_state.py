import reflex as rx
import logging
from datetime import datetime
from app.states.base_state import BaseState
from app.models import User, Match, Payment, Prediction
from app.database.database import SessionLocal
from app.database import service
from app.database.models import Prediction as PredictionModel


class AdminState(BaseState):
    """State for the admin dashboard."""

    active_tab: str = "users"
    users: list[User] = []
    matches: list[Match] = []
    payments: list[Payment] = []
    predictions: list[Prediction] = []
    is_match_modal_open: bool = False
    editing_match_id: int = 0
    match_team1: str = ""
    match_team2: str = ""
    match_start_time: str = ""
    match_status: str = "upcoming"
    match_score1: int = 0
    match_score2: int = 0
    is_payment_modal_open: bool = False
    payment_user_id: int = 0
    payment_amount: float = 0.0
    payment_status: str = "completed"

    @rx.event
    def on_mount(self):
        """Check admin access and load data."""
        if not self.current_user or not self.current_user.is_admin:
            return rx.redirect("/")
        self.load_data()

    @rx.event
    def load_data(self):
        """Refresh all admin data."""
        with SessionLocal() as db:
            users_sqla = service.get_all_users(db)
            self.users = [
                User(
                    id=u.id,
                    username=u.username,
                    password_hash=u.password_hash,
                    is_admin=u.is_admin,
                    total_points=u.total_points,
                    payment_status=u.payment_status,
                    created_at=str(u.created_at),
                )
                for u in users_sqla
            ]
            matches_sqla = service.get_matches(db)
            matches_sqla.sort(key=lambda x: x.id, reverse=True)
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
            payments_sqla = service.get_all_payments(db)
            self.payments = [
                Payment(
                    id=p.id,
                    user_id=p.user_id,
                    amount=p.amount,
                    date=str(p.date),
                    status=p.status,
                )
                for p in payments_sqla
            ]
            predictions_sqla = (
                db.query(PredictionModel)
                .order_by(PredictionModel.created_at.desc())
                .limit(100)
                .all()
            )
            self.predictions = [
                Prediction(
                    id=p.id,
                    user_id=p.user_id,
                    match_id=p.match_id,
                    team1_prediction=p.team1_prediction,
                    team2_prediction=p.team2_prediction,
                    points_earned=p.points_earned,
                    boost_active=p.boost_active,
                    created_at=str(p.created_at),
                )
                for p in predictions_sqla
            ]

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def toggle_admin(self, user_id: int):
        with SessionLocal() as db:
            service.toggle_user_admin(db, user_id)
        self.load_data()
        yield rx.toast.success("User role updated")

    @rx.event
    def delete_user(self, user_id: int):
        with SessionLocal() as db:
            service.delete_user(db, user_id)
        self.load_data()
        yield rx.toast.success("User deleted")

    @rx.event
    def update_payment_status(self, user_id: int, status: str):
        with SessionLocal() as db:
            service.update_user_payment(db, user_id, status)
        self.load_data()
        yield rx.toast.success(f"Payment status updated to {status}")

    @rx.event
    def open_match_modal(self, match_id: int = 0):
        self.editing_match_id = match_id
        if match_id == 0:
            self.match_team1 = ""
            self.match_team2 = ""
            self.match_start_time = str(datetime.now().strftime("%Y-%m-%dT%H:%M"))
            self.match_status = "upcoming"
            self.match_score1 = 0
            self.match_score2 = 0
        else:
            match = next((m for m in self.matches if m.id == match_id), None)
            if match:
                self.match_team1 = match.team1
                self.match_team2 = match.team2
                self.match_start_time = match.start_time
                self.match_status = match.status
                self.match_score1 = (
                    match.team1_score if match.team1_score is not None else 0
                )
                self.match_score2 = (
                    match.team2_score if match.team2_score is not None else 0
                )
        self.is_match_modal_open = True

    @rx.event
    def close_match_modal(self):
        self.is_match_modal_open = False

    @rx.event
    def save_match(self, form_data: dict):
        try:
            team1 = form_data.get("team1")
            team2 = form_data.get("team2")
            start_time_str = form_data.get("start_time")
            status = form_data.get("status")
            score1 = int(form_data.get("score1", 0))
            score2 = int(form_data.get("score2", 0))
            if not team1 or not team2:
                yield rx.toast.error("Team names are required")
                return
            try:
                start_time = datetime.fromisoformat(start_time_str)
            except ValueError as e:
                logging.exception(f"Error parsing ISO format: {e}")
                try:
                    start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
                except ValueError as e2:
                    logging.exception(f"Error parsing fallback format: {e2}")
                    yield rx.toast.error("Invalid date format")
                    return
            with SessionLocal() as db:
                if self.editing_match_id == 0:
                    service.create_match(db, team1, team2, start_time, status)
                    yield rx.toast.success("Match created")
                else:
                    service.update_match(
                        db,
                        self.editing_match_id,
                        team1,
                        team2,
                        start_time,
                        status,
                        score1 if status != "upcoming" else None,
                        score2 if status != "upcoming" else None,
                    )
                    yield rx.toast.success("Match updated")
            self.is_match_modal_open = False
            self.load_data()
        except Exception as e:
            logging.exception(f"Error saving match: {e}")
            yield rx.toast.error("Failed to save match")

    @rx.event
    def delete_match(self, match_id: int):
        with SessionLocal() as db:
            service.delete_match(db, match_id)
        self.load_data()
        yield rx.toast.success("Match deleted")

    @rx.event
    def open_payment_modal(self):
        self.is_payment_modal_open = True
        self.payment_amount = 0.0
        self.payment_status = "completed"
        if self.users:
            self.payment_user_id = self.users[0].id

    @rx.event
    def close_payment_modal(self):
        self.is_payment_modal_open = False

    @rx.event
    def save_payment(self, form_data: dict):
        try:
            user_id = int(form_data.get("user_id"))
            amount = float(form_data.get("amount"))
            status = form_data.get("status")
            with SessionLocal() as db:
                service.create_payment(db, user_id, amount, status)
            self.is_payment_modal_open = False
            self.load_data()
            yield rx.toast.success("Payment recorded")
        except Exception as e:
            logging.exception(f"Error saving payment: {e}")
            yield rx.toast.error("Invalid payment data")

    @rx.var
    def get_username_map(self) -> dict[int, str]:
        return {u.id: u.username for u in self.users}

    @rx.var
    def get_match_map(self) -> dict[int, str]:
        return {m.id: f"{m.team1} vs {m.team2}" for m in self.matches}