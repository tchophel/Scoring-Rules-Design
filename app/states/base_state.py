import reflex as rx
from app.models import User, Match, Prediction
from typing import Optional
import hashlib
from datetime import datetime, timedelta
import random


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def calculate_points_for_match(match: Match, prediction: Prediction) -> int:
    """
    Calculate points based on rules:
    7 points: both scores exactly correct
    5 points: one score correct
    2 points: both scores wrong, but the user predicts the correct winner
    0 points: completely wrong

    If boost_active is True, points are doubled.
    """
    points = 0
    if (
        match.status != "finished"
        or match.team1_score is None
        or match.team2_score is None
    ):
        return 0
    if (
        match.team1_score == prediction.team1_prediction
        and match.team2_score == prediction.team2_prediction
    ):
        points = 7
    elif (
        match.team1_score == prediction.team1_prediction
        or match.team2_score == prediction.team2_prediction
    ):
        points = 5
    else:
        actual_diff = match.team1_score - match.team2_score
        pred_diff = prediction.team1_prediction - prediction.team2_prediction
        if (
            actual_diff > 0
            and pred_diff > 0
            or (actual_diff < 0 and pred_diff < 0)
            or (actual_diff == 0 and pred_diff == 0)
        ):
            points = 2
    if prediction.boost_active:
        points *= 2
    return points


MOCK_USERS: list[User] = []
MOCK_MATCHES: list[Match] = []
MOCK_PREDICTIONS: list[Prediction] = []
if not MOCK_USERS:
    admin = User(
        id=1,
        username="admin",
        password_hash=hash_password("admin123"),
        is_admin=True,
        total_points=150,
        payment_status="paid",
    )
    MOCK_USERS.append(admin)
    for i in range(4):
        user = User(
            id=i + 2,
            username=f"user{i + 1}",
            password_hash=hash_password(f"password{i + 1}"),
            is_admin=False,
            total_points=random.randint(10, 80),
            payment_status="paid",
        )
        MOCK_USERS.append(user)
if not MOCK_MATCHES:
    teams = [
        "Real Madrid",
        "Barcelona",
        "Man City",
        "Liverpool",
        "Bayern Munich",
        "PSG",
        "Juventus",
        "Inter Milan",
        "Arsenal",
        "Chelsea",
    ]
    match_id = 1
    for i in range(5):
        t1, t2 = random.sample(teams, 2)
        score1 = random.randint(0, 3)
        score2 = random.randint(0, 3)
        match = Match(
            id=match_id,
            team1=t1,
            team2=t2,
            start_time=str(datetime.now() - timedelta(days=i + 1)),
            status="finished",
            team1_score=score1,
            team2_score=score2,
        )
        MOCK_MATCHES.append(match)
        for user in MOCK_USERS:
            if random.random() > 0.8:
                continue
            p1 = random.randint(0, 3)
            p2 = random.randint(0, 3)
            boost = random.choice([True, False]) if random.random() > 0.7 else False
            pred = Prediction(
                id=len(MOCK_PREDICTIONS) + 1,
                user_id=user.id,
                match_id=match.id,
                team1_prediction=p1,
                team2_prediction=p2,
                boost_active=boost,
                created_at=str(datetime.now() - timedelta(days=i + 1, hours=2)),
            )
            pred.points_earned = calculate_points_for_match(match, pred)
            MOCK_PREDICTIONS.append(pred)
        match_id += 1
    t1, t2 = random.sample(teams, 2)
    match = Match(
        id=match_id,
        team1=t1,
        team2=t2,
        start_time=str(datetime.now() - timedelta(minutes=45)),
        status="live",
        team1_score=1,
        team2_score=0,
    )
    MOCK_MATCHES.append(match)
    match_id += 1
    t1, t2 = random.sample(teams, 2)
    match = Match(
        id=match_id,
        team1=t1,
        team2=t2,
        start_time=str(datetime.now() + timedelta(minutes=3)),
        status="upcoming",
    )
    MOCK_MATCHES.append(match)
    match_id += 1
    for i in range(5):
        t1, t2 = random.sample(teams, 2)
    match = Match(
        id=match_id,
        team1=t1,
        team2=t2,
        start_time=str(datetime.now() + timedelta(days=i, hours=random.randint(2, 20))),
        status="upcoming",
    )
    MOCK_MATCHES.append(match)
    match_id += 1
MOCK_PAYMENTS: list = []


class BaseState(rx.State):
    """The base state for the app."""

    current_user: Optional[User] = None

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    @rx.var
    def is_admin(self) -> bool:
        return self.current_user is not None and self.current_user.is_admin

    @rx.var
    def top_player(self) -> Optional[User]:
        """Get the user with the highest points."""
        if not MOCK_USERS:
            return None
        return sorted(MOCK_USERS, key=lambda u: u.total_points, reverse=True)[0]

    @rx.event
    def logout(self):
        """Logout the current user."""
        self.current_user = None
        return rx.redirect("/")

    def _get_user_from_db(self, username: str) -> Optional[User]:
        for user in MOCK_USERS:
            if user.username == username:
                return user
        return None

    @rx.event
    async def check_login(self):
        """Check if user is logged in (placeholder for persistent session logic)."""
        pass

    is_mobile_menu_open: bool = False

    @rx.event
    def toggle_mobile_menu(self):
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def close_mobile_menu(self):
        self.is_mobile_menu_open = False