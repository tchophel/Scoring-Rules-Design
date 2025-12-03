import hashlib
from app.models import Match, Prediction


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