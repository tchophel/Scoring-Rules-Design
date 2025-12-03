import reflex as rx
from app.models import User
from app.database.database import SessionLocal
from app.database import service
from typing import Optional


class BaseState(rx.State):
    """The base state for the app."""

    current_user: Optional[User] = None
    top_player: Optional[User] = None
    is_mobile_menu_open: bool = False

    @rx.var
    def is_authenticated(self) -> bool:
        return self.current_user is not None

    @rx.var
    def is_admin(self) -> bool:
        return self.current_user is not None and self.current_user.is_admin

    @rx.event
    def load_top_player(self):
        """Load the top player from the database."""
        with SessionLocal() as db:
            leaderboard = service.get_leaderboard(db)
            if leaderboard:
                top_sqla = leaderboard[0]
                self.top_player = User(
                    id=top_sqla.id,
                    username=top_sqla.username,
                    password_hash=top_sqla.password_hash,
                    is_admin=top_sqla.is_admin,
                    total_points=top_sqla.total_points,
                    payment_status=top_sqla.payment_status,
                    created_at=str(top_sqla.created_at),
                )
            else:
                self.top_player = None

    @rx.event
    def logout(self):
        """Logout the current user."""
        self.current_user = None
        return rx.redirect("/")

    @rx.event
    async def check_login(self):
        """Check if user is logged in (placeholder for persistent session logic)."""
        pass

    @rx.event
    def toggle_mobile_menu(self):
        self.is_mobile_menu_open = not self.is_mobile_menu_open

    @rx.event
    def close_mobile_menu(self):
        self.is_mobile_menu_open = False