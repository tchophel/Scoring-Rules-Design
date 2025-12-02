import reflex as rx
from app.states.base_state import BaseState, hash_password, MOCK_USERS
from app.models import User


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
        user = self._get_user_from_db(username)
        if user and user.password_hash == hash_password(password):
            if user.payment_status != "paid":
                self.error_message = f"Account status: {user.payment_status}. Please contact admin for payment."
                return
            self.current_user = user
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
        existing_user = self._get_user_from_db(username)
        if existing_user:
            self.error_message = "Username already taken."
            return
        new_user = User(
            id=len(MOCK_USERS) + 1,
            username=username,
            password_hash=hash_password(password),
            is_admin=False,
            total_points=0,
            payment_status="pending",
        )
        MOCK_USERS.append(new_user)
        return rx.redirect("/login")