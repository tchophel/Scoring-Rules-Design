import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database.models import User, Match, Prediction
from app.database.service import (
    create_user,
    create_match,
    create_or_update_prediction,
    update_match,
)
from app.utils import hash_password


def seed_data(db: Session):
    """Seed the database with initial data."""
    if db.query(User).count() > 0:
        print("Database already seeded.")
        return
    print("Seeding database...")
    admin = create_user(db, "admin", hash_password("admin123"), is_admin=True)
    users = [admin]
    for i in range(4):
        user = create_user(db, f"user{i + 1}", hash_password(f"password{i + 1}"))
        user.payment_status = "paid" if random.random() > 0.2 else "pending"
        users.append(user)
    db.commit()
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
    matches = []
    for i in range(5):
        t1, t2 = random.sample(teams, 2)
        start_time = datetime.now() - timedelta(days=i + 1)
        match = create_match(db, t1, t2, start_time, status="finished")
        update_match(
            db,
            match.id,
            match.team1,
            match.team2,
            match.start_time,
            "finished",
            random.randint(0, 3),
            random.randint(0, 3),
        )
        matches.append(match)
    t1, t2 = random.sample(teams, 2)
    live_match = create_match(
        db, t1, t2, datetime.now() - timedelta(minutes=45), status="live"
    )
    update_match(
        db,
        live_match.id,
        live_match.team1,
        live_match.team2,
        live_match.start_time,
        "live",
        1,
        0,
    )
    matches.append(live_match)
    for i in range(5):
        t1, t2 = random.sample(teams, 2)
        start_time = datetime.now() + timedelta(days=i, hours=random.randint(2, 20))
        upcoming = create_match(db, t1, t2, start_time, status="upcoming")
        matches.append(upcoming)
    for match in matches:
        if match.status == "finished":
            for user in users:
                if random.random() > 0.2:
                    p1 = random.randint(0, 3)
                    p2 = random.randint(0, 3)
                    boost = (
                        random.choice([True, False]) if random.random() > 0.7 else False
                    )
                    create_or_update_prediction(db, user.id, match.id, p1, p2, boost)
            update_match(
                db,
                match.id,
                match.team1,
                match.team2,
                match.start_time,
                match.status,
                match.team1_score,
                match.team2_score,
            )
    print("Database seeding complete.")