import reflex as rx
from app.states.base_state import BaseState
from app.models import User
from app.utils import hash_password
from app.database.database import SessionLocal
from app.database import service


class AuthState(BaseState):
    """State for authentication pages."""

    error_message: str = ""

    @rx.event
    def on_mount(self):
        self.error_message = ""

    @rx.event
    def handle_login(self, form_data: dict):
        """Handle login form submission."""
        username = form_data.get("username")
        password = form_data.get("password")
        with SessionLocal() as db:
            user_sqla = service.get_user_by_username(db, username)
            if user_sqla and user_sqla.password_hash == hash_password(password):
                if user_sqla.payment_status != "paid":
                    self.error_message = f"Account status: {user_sqla.payment_status}. Please contact admin for payment."
                    return
                self.current_user = User(
                    id=user_sqla.id,
                    username=user_sqla.username,
                    password_hash=user_sqla.password_hash,
                    is_admin=user_sqla.is_admin,
                    total_points=user_sqla.total_points,
                    payment_status=user_sqla.payment_status,
                    created_at=str(user_sqla.created_at),
                )
                self.error_message = ""
                return rx.redirect("/")
            else:
                self.error_message = "Invalid username or password."

    @rx.event
    def handle_register(self, form_data: dict):
        """Handle registration form submission."""
        username = form_data.get("username")
        password = form_data.get("password")
        confirm_password = form_data.get("confirm_password")
        if password != confirm_password:
            self.error_message = "Passwords do not match."
            return
        if len(password) < 6:
            self.error_message = "Password must be at least 6 characters."
            return
        if not username:
            self.error_message = "Username is required."
            return
        with SessionLocal() as db:
            existing_user = service.get_user_by_username(db, username)
            if existing_user:
                self.error_message = "Username already taken."
                return
            service.create_user(
                db, username=username, password_hash=hash_password(password)
            )
        return rx.redirect("/login")