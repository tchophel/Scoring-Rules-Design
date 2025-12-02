import reflex as rx
from app.states.base_state import BaseState, MOCK_USERS
from app.models import User


class LeaderboardState(BaseState):
    """State for the leaderboard page."""

    ranked_users: list[tuple[int, User]] = []

    @rx.event
    def load_leaderboard(self):
        """Load and sort users by total points."""
        sorted_users = sorted(MOCK_USERS, key=lambda u: u.total_points, reverse=True)
        self.ranked_users = [(i, u) for i, u in enumerate(sorted_users)]