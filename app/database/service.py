from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional
from datetime import datetime
from app.database.models import User, Match, Prediction, Payment
from app.utils import hash_password, calculate_points_for_match
from app.models import Match as MatchDTO, Prediction as PredictionDTO
import logging


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(
    db: Session, username: str, password_hash: str, is_admin: bool = False
) -> User:
    db_user = User(
        username=username,
        password_hash=password_hash,
        is_admin=is_admin,
        payment_status="paid" if is_admin else "pending",
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def get_leaderboard(db: Session) -> list[User]:
    return db.query(User).order_by(desc(User.total_points)).all()


def update_user_payment(db: Session, user_id: int, status: str) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if user:
        user.payment_status = status
        db.commit()
        db.refresh(user)
    return user


def toggle_user_admin(db: Session, user_id: int) -> Optional[User]:
    user = get_user_by_id(db, user_id)
    if user:
        user.is_admin = not user.is_admin
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> bool:
    user = get_user_by_id(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


def get_matches(db: Session, status: Optional[str] = None) -> list[Match]:
    query = db.query(Match)
    if status:
        query = query.filter(Match.status == status)
    return query.order_by(Match.start_time).all()


def get_match_by_id(db: Session, match_id: int) -> Optional[Match]:
    return db.query(Match).filter(Match.id == match_id).first()


def create_match(
    db: Session, team1: str, team2: str, start_time: datetime, status: str = "upcoming"
) -> Match:
    db_match = Match(team1=team1, team2=team2, start_time=start_time, status=status)
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def update_match(
    db: Session,
    match_id: int,
    team1: str,
    team2: str,
    start_time: datetime,
    status: str,
    team1_score: Optional[int] = None,
    team2_score: Optional[int] = None,
) -> Optional[Match]:
    match = get_match_by_id(db, match_id)
    if not match:
        return None
    match.team1 = team1
    match.team2 = team2
    match.start_time = start_time
    match.status = status
    match.team1_score = team1_score
    match.team2_score = team2_score
    if status == "finished" and team1_score is not None and (team2_score is not None):
        recalculate_points_for_match_predictions(db, match)
    db.commit()
    db.refresh(match)
    return match


def delete_match(db: Session, match_id: int) -> bool:
    match = get_match_by_id(db, match_id)
    if match:
        db.delete(match)
        db.commit()
        return True
    return False


def get_user_predictions(db: Session, user_id: int) -> list[Prediction]:
    return db.query(Prediction).filter(Prediction.user_id == user_id).all()


def get_prediction(db: Session, user_id: int, match_id: int) -> Optional[Prediction]:
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id, Prediction.match_id == match_id)
        .first()
    )


def create_or_update_prediction(
    db: Session,
    user_id: int,
    match_id: int,
    team1_pred: int,
    team2_pred: int,
    boost_active: bool,
) -> Prediction:
    prediction = get_prediction(db, user_id, match_id)
    if prediction:
        prediction.team1_prediction = team1_pred
        prediction.team2_prediction = team2_pred
        prediction.boost_active = boost_active
    else:
        prediction = Prediction(
            user_id=user_id,
            match_id=match_id,
            team1_prediction=team1_pred,
            team2_prediction=team2_pred,
            boost_active=boost_active,
        )
        db.add(prediction)
    db.commit()
    db.refresh(prediction)
    return prediction


def recalculate_points_for_match_predictions(db: Session, match: Match):
    """Update points for all predictions associated with a match."""
    if match.status != "finished" or match.team1_score is None:
        return
    match_dto = MatchDTO(
        id=match.id,
        team1=match.team1,
        team2=match.team2,
        start_time=str(match.start_time),
        status=match.status,
        team1_score=match.team1_score,
        team2_score=match.team2_score,
    )
    predictions = db.query(Prediction).filter(Prediction.match_id == match.id).all()
    for pred in predictions:
        pred_dto = PredictionDTO(
            id=pred.id,
            user_id=pred.user_id,
            match_id=pred.match_id,
            team1_prediction=pred.team1_prediction,
            team2_prediction=pred.team2_prediction,
            points_earned=pred.points_earned,
            boost_active=pred.boost_active,
            created_at=str(pred.created_at),
        )
        points = calculate_points_for_match(match_dto, pred_dto)
        if pred.points_earned != points:
            old_points = pred.points_earned
            pred.points_earned = points
            user = get_user_by_id(db, pred.user_id)
            if user:
                user.total_points = user.total_points - old_points + points
    db.commit()


def create_payment(
    db: Session, user_id: int, amount: float, status: str = "completed"
) -> Payment:
    payment = Payment(user_id=user_id, amount=amount, status=status)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def get_all_payments(db: Session) -> list[Payment]:
    return db.query(Payment).order_by(desc(Payment.date)).all()