import reflex as rx
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class User(BaseModel):
    """User model for authentication and profile."""

    id: int = 0
    username: str
    password_hash: str
    is_admin: bool = False
    total_points: int = 0
    payment_status: str = "pending"
    created_at: str = str(datetime.now())


class Match(BaseModel):
    """Match model for sports events."""

    id: int = 0
    team1: str
    team2: str
    start_time: str = str(datetime.now())
    status: str = "upcoming"
    team1_score: Optional[int] = None
    team2_score: Optional[int] = None


class Prediction(BaseModel):
    """User predictions for matches."""

    id: int = 0
    user_id: int
    match_id: int
    team1_prediction: int
    team2_prediction: int
    points_earned: int = 0
    boost_active: bool = False
    created_at: str = str(datetime.now())


class Payment(BaseModel):
    """Payment records (placeholder for future phases)."""

    id: int = 0
    user_id: int
    amount: float
    date: str = str(datetime.now())
    status: str = "completed"