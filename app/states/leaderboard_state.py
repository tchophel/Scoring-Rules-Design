import reflex as rx
from app.states.base_state import BaseState
from app.models import User
from app.database.database import SessionLocal
from app.database import service


class LeaderboardState(BaseState):
    """State for the leaderboard page."""

    ranked_users: list[tuple[int, User]] = []

    @rx.event
    def load_leaderboard(self):
        """Load and sort users by total points."""
        with SessionLocal() as db:
            leaderboard_sqla = service.get_leaderboard(db)
            self.ranked_users = [
                (
                    i,
                    User(
                        id=u.id,
                        username=u.username,
                        password_hash=u.password_hash,
                        is_admin=u.is_admin,
                        total_points=u.total_points,
                        payment_status=u.payment_status,
                        created_at=str(u.created_at),
                    ),
                )
                for i, u in enumerate(leaderboard_sqla)
            ]