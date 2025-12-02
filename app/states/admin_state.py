import reflex as rx
import logging
from datetime import datetime
from app.states.base_state import (
    BaseState,
    MOCK_USERS,
    MOCK_MATCHES,
    MOCK_PAYMENTS,
    MOCK_PREDICTIONS,
)
from app.models import User, Match, Payment, Prediction


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
        self.users = MOCK_USERS
        self.matches = sorted(MOCK_MATCHES, key=lambda m: m.id, reverse=True)
        self.payments = MOCK_PAYMENTS
        self.predictions = MOCK_PREDICTIONS

    @rx.event
    def set_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def toggle_admin(self, user_id: int):
        for user in MOCK_USERS:
            if user.id == user_id:
                user.is_admin = not user.is_admin
                break
        self.load_data()
        yield rx.toast.success("User role updated")

    @rx.event
    def delete_user(self, user_id: int):
        global MOCK_USERS
        MOCK_USERS = [u for u in MOCK_USERS if u.id != user_id]
        self.load_data()
        yield rx.toast.success("User deleted")

    @rx.event
    def update_payment_status(self, user_id: int, status: str):
        for user in MOCK_USERS:
            if user.id == user_id:
                user.payment_status = status
                break
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
            match = next((m for m in MOCK_MATCHES if m.id == match_id), None)
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
            start_time = form_data.get("start_time")
            status = form_data.get("status")
            score1 = int(form_data.get("score1", 0))
            score2 = int(form_data.get("score2", 0))
            if not team1 or not team2:
                yield rx.toast.error("Team names are required")
                return
            if self.editing_match_id == 0:
                new_id = max([m.id for m in MOCK_MATCHES]) + 1 if MOCK_MATCHES else 1
                new_match = Match(
                    id=new_id,
                    team1=team1,
                    team2=team2,
                    start_time=start_time,
                    status=status,
                    team1_score=score1 if status != "upcoming" else None,
                    team2_score=score2 if status != "upcoming" else None,
                )
                MOCK_MATCHES.append(new_match)
                yield rx.toast.success("Match created")
            else:
                for m in MOCK_MATCHES:
                    if m.id == self.editing_match_id:
                        m.team1 = team1
                        m.team2 = team2
                        m.start_time = start_time
                        m.status = status
                        m.team1_score = score1 if status != "upcoming" else None
                        m.team2_score = score2 if status != "upcoming" else None
                        break
                yield rx.toast.success("Match updated")
            self.is_match_modal_open = False
            self.load_data()
        except Exception as e:
            logging.exception(f"Error saving match: {e}")
            yield rx.toast.error("Failed to save match")

    @rx.event
    def delete_match(self, match_id: int):
        global MOCK_MATCHES
        MOCK_MATCHES = [m for m in MOCK_MATCHES if m.id != match_id]
        self.load_data()
        yield rx.toast.success("Match deleted")

    @rx.event
    def open_payment_modal(self):
        self.is_payment_modal_open = True
        self.payment_amount = 0.0
        self.payment_status = "completed"
        if MOCK_USERS:
            self.payment_user_id = MOCK_USERS[0].id

    @rx.event
    def close_payment_modal(self):
        self.is_payment_modal_open = False

    @rx.event
    def save_payment(self, form_data: dict):
        try:
            user_id = int(form_data.get("user_id"))
            amount = float(form_data.get("amount"))
            status = form_data.get("status")
            new_payment = Payment(
                id=len(MOCK_PAYMENTS) + 1,
                user_id=user_id,
                amount=amount,
                date=str(datetime.now()),
                status=status,
            )
            MOCK_PAYMENTS.append(new_payment)
            self.is_payment_modal_open = False
            self.load_data()
            yield rx.toast.success("Payment recorded")
        except Exception as e:
            logging.exception(f"Error saving payment: {e}")
            yield rx.toast.error("Invalid payment data")

    @rx.var
    def get_username_map(self) -> dict[int, str]:
        return {u.id: u.username for u in MOCK_USERS}

    @rx.var
    def get_match_map(self) -> dict[int, str]:
        return {m.id: f"{m.team1} vs {m.team2}" for m in MOCK_MATCHES}